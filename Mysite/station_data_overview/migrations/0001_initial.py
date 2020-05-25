# Generated by Django 2.2.12 on 2020-04-30 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OnlyStationInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station', models.CharField(blank=True, max_length=20, null=True)),
                ('owner', models.CharField(blank=True, max_length=20, null=True)),
                ('operator', models.TextField(blank=True, null=True)),
                ('ad_manger', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('acos', models.TextField(blank=True, null=True)),
                ('ad_sales', models.FloatField(blank=True, null=True)),
                ('percentage', models.TextField(blank=True, null=True)),
                ('accept_time', models.DateField(blank=True, null=True)),
                ('operator_time', models.CharField(blank=True, max_length=20, null=True)),
                ('update_time', models.CharField(blank=True, max_length=30, null=True)),
                ('shop_sales', models.FloatField(blank=True, null=True)),
                ('cpc', models.FloatField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('give_other_time', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'only_station_info',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StationSalesOverall',
            fields=[
                ('station', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('account', models.CharField(blank=True, max_length=255, null=True)),
                ('site', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField()),
                ('ad_spend', models.FloatField(blank=True, null=True)),
                ('ad_sales', models.FloatField(blank=True, null=True)),
                ('acos', models.CharField(blank=True, max_length=255, null=True)),
                ('shop_sales', models.FloatField(blank=True, null=True)),
                ('spend_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('sale_rate', models.CharField(blank=True, max_length=255, null=True)),
                ('update_datetime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'station_sales_overall',
                'managed': False,
            },
        ),
    ]
