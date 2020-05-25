from django.db import models

# Create your models here.


class Submit(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    submitter = models.CharField(max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    brief = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submit'
