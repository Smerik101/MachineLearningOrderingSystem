from datetime import datetime, date, timedelta
from .models import Stocktake


def get_stocktake():
    check_stocktake = Stocktake.objects.filter(date = date.today() - timedelta(days=1))
    if check_stocktake.exists():
        if check_stocktake.filter(status = 'open').exists():
            return check_stocktake.get() 
        return None
    stocktake = Stocktake.objects.create(
                           date=date.today() - timedelta(days=1),
                           user="erik", 
                           status="open", 
                           created_at=datetime.now(), 
                           completed_at=None, 
                           sales=0, 
                           dayofweek=0, 
                           publicholiday=0, 
                           schoolholiday=0,
                           slug="1234"  )
    stocktake.save()
    return stocktake

