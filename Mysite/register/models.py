from django.db import models

# Create your models here.


class Userlogin(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255, blank=True, null=True)
    realname = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'userlogin'

