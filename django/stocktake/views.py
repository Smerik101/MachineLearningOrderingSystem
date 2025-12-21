from django.shortcuts import render, redirect
from .models import Stocktake, StocktakeItem
from .forms import StocktakeItemsFormSet
from .services import get_stocktake
from home.models import UniqueItems
from django.db.utils import IntegrityError

# Create your views here.


def stocktake(request):
    return render(request, 'stocktake/stocktake.html')


def entry(request):
    stocktake = get_stocktake()
    items = UniqueItems.objects.all()
    try:
        for item in items:
            StocktakeItem.objects.get_or_create(
            name=item.name,
            stocktake=stocktake
            )
    except IntegrityError:
        return render(request, 'stocktake/alreadycomp.html')

    queryset = StocktakeItem.objects.filter(stocktake=stocktake)

    if request.method == "POST":
        formset = StocktakeItemsFormSet(request.POST, queryset=queryset)
        stocktake.status = 'closed'
        stocktake.save()
        if formset.is_valid():
            formset.save()
            return render(request, 'stocktake/complete.html')
    else:
        formset = StocktakeItemsFormSet(queryset=queryset)

    return render(request, "stocktake/entry.html", {
        "formset": formset, "stocktake": stocktake
    })
    

def history(request):
    stocktakes = Stocktake.objects.all().order_by('-date')
    return render(request, "stocktake/history.html"), {'stocktakes': stocktakes}