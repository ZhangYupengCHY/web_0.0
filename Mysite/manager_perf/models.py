from django.db import models

# Create your models here.


class StationSalesOverall(models.Model):
    station = models.CharField(primary_key=True, max_length=255)
    account = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    ad_spend = models.FloatField(blank=True, null=True)
    ad_sales = models.FloatField(blank=True, null=True)
    acos = models.FloatField(blank=True, null=True)
    shop_sales = models.FloatField(blank=True, null=True)
    spend_rate = models.FloatField(blank=True, null=True)
    sale_rate = models.FloatField(blank=True, null=True)
    update_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'station_sales_overall'
        unique_together = (('station', 'date'),)


class OnlyStationInfo(models.Model):
    station = models.CharField(max_length=20, blank=True, null=True)
    owner = models.CharField(max_length=20, blank=True, null=True)
    operator = models.TextField(blank=True, null=True)
    ad_manger = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    acos = models.TextField(blank=True, null=True)
    ad_sales = models.FloatField(blank=True, null=True)
    percentage = models.TextField(blank=True, null=True)
    accept_time = models.DateField(blank=True, null=True)
    operator_time = models.CharField(max_length=20, blank=True, null=True)
    update_time = models.CharField(max_length=30, blank=True, null=True)
    shop_sales = models.FloatField(blank=True, null=True)
    cpc = models.FloatField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    give_other_time = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'only_station_info'
