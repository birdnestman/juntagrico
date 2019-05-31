import hashlib

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from juntagrico.config import Config
from juntagrico.dao.depotdao import DepotDao
from juntagrico.dao.extrasubscriptioncategorydao import ExtraSubscriptionCategoryDao
from juntagrico.dao.extrasubscriptiontypedao import ExtraSubscriptionTypeDao
from juntagrico.dao.memberdao import MemberDao
from juntagrico.dao.subscriptionproductdao import SubscriptionProductDao
from juntagrico.decorators import primary_member_of_subscription
from juntagrico.entity.depot import Depot
from juntagrico.entity.extrasubs import ExtraSubscription
from juntagrico.entity.member import Member
from juntagrico.entity.share import Share
from juntagrico.entity.subs import Subscription
from juntagrico.entity.subtypes import TSST, TFSST
from juntagrico.forms import RegisterMemberForm
from juntagrico.mailer import send_subscription_canceled
from juntagrico.util import temporal, return_to_previous_location
from juntagrico.util.form_evaluation import selected_subscription_types
from juntagrico.util.management import create_or_update_member, replace_subscription_types
from juntagrico.util.temporal import end_of_next_business_year, next_cancelation_date, end_of_business_year, \
    cancelation_date
from juntagrico.views import get_menu_dict


@login_required
def subscription(request, subscription_id=None):
    '''
    Details for an subscription of a member
    '''
    member = request.user.member
    future_subscription = member.future_subscription is not None
    can_order = member.future_subscription is None and (
        member.subscription is None or member.subscription.canceled)
    renderdict = get_menu_dict(request)
    if subscription_id is None:
        subscription = member.subscription
    else:
        subscription = get_object_or_404(Subscription, id=subscription_id)
        future_subscription = future_subscription and not(
            subscription == member.future_subscription)
    end_date = end_of_next_business_year()

    if subscription is not None:
        cancelation_date = subscription.cancelation_date
        if cancelation_date is not None and cancelation_date <= next_cancelation_date():
            end_date = end_of_business_year()
        renderdict.update({
            'subscription': subscription,
            'co_members': subscription.recipients.exclude(
                email=request.user.member.email),
            'primary': subscription.primary_member.email == request.user.member.email,
            'next_extra_subscription_date': Subscription.next_extra_change_date(),
            'next_size_date': Subscription.next_size_change_date(),
            'has_extra_subscriptions': ExtraSubscriptionCategoryDao.all_categories_ordered().count() > 0,
        })
    renderdict.update({
        'no_subscription': subscription is None,
        'end_date': end_date,
        'can_order': can_order,
        'future_subscription': future_subscription,
        'member': request.user.member,
        'shares': request.user.member.active_shares.count(),
        'shares_unpaid': request.user.member.share_set.filter(paid_date=None).count(),
        'menu': {'subscription': 'active'},
    })
    return render(request, 'subscription.html', renderdict)


@primary_member_of_subscription
def subscription_change(request, subscription_id):
    '''
    change an subscription
    '''
    subscription = get_object_or_404(Subscription, id=subscription_id)
    now = timezone.now().date()
    can_change = not (temporal.cancelation_date() <= now < temporal.start_of_next_business_year())
    renderdict = get_menu_dict(request)
    renderdict.update({
        'subscription': subscription,
        'member': request.user.member,
        'change_size': can_change,
        'next_cancel_date': temporal.next_cancelation_date(),
        'next_extra_subscription_date': Subscription.next_extra_change_date(),
        'next_business_year': temporal.start_of_next_business_year()
    })
    return render(request, 'subscription_change.html', renderdict)


@primary_member_of_subscription
def depot_change(request, subscription_id):
    '''
    change a depot
    '''
    subscription = get_object_or_404(Subscription, id=subscription_id)
    saved = False
    if request.method == 'POST':
        if subscription.state == 'waiting':
            subscription.depot = get_object_or_404(
                Depot, id=int(request.POST.get('depot')))
        else:
            subscription.future_depot = get_object_or_404(
                Depot, id=int(request.POST.get('depot')))
        subscription.save()
        saved = True
    renderdict = get_menu_dict(request)
    depots = DepotDao.all_depots()
    requires_map = False
    for depot in depots:
        requires_map = requires_map or depot.has_geo
    renderdict.update({
        'subscription': subscription,
        'saved': saved,
        'member': request.user.member,
        'depots': depots,
        'requires_map': requires_map,
    })
    return render(request, 'depot_change.html', renderdict)


@primary_member_of_subscription
def size_change(request, subscription_id, multi=False):
    """
    change the size of a subscription
    """
    subscription = get_object_or_404(Subscription, id=subscription_id)
    saved = False
    share_error = False
    if request.method == 'POST' and int(timezone.now().strftime('%m')) <= Config.business_year_cancelation_month():
        # create dict with subscription type -> selected amount
        selected = selected_subscription_types(request.POST)
        # check if members of sub have enough shares
        if subscription.all_shares < sum([sub_type.shares * amount for sub_type, amount in selected.items()]):
            share_error = True
        elif sum(selected.values()) > 0:  # check that at least one subscription was selected
            replace_subscription_types(subscription, selected)
            saved = True
    products = SubscriptionProductDao.get_all()
    renderdict = get_menu_dict(request)
    renderdict.update({
        'saved': saved,
        'subscription': subscription,
        'shareerror': share_error,
        'hours_used': Config.assignment_unit() == 'HOURS',
        'next_cancel_date': temporal.next_cancelation_date(),
        'selected_subscription': subscription.future_types.all()[0].id,
        'products': products,
        'multi_edit': (multi or subscription.types.count() > 1) and Config.allow_multiple_subscriptions(),
    })
    return render(request, 'size_change.html', renderdict)


@primary_member_of_subscription
def extra_change(request, subscription_id):
    '''
    change an extra subscription
    '''
    subscription = get_object_or_404(Subscription, id=subscription_id)
    if request.method == 'POST':
        for type in ExtraSubscriptionTypeDao.all_extra_types():
            value = int(request.POST.get('extra'+str(type.id)))
            if value > 0:
                for x in range(value):
                    ExtraSubscription.objects.create(
                        main_subscription=subscription, type=type)
        return redirect('/my/subscription/change/extra/'+str(subscription.id)+'/')
    renderdict = get_menu_dict(request)
    renderdict.update({
        'types': ExtraSubscriptionTypeDao.all_extra_types(),
        'extras': subscription.extra_subscription_set.all(),
        'sub_id': subscription_id
    })
    return render(request, 'extra_change.html', renderdict)


def signup(request):
    '''
    Become a member of juntagrico
    '''
    if Config.enable_registration() is False:
        raise Http404
    logout(request)
    success = False
    agberror = False
    agbchecked = False
    userexists = False
    if request.method == 'POST':
        agbchecked = request.POST.get('agb') == 'on'
        memberform = RegisterMemberForm(request.POST)
        if not agbchecked:
            agberror = True
        else:
            if memberform.is_valid():
                # check if user already exists
                email = memberform.cleaned_data['email']
                if User.objects.filter(email__iexact=email).__len__() > 0:
                    userexists = True
                else:
                    member = Member(**memberform.cleaned_data)
                    request.session['main_member'] = member
                    return redirect('/my/create/subscription')
    else:
        memberform = RegisterMemberForm()

    renderdict = {
        'memberform': memberform,
        'success': success,
        'agberror': agberror,
        'agbchecked': agbchecked,
        'userexists': userexists,
        'menu': {'join': 'active'},
    }
    return render(request, 'signup.html', renderdict)


def confirm(request, hash):
    '''
    Confirm from a user that has been added as a co_subscription member
    '''

    for member in MemberDao.all_members():
        if hash == hashlib.sha1((member.email + str(member.id)).encode('utf8')).hexdigest():
            member.confirmed = True
            member.save()

    return redirect('/my/home')


@primary_member_of_subscription
def add_member(request, subscription_id):
    share_error = False
    shares = 0
    member_exists = False
    member_blocked = False
    main_member = request.user.member
    subscription = get_object_or_404(Subscription, id=subscription_id)
    if request.method == 'POST':
        # validate shares
        try:
            if Config.enable_shares():
                shares = int(request.POST.get('shares'))
                share_error = shares < 0
        except ValueError:
            share_error = True

        memberform = RegisterMemberForm(request.POST)
        member = MemberDao.member_by_email(request.POST.get('email'))
        if member is not None:  # use existing member
            member_exists = True
            member_blocked = member.blocked
        elif memberform.is_valid():  # or create new member
            member = Member(**memberform.cleaned_data)
        if member is not None:
            create_or_update_member(member, subscription, shares, main_member)
            return redirect('/my/subscription/detail/' + str(subscription_id) + '/')
    else:
        initial = {'addr_street': main_member.addr_street,
                   'addr_zipcode': main_member.addr_zipcode,
                   'addr_location': main_member.addr_location,
                   'phone': main_member.phone,
                   }
        memberform = RegisterMemberForm(initial=initial)
    renderdict = {
        'shares': shares,
        'memberexists': member_exists,
        'memberblocked': member_blocked,
        'shareerror': share_error,
        'memberform': memberform,
        'subscription_id': subscription_id
    }
    return render(request, 'add_member.html', renderdict)


@permission_required('juntagrico.is_operations_group')
def activate_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    change_date = request.session.get('changedate', None)
    if subscription.active is False and subscription.deactivation_date is None:
        try:
            subscription.active = True
            subscription.activation_date = change_date
            subscription.save()
        except ValidationError:
            renderdict = get_menu_dict(request)
            return render(request, 'activation_error.html', renderdict)
    return return_to_previous_location(request)


@permission_required('juntagrico.is_operations_group')
def deactivate_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    change_date = request.session.get('changedate', None)
    if subscription.active is True:
        subscription.active = False
        subscription.deactivation_date = change_date
        subscription.save()
        for extra in subscription.extra_subscription_set.all():
            if extra.active is True:
                extra.active = False
                extra.deactivation_date = change_date
                extra.save()
    return return_to_previous_location(request)


@permission_required('juntagrico.is_operations_group')
def activate_future_types(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    for type in TSST.objects.filter(subscription=subscription):
        type.delete()
    for type in TFSST.objects.filter(subscription=subscription):
        TSST.objects.create(subscription=subscription, type=type.type)
    return return_to_previous_location(request)


@primary_member_of_subscription
def cancel_subscription(request, subscription_id):
    subscription = get_object_or_404(Subscription, id=subscription_id)
    now = timezone.now().date()
    if now <= cancelation_date():
        end_date = end_of_business_year()
    else:
        end_date = end_of_next_business_year()
    if request.method == 'POST':
        if subscription.active is True and subscription.canceled is False:
            subscription.canceled = True
            subscription.end_date = request.POST.get('end_date')
            subscription.save()
            message = request.POST.get('message')
            send_subscription_canceled(subscription, message)
            for extra in subscription.extra_subscription_set.all():
                if extra.active is True:
                    extra.canceled = True
                    extra.save()
                elif extra.active is False and extra.deactivation_date is None:
                    extra.delete()
        elif subscription.active is False and subscription.deactivation_date is None:
            subscription.delete()
        return redirect('/my/subscription/detail')

    renderdict = get_menu_dict(request)
    renderdict.update({
        'end_date': end_date,
    })
    return render(request, 'cancelsubscription.html', renderdict)


@permission_required('juntagrico.is_operations_group')
def activate_extra(request, extra_id):
    extra = get_object_or_404(ExtraSubscription, id=extra_id)
    change_date = request.session.get('changedate', None)
    if extra.active is False and extra.deactivation_date is None:
        extra.active = True
        extra.activation_date = change_date
        extra.save()
    return return_to_previous_location(request)


@permission_required('juntagrico.is_operations_group')
def deactivate_extra(request, extra_id):
    extra = get_object_or_404(ExtraSubscription, id=extra_id)
    change_date = request.session.get('changedate', None)
    if extra.active is True:
        extra.active = False
        extra.deactivation_date = change_date
        extra.save()
    return return_to_previous_location(request)


@primary_member_of_subscription
def cancel_extra(request, extra_id, subscription_id):
    extra = get_object_or_404(ExtraSubscription, id=extra_id)
    if extra.active is False:
        extra.delete()
    else:
        extra.canceled = True
        extra.save()
    return return_to_previous_location(request)


@login_required
def order_shares(request):
    if request.method == 'POST':
        referer = request.POST.get('referer')
        try:
            shares = int(request.POST.get('shares'))
            shareerror = shares < 1
        except ValueError:
            shareerror = True
        if not shareerror:
            member = request.user.member
            for num in range(0, shares):
                Share.objects.create(member=member, paid_date=None)
            return redirect('/my/order/share/success?referer='+referer)
    else:
        shareerror = False
        if request.META.get('HTTP_REFERER')is not None:
            referer = request.META.get('HTTP_REFERER')
        else:
            referer = 'http://'+Config.adminportal_server_url()
    renderdict = get_menu_dict(request)
    renderdict.update({
        'referer': referer,
        'shareerror': shareerror
    })
    return render(request, 'order_share.html', renderdict)


@login_required
def order_shares_success(request):
    if request.GET.get('referer')is not None:
        referer = request.GET.get('referer')
    else:
        referer = 'http://'+Config.adminportal_server_url()
    renderdict = get_menu_dict(request)
    renderdict.update({
        'referer': referer
    })
    return render(request, 'order_share_success.html', renderdict)


@permission_required('juntagrico.is_operations_group')
def payout_share(request, share_id):
    share = get_object_or_404(Share, id=share_id)
    share.payback_date = timezone.now()
    share.save()
    member = share.member
    if member.active_shares_count == 0 and member.canceled is True:
        member.inactive = True
        member.save()
    return return_to_previous_location(request)
