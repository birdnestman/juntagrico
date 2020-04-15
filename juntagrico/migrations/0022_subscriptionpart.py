# Generated by Django 3.0.5 on 2020-04-14 20:18

from django.db import migrations, models
import django.db.models.deletion
import juntagrico.entity


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0021_auto_20200414_2150'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_date', models.DateField(blank=True, null=True, verbose_name='Aktivierungssdatum')),
                ('cancellation_date', models.DateField(blank=True, null=True, verbose_name='Kündigüngssdatum')),
                ('deactivation_date', models.DateField(blank=True, null=True, verbose_name='Deaktivierungssdatum')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parts', to='juntagrico.Subscription', verbose_name='Abo')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='juntagrico.SubscriptionType', verbose_name='Abo-Typ')),
            ],
            options={
                'verbose_name': 'Abo Bestandteil',
                'verbose_name_plural': 'Abo Bestandteile',
            },
            bases=(models.Model, juntagrico.entity.OldHolder),
        ),
    ]
