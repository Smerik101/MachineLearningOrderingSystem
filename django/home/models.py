from django.db import models
from django.utils import timezone


# Create your models here.

"""
class Initialize(models.Model):
    todays_date = models.DateField(default=timezone.now)
    todays_day = models.IntegerField()
    is_weekend = models.BooleanField()
    is_public_holiday = models.BooleanField()
    yesterday_date = models.DateField()
    yesterday_day = models.IntegerField()
    yesterday_is_weekend = models.BooleanField()
    yesterday_is_public_holiday = models.BooleanField()

    model_path = models.FilePathField(default='../models')
    pp_path = models.FilePathField(default='../preprocessed')

    state = models.JSONField(default=dict)
    current_stocktake = models.DateTimeField()
    last_stocktake = models.DateTimeField()


class Setting(models.Model):
    order_days = models.JSONField(default=list)
    delivery_delay = models.IntegerField()
    delivery_days = models.JSONField(default=list)
    order_for_days = models.JSONField(default=list)


class Product(models.Model):
    product = models.CharField()
    buffer = models.IntegerField(default=0)
    

class Admin(models.Model):
    feature_pref = models.JSONField(default=list)
"""

class UniqueItems(models.Model):
    name = models.CharField(max_length=20)
    buffer = models.IntegerField(default=0)