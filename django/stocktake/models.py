from django.db import models
from django.utils import timezone

# Create your models here.
class Stocktake(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    user = models.CharField(max_length=10)
    status = models.CharField(default="open", max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    sales = models.FloatField(default=0)
    dayofweek = models.IntegerField(default=0)
    publicholiday = models.BooleanField(default=0)
    schoolholiday = models.BooleanField(default=0)
    slug = models.SlugField(default="", null=True)


class StocktakeItem(models.Model):
    name = models.CharField(max_length=20)
    stocktake = models.ForeignKey(to=Stocktake, on_delete=models.CASCADE, default=None)
    counted = models.IntegerField(default=None, null=True)
    usage = models.IntegerField(default=0)
    endstock = models.IntegerField(default=0)

