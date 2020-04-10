# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-10 08:39


import re

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import juntagrico.util.temporal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityArea',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('description', models.TextField(default='',
                                                 max_length=1000, verbose_name='Beschreibung')),
                ('core', models.BooleanField(
                    default=False, verbose_name='Kernbereich')),
                ('hidden', models.BooleanField(
                    default=False, verbose_name='versteckt')),
                ('show_coordinator_phonenumber', models.BooleanField(
                    default=False, verbose_name='Koordinator Tel Nr Veröffentlichen')),
            ],
            options={
                'verbose_name': 'Tätigkeitsbereich',
                'verbose_name_plural': 'Tätigkeitsbereiche',
                'permissions': (('is_area_admin', 'Benutzer ist TätigkeitsbereichskoordinatorIn'),),
            },
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('core_cache', models.BooleanField(
                    default=False, verbose_name='Kernbereich')),
            ],
            options={
                'verbose_name': 'Mitglied',
                'verbose_name_plural': 'Arbeitseinsätze',
            },
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False, verbose_name='bezahlt')),
                ('bill_date', models.DateField(blank=True,
                                               null=True, verbose_name='Aktivierungssdatum')),
                ('ref_number', models.CharField(max_length=30,
                                                unique=True, verbose_name='Referenznummer')),
                ('amount', models.FloatField(verbose_name='Betrag')),
            ],
            options={
                'verbose_name': 'Rechnung',
                'verbose_name_plural': 'Rechnungen',
            },
        ),
        migrations.CreateModel(
            name='Billable',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Verrechenbare Einheit',
                'verbose_name_plural': 'Verrechenbare Einhaiten',
            },
        ),
        migrations.CreateModel(
            name='Depot',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator(re.compile(
                    '^[-a-zA-Z0-9_]+\\Z', 32), "Enter a valid 'slug' consisting of letters, numbers, underscores or hyphens.", 'invalid')], verbose_name='Code')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Depot Name')),
                ('weekday', models.PositiveIntegerField(choices=[(1, 'Montag'), (2, 'Dienstag'), (3, 'Mittwoch'), (
                    4, 'Donnerstag'), (5, 'Freitag'), (6, 'Samstag'), (7, 'Sonntag')], verbose_name='Wochentag')),
                ('latitude', models.CharField(default='',
                                              max_length=100, verbose_name='Latitude')),
                ('longitude', models.CharField(default='',
                                               max_length=100, verbose_name='Longitude')),
                ('addr_street', models.CharField(
                    max_length=100, verbose_name='Strasse')),
                ('addr_zipcode', models.CharField(
                    max_length=10, verbose_name='PLZ')),
                ('addr_location', models.CharField(
                    max_length=50, verbose_name='Ort')),
                ('description', models.TextField(default='',
                                                 max_length=1000, verbose_name='Beschreibung')),
            ],
            options={
                'verbose_name': 'Depot',
                'verbose_name_plural': 'Depots',
                'permissions': (('is_depot_admin', 'Benutzer ist Depot Admin'),),
            },
        ),
        migrations.CreateModel(
            name='ExtraSubBillingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='Preis')),
                ('start_day', models.PositiveIntegerField(verbose_name='Start Tag')),
                ('start_month', models.PositiveIntegerField(choices=[(1, 'Januar'), (2, 'Februar'), (3, 'März'), (4, 'April'), (5, 'Mai'), (6, 'Juni'), (
                    7, 'Juli'), (8, 'August'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Dezember')], verbose_name='Start Monat')),
                ('end_day', models.PositiveIntegerField(verbose_name='End Tag')),
                ('end_month', models.PositiveIntegerField(choices=[(1, 'Januar'), (2, 'Februar'), (3, 'März'), (4, 'April'), (5, 'Mai'), (6, 'Juni'), (
                    7, 'Juli'), (8, 'August'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'Dezember')], verbose_name='End Monat')),
                ('code', models.TextField(default='', max_length=1000,
                                          verbose_name='Code für Teilabrechnung')),
            ],
            options={
                'verbose_name': 'Verechnungsperdiode Zusatzabos',
                'verbose_name_plural': 'Verechnungsperdioden Zusatzabos',
            },
        ),
        migrations.CreateModel(
            name='ExtraSubscriptionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True,
                                                 max_length=1000, verbose_name='Beschreibung')),
                ('sort_order', models.FloatField(
                    default=1.0, verbose_name='Nummer zum Sortieren')),
            ],
            options={
                'verbose_name': 'Zusatz-Abo-Kategorie',
                'verbose_name_plural': 'Zusatz-Abo-Kategorien',
            },
        ),
        migrations.CreateModel(
            name='ExtraSubscriptionType',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('size', models.CharField(default='', max_length=100,
                                          verbose_name='Groesse (gross,4, ...)')),
                ('description', models.TextField(
                    max_length=1000, verbose_name='Beschreibung')),
                ('sort_order', models.FloatField(
                    default=1.0, verbose_name='Groesse zum Sortieren')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                               related_name='category', to='juntagrico.ExtraSubscriptionCategory')),
            ],
            options={
                'verbose_name': 'Zusatz-Abo-Typ',
                'verbose_name_plural': 'Zusatz-Abo-Typen',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('slots', models.PositiveIntegerField(verbose_name='Plaetze')),
                ('time', models.DateTimeField()),
                ('pinned', models.BooleanField(default=False)),
                ('reminder_sent', models.BooleanField(
                    default=False, verbose_name='Reminder verschickt')),
                ('canceled', models.BooleanField(
                    default=False, verbose_name='abgesagt')),
            ],
            options={
                'verbose_name': 'AbstractJob',
                'verbose_name_plural': 'AbstractJobs',
            },
        ),
        migrations.CreateModel(
            name='JobExtra',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('per_member', models.BooleanField(default=False,
                                                   verbose_name='jeder kann Extra auswählen')),
            ],
            options={
                'verbose_name': 'JobExtra',
                'verbose_name_plural': 'JobExtras',
            },
        ),
        migrations.CreateModel(
            name='JobExtraType',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('display_empty', models.CharField(max_length=1000,
                                                   verbose_name='Icon für felhlendes Extra')),
                ('display_full', models.CharField(
                    max_length=1000, verbose_name='Icon für Extra')),
            ],
            options={
                'verbose_name': 'JobExtraTyp',
                'verbose_name_plural': 'JobExtraTypen',
            },
        ),
        migrations.CreateModel(
            name='JobType',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('displayed_name', models.CharField(blank=True,
                                                    max_length=100, null=True, verbose_name='Angezeigter Name')),
                ('description', models.TextField(default='',
                                                 max_length=1000, verbose_name='Beschreibung')),
                ('duration', models.PositiveIntegerField(
                    verbose_name='Dauer in Stunden')),
                ('location', models.CharField(
                    default='', max_length=100, verbose_name='Ort')),
                ('activityarea', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='juntagrico.ActivityArea')),
            ],
            options={
                'verbose_name': 'Jobart',
                'verbose_name_plural': 'Jobarten',
            },
        ),
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('template', models.TextField(default='',
                                              max_length=1000, verbose_name='Template')),
                ('code', models.TextField(default='',
                                          max_length=1000, verbose_name='Code')),
            ],
            options={
                'verbose_name': 'MailTemplate',
                'verbose_name_plural': 'MailTemplates',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(
                    max_length=30, verbose_name='Vorname')),
                ('last_name', models.CharField(
                    max_length=30, verbose_name='Nachname')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('addr_street', models.CharField(
                    max_length=100, verbose_name='Strasse')),
                ('addr_zipcode', models.CharField(
                    max_length=10, verbose_name='PLZ')),
                ('addr_location', models.CharField(
                    max_length=50, verbose_name='Ort')),
                ('birthday', models.DateField(blank=True,
                                              null=True, verbose_name='Geburtsdatum')),
                ('phone', models.CharField(max_length=50, verbose_name='Telefonnr')),
                ('mobile_phone', models.CharField(blank=True,
                                                  max_length=50, null=True, verbose_name='Mobile')),
                ('confirmed', models.BooleanField(
                    default=False, verbose_name='bestätigt')),
                ('reachable_by_email', models.BooleanField(default=False,
                                                           verbose_name='Kontaktierbar von der Job Seite aus')),
                ('block_emails', models.BooleanField(
                    default=False, verbose_name='keine emails')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                              related_name='member', to=settings.AUTH_USER_MODEL)),
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
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_date', models.DateField(blank=True,
                                               null=True, verbose_name='Bezahldatum')),
                ('amount', models.FloatField(verbose_name='Betrag')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                           related_name='payments', to='juntagrico.Bill')),
            ],
            options={
                'verbose_name': 'Zahlung',
                'verbose_name_plural': 'Zahlung',
            },
        ),
        migrations.CreateModel(
            name='SpecialRoles',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'), ('can_send_mails', 'Benutzer kann im System Emails versenden'), ('can_use_general_email', 'Benutzer kann General Email Adresse verwenden')),
            },
        ),
        migrations.CreateModel(
            name='SubscriptionSize',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('long_name', models.CharField(max_length=100,
                                               unique=True, verbose_name='Langer Name')),
                ('size', models.PositiveIntegerField(
                    unique=True, verbose_name='Grösse')),
                ('shares', models.PositiveIntegerField(
                    verbose_name='Anz benötigter Anteilsscheine')),
                ('required_assignments', models.PositiveIntegerField(
                    verbose_name='Anz benötigter Arbeitseinsätze')),
                ('price', models.PositiveIntegerField(verbose_name='Preis')),
                ('depot_list', models.BooleanField(
                    default=True, verbose_name='Sichtbar auf Depotliste')),
                ('description', models.TextField(blank=True,
                                                 max_length=1000, verbose_name='Beschreibung')),
            ],
            options={
                'verbose_name': 'Abo Grösse',
                'verbose_name_plural': 'Abo Grössen',
            },
        ),
        migrations.CreateModel(
            name='ExtraSubscription',
            fields=[
                ('billable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                      parent_link=True, primary_key=True, serialize=False, to='juntagrico.Billable')),
                ('active', models.BooleanField(default=False)),
                ('canceled', models.BooleanField(
                    default=False, verbose_name='gekündigt')),
                ('activation_date', models.DateField(blank=True,
                                                     null=True, verbose_name='Aktivierungssdatum')),
                ('deactivation_date', models.DateField(blank=True,
                                                       null=True, verbose_name='Deaktivierungssdatum')),
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
                ('job_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                 parent_link=True, primary_key=True, serialize=False, to='juntagrico.Job')),
                ('name', models.CharField(max_length=100,
                                          unique=True, verbose_name='Name')),
                ('displayed_name', models.CharField(blank=True,
                                                    max_length=100, null=True, verbose_name='Angezeigter Name')),
                ('description', models.TextField(default='',
                                                 max_length=1000, verbose_name='Beschreibung')),
                ('duration', models.PositiveIntegerField(
                    verbose_name='Dauer in Stunden')),
                ('location', models.CharField(
                    default='', max_length=100, verbose_name='Ort')),
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
                ('job_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                 parent_link=True, primary_key=True, serialize=False, to='juntagrico.Job')),
                ('type', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT, to='juntagrico.JobType')),
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
                ('billable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                      parent_link=True, primary_key=True, serialize=False, to='juntagrico.Billable')),
                ('paid_date', models.DateField(blank=True,
                                               null=True, verbose_name='Bezahlt am')),
                ('issue_date', models.DateField(blank=True,
                                                null=True, verbose_name='Ausgestellt am')),
                ('booking_date', models.DateField(blank=True,
                                                  null=True, verbose_name='Eingebucht am')),
                ('cancelled_date', models.DateField(
                    blank=True, null=True, verbose_name='Gekündigt am')),
                ('termination_date', models.DateField(
                    blank=True, null=True, verbose_name='Gekündigt auf')),
                ('payback_date', models.DateField(blank=True,
                                                  null=True, verbose_name='Zurückbezahlt am')),
                ('number', models.IntegerField(blank=True,
                                               null=True, verbose_name='Anteilschein Nummer')),
                ('notes', models.TextField(blank=True, default='',
                                           max_length=1000, verbose_name='Notizen')),
                ('member', models.ForeignKey(blank=True, null=True,
                                             on_delete=django.db.models.deletion.SET_NULL, to='juntagrico.Member')),
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
                ('billable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE,
                                                      parent_link=True, primary_key=True, serialize=False, to='juntagrico.Billable')),
                ('size', models.PositiveIntegerField(default=1)),
                ('future_size', models.PositiveIntegerField(
                    default=1, verbose_name='Zukuenftige Groesse')),
                ('active', models.BooleanField(default=False)),
                ('activation_date', models.DateField(blank=True,
                                                     null=True, verbose_name='Aktivierungssdatum')),
                ('deactivation_date', models.DateField(blank=True,
                                                       null=True, verbose_name='Deaktivierungssdatum')),
                ('creation_date', models.DateField(auto_now_add=True,
                                                   null=True, verbose_name='Erstellungsdatum')),
                ('start_date', models.DateField(
                    default=juntagrico.util.temporal.start_of_next_business_year, verbose_name='Gewünschtes Startdatum')),
            ],
            options={
                'verbose_name': 'Abo',
                'verbose_name_plural': 'Abos',
                'permissions': (('can_filter_subscriptions', 'Benutzer kann Abos filtern'),),
            },
            bases=('juntagrico.billable',),
        ),
        migrations.AddField(
            model_name='jobextra',
            name='extra_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='job_types_set', to='juntagrico.JobExtraType'),
        ),
        migrations.AddField(
            model_name='jobextra',
            name='recuring_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='job_extras_set', to='juntagrico.JobType'),
        ),
        migrations.AddField(
            model_name='job',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='polymorphic_juntagrico.job_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='extrasubbillingperiod',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='periods', to='juntagrico.ExtraSubscriptionType'),
        ),
        migrations.AddField(
            model_name='depot',
            name='contact',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='billable',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='polymorphic_juntagrico.billable_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='bill',
            name='billable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='bills', to='juntagrico.Billable'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='job',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='juntagrico.Job'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='job_extras',
            field=models.ManyToManyField(
                blank=True, related_name='assignments', to='juntagrico.JobExtra'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='member',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='activityarea',
            name='coordinator',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='activityarea',
            name='members',
            field=models.ManyToManyField(
                blank=True, related_name='areas', to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='depot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='subscription_set', to='juntagrico.Depot'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='future_depot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='future_subscription_set', to='juntagrico.Depot'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='primary_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='subscription_primary', to='juntagrico.Member'),
        ),
        migrations.AddField(
            model_name='onetimejob',
            name='activityarea',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='juntagrico.ActivityArea'),
        ),
        migrations.AddField(
            model_name='member',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='members', to='juntagrico.Subscription'),
        ),
        migrations.AddField(
            model_name='jobextra',
            name='onetime_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='job_extras_set', to='juntagrico.OneTimeJob'),
        ),
        migrations.AddField(
            model_name='extrasubscription',
            name='main_subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='extra_subscription_set', to='juntagrico.Subscription'),
        ),
        migrations.AddField(
            model_name='extrasubscription',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                    related_name='extra_subscriptions', to='juntagrico.ExtraSubscriptionType'),
        ),
    ]
