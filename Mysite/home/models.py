from django.db import models

# Create your models here.


class StationSalesOverall(models.Model):
    station = models.CharField(max_length=255, blank=True, null=True)
    account = models.CharField(max_length=255, blank=True, null=True)
    site = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
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
