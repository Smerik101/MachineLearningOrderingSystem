from django.contrib import admin
from .models import StocktakeItem, Stocktake

# Register your models here.
admin.site.register(Stocktake)
admin.site.register(StocktakeItem)