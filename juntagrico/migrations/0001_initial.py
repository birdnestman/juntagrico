# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-15 04:55
from __future__ import unicode_literals

import re

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import juntagrico.util.temporal 


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('description', models.TextField(default=b'', max_length=1000, verbose_name=b'Beschreibung')),
                ('core', models.BooleanField(default=False, verbose_name=b'Kernbereich')),
                ('hidden', models.BooleanField(default=False, verbose_name=b'versteckt')),
                ('show_coordinator_phonenumber', models.BooleanField(default=False, verbose_name=b'Koordinator Tel Nr Ver\xc3\xb6ffentlichen')),
            ],
            options={
                'verbose_name': 'T\xe4tigkeitsbereich',
                'verbose_name_plural': 'T\xe4tigkeitsbereiche',
                'permissions': (('is_area_admin', 'Benutzer ist T\xe4tigkeitsbereichskoordinatorIn'),),
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('core_cache', models.BooleanField(default=False, verbose_name=b'Kernbereich')),
            ],
            options={
                'verbose_name': 'Mitglied',
                'verbose_name_plural': 'Arbeitseins\xe4tze',
            },
        ),
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(max_length=20)),
                ('field', models.CharField(max_length=100)),
                ('source_id', models.PositiveIntegerField()),
                ('target_id', models.PositiveIntegerField(blank=True, null=True)),
                ('source_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_set', to='contenttypes.ContentType')),
                ('target_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='target_set', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False, verbose_name=b'bezahlt')),
                ('bill_date', models.DateField(blank=True, null=True, verbose_name=b'Aktivierungssdatum')),
                ('ref_number', models.CharField(max_length=30, unique=True, verbose_name=b'Referenznummer')),
                ('amount', models.FloatField(verbose_name=b'Betrag')),
            ],
            options={
                'verbose_name': 'Rechnung',
                'verbose_name_plural': 'Rechnungen',
            },
        ),
        migrations.CreateModel(
            name='Billable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Verrechenbare Einheit',
                'verbose_name_plural': 'Verrechenbare Einhaiten',
            },
        ),
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-a-zA-Z0-9_]+\\Z'), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name=b'Code')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Depot Name')),
                ('weekday', models.PositiveIntegerField(choices=[(1, b'Montag'), (2, b'Dienstag'), (3, b'Mittwoch'), (4, b'Donnerstag'), (5, b'Freitag'), (6, b'Samstag'), (7, b'Sonntag')], verbose_name=b'Wochentag')),
                ('latitude', models.CharField(default=b'', max_length=100, verbose_name=b'Latitude')),
                ('longitude', models.CharField(default=b'', max_length=100, verbose_name=b'Longitude')),
                ('addr_street', models.CharField(max_length=100, verbose_name=b'Strasse')),
                ('addr_zipcode', models.CharField(max_length=10, verbose_name=b'PLZ')),
                ('addr_location', models.CharField(max_length=50, verbose_name=b'Ort')),
                ('description', models.TextField(default=b'', max_length=1000, verbose_name=b'Beschreibung')),
            ],
            options={
                'verbose_name': 'Depot',
                'verbose_name_plural': 'Depots',
                'permissions': (('is_depot_admin', 'Benutzer ist Depot Admin'),),
            },
        ),
        migrations.CreateModel(
            name='ExtraSubscriptionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name=b'Beschreibung')),
                ('sort_order', models.FloatField(default=1.0, verbose_name=b'Nummer zum Sortieren')),
            ],
            options={
                'verbose_name': 'Zusatz-Abo-Kategorie',
                'verbose_name_plural': 'Zusatz-Abo-Kategorien',
            },
        ),
        migrations.CreateModel(
            name='ExtraSubscriptionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('size', models.CharField(default=b'', max_length=100, verbose_name=b'Groesse (gross,4, ...)')),
                ('description', models.TextField(max_length=1000, verbose_name=b'Beschreibung')),
                ('sort_order', models.FloatField(default=1.0, verbose_name=b'Groesse zum Sortieren')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='category', to='juntagrico.ExtraSubscriptionCategory')),
            ],
            options={
                'verbose_name': 'Zusatz-Abo-Typ',
                'verbose_name_plural': 'Zusatz-Abo-Typen',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slots', models.PositiveIntegerField(verbose_name=b'Plaetze')),
                ('time', models.DateTimeField()),
                ('pinned', models.BooleanField(default=False)),
                ('reminder_sent', models.BooleanField(default=False, verbose_name=b'Reminder verschickt')),
                ('canceled', models.BooleanField(default=False, verbose_name=b'abgesagt')),
            ],
            options={
                'verbose_name': 'AbstractJob',
                'verbose_name_plural': 'AbstractJobs',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('displayed_name', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Angezeigter Name')),
                ('description', models.TextField(default=b'', max_length=1000, verbose_name=b'Beschreibung')),
                ('duration', models.PositiveIntegerField(verbose_name=b'Dauer in Stunden')),
                ('location', models.CharField(default=b'', max_length=100, verbose_name=b'Ort')),
                ('activityarea', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.ActivityArea')),
            ],
            options={
                'verbose_name': 'Jobart',
                'verbose_name_plural': 'Jobarten',
            },
        ),
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('template', models.TextField(default=b'', max_length=1000, verbose_name=b'Template')),
                ('code', models.TextField(default=b'', max_length=1000, verbose_name=b'Code')),
            ],
            options={
                'verbose_name': 'MailTemplate',
                'verbose_name_plural': 'MailTemplates',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name=b'Vorname')),
                ('last_name', models.CharField(max_length=30, verbose_name=b'Nachname')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('addr_street', models.CharField(max_length=100, verbose_name=b'Strasse')),
                ('addr_zipcode', models.CharField(max_length=10, verbose_name=b'PLZ')),
                ('addr_location', models.CharField(max_length=50, verbose_name=b'Ort')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name=b'Geburtsdatum')),
                ('phone', models.CharField(max_length=50, verbose_name=b'Telefonnr')),
                ('mobile_phone', models.CharField(blank=True, max_length=50, null=True, verbose_name=b'Mobile')),
                ('confirmed', models.BooleanField(default=True, verbose_name=b'best\xc3\xa4tigt')),
                ('reachable_by_email', models.BooleanField(default=False, verbose_name=b'Kontaktierbar von der Job Seite aus')),
                ('block_emails', models.BooleanField(default=False, verbose_name=b'keine emails')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mitglied',
                'verbose_name_plural': 'Mitglieder',
                'permissions': (('can_filter_members', 'Benutzer kann Mitglieder filtern'),),
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_date', models.DateField(blank=True, null=True, verbose_name=b'Bezahldatum')),
                ('amount', models.FloatField(verbose_name=b'Betrag')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='juntagrico.Bill')),
            ],
            options={
                'verbose_name': 'Zahlung',
                'verbose_name_plural': 'Zahlung',
            },
        ),
        migrations.CreateModel(
            name='SpecialRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'), ('can_send_mails', 'Benutzer kann im System Emails versenden'), ('can_use_general_email', 'Benutzer kann General Email Adresse verwenden')),
            },
        ),
        migrations.CreateModel(
            name='SubscriptionSize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('long_name', models.CharField(max_length=100, unique=True, verbose_name=b'Langer Name')),
                ('size', models.PositiveIntegerField(unique=True, verbose_name=b'Gr\xc3\xb6sse')),
                ('shares', models.PositiveIntegerField(verbose_name=b'Anz ben\xc3\xb6tigter Anteilsscheine')),
                ('depot_list', models.BooleanField(default=True, verbose_name=b'Sichtbar auf Depotliste')),
                ('description', models.TextField(blank=True, max_length=1000, verbose_name=b'Beschreibung')),
            ],
            options={
                'verbose_name': 'Abo Gr\xf6sse',
                'verbose_name_plural': 'Abo Gr\xf6ssen',
            },
        ),
        migrations.CreateModel(
            name='ExtraSubscription',
            fields=[
                ('billable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='juntagrico.Billable')),
                ('active', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(default=False, verbose_name=b'gek\xc3\xbcndigt')),
                ('activation_date', models.DateField(blank=True, null=True, verbose_name=b'Aktivierungssdatum')),
                ('deactivation_date', models.DateField(blank=True, null=True, verbose_name=b'Deaktivierungssdatum')),
            ],
            options={
                'verbose_name': 'Zusatz-Abo',
                'verbose_name_plural': 'Zusatz-Abos',
            },
            bases=('juntagrico.billable',),
        ),
        migrations.CreateModel(
            name='OneTimeJob',
            fields=[
                ('job_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='juntagrico.Job')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name=b'Name')),
                ('displayed_name', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'Angezeigter Name')),
                ('description', models.TextField(default=b'', max_length=1000, verbose_name=b'Beschreibung')),
                ('duration', models.PositiveIntegerField(verbose_name=b'Dauer in Stunden')),
                ('location', models.CharField(default=b'', max_length=100, verbose_name=b'Ort')),
            ],
            options={
                'verbose_name': 'EinzelJob',
                'verbose_name_plural': 'EinzelJobs',
            },
            bases=('juntagrico.job', models.Model),
        ),
        migrations.CreateModel(
            name='RecuringJob',
            fields=[
                ('job_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='juntagrico.Job')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.JobType')),
            ],
            options={
                'verbose_name': 'Job',
                'verbose_name_plural': 'Jobs',
            },
            bases=('juntagrico.job',),
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('billable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='juntagrico.Billable')),
                ('paid_date', models.DateField(blank=True, null=True, verbose_name=b'Bezahlt am')),
                ('issue_date', models.DateField(blank=True, null=True, verbose_name=b'Ausgestellt am')),
                ('booking_date', models.DateField(blank=True, null=True, verbose_name=b'Eingebucht am')),
                ('cancelled_date', models.DateField(blank=True, null=True, verbose_name=b'Gek\xc3\xbcndigt am')),
                ('termination_date', models.DateField(blank=True, null=True, verbose_name=b'Gek\xc3\xbcndigt auf')),
                ('payback_date', models.DateField(blank=True, null=True, verbose_name=b'Zur\xc3\xbcckbezahlt am')),
                ('number', models.IntegerField(blank=True, null=True, verbose_name=b'Anteilschein Nummer')),
                ('notes', models.TextField(blank=True, default=b'', max_length=1000, verbose_name=b'Notizen')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='juntagrico.Member')),
            ],
            options={
                'verbose_name': 'Anteilschein',
                'verbose_name_plural': 'Anteilscheine',
            },
            bases=('juntagrico.billable',),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('billable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='juntagrico.Billable')),
                ('size', models.PositiveIntegerField(default=1)),
                ('future_size', models.PositiveIntegerField(default=1, verbose_name=b'Zukuenftige Groesse')),
                ('active', models.BooleanField(default=False)),
                ('activation_date', models.DateField(blank=True, null=True, verbose_name=b'Aktivierungssdatum')),
                ('deactivation_date', models.DateField(blank=True, null=True, verbose_name=b'Deaktivierungssdatum')),
                ('creation_date', models.DateField(auto_now_add=True, null=True, verbose_name=b'Erstellungsdatum')),
                ('start_date', models.DateField(default=juntagrico.util.temporal.start_of_next_year, verbose_name=b'Gew\xc3\xbcnschtes Startdatum')),
            ],
            options={
                'verbose_name': 'Abo',
                'verbose_name_plural': 'Abos',
                'permissions': (('can_filter_subscriptions', 'Benutzer kann Abos filtern'),),
            },
            bases=('juntagrico.billable',),
        ),
        migrations.AddField(
            model_name='job',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_juntagrico.job_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='depot',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='billable',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_juntagrico.billable_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='bill',
            name='billable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bills', to='juntagrico.Billable'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juntagrico.Job'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='activityarea',
            name='coordinator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='activityarea',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='areas', to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='depot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscription_set', to='juntagrico.Depot'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='future_depot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='future_subscription_set', to='juntagrico.Depot'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='primary_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subscription_primary', to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='onetimejob',
            name='activityarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='juntagrico.ActivityArea'),
        ),
        migrations.AddField(
            model_name='member',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='juntagrico.Subscription'),
        ),
        migrations.AddField(
            model_name='extrasubscription',
            name='main_subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='extra_subscription_set', to='juntagrico.Subscription'),
        ),
        migrations.AddField(
            model_name='extrasubscription',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='extra_subscriptions', to='juntagrico.ExtraSubscriptionType'),
        ),
    ]
