from datetime import timedelta
from .models import Stocktake
from django.utils import timezone
import holidays


def update_state(date):
    stocktakes = Stocktake.objects.filter(status = 'Open')
    stocktakes = stocktakes.exclude(date = date)
    if stocktakes != None:
        for obj in stocktakes:
            obj.status = "Not submitted"
            obj.save()


def get_info():
    au_holidays = holidays.Australia(state='ACT', years=2025)
    date = timezone.now().date() - timedelta(days=1)
    dow = date.weekday()
    pubhol = 0
    if date in au_holidays:
        pubhol = 1
    schhol = 0 #Find school holiday APK
    return date, dow, pubhol, schhol


def update_stock(queryset):
    for obj in queryset:
        item = obj.item 
        obj.usage = item.stock - obj.counted
        item.stock = obj.counted
        item.save()
        obj.save()


def get_stocktake():
    date, dow, pubhol, schhol = get_info()
    update_state(date)
    check_stocktake = Stocktake.objects.filter(date=date)
    if check_stocktake.exists():
        if check_stocktake.filter(status = 'Open').exists():
            return check_stocktake.get() 
        return None
    stocktake = Stocktake.objects.create(
                           date=date,
                           user="erik", 
                           status="Open", 
                           created_at=timezone.now(), 
                           completed_at=None, 
                           sales=0, 
                           dayofweek=dow, 
                           publicholiday=pubhol, 
                           schoolholiday=schhol,
                           slug=str(date))  
    stocktake.save()
    return stocktake

