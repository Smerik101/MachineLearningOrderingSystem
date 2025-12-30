from django.shortcuts import render
from .models import Stocktake, StocktakeItem
from .forms import StocktakeItemsFormSet, SalesForm
from .services import get_stocktake, update_stock
from home.models import UniqueItem
from django.db.utils import IntegrityError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/home/login/")
def stocktake(request):
    return render(request, 'stocktake/stocktake.html')


@login_required(login_url="/home/login/")
def stocktake_view(request, slug):
    stocktake = get_object_or_404(Stocktake, slug=slug)
    items = StocktakeItem.objects.filter(stocktake=stocktake)
    return render(request, "stocktake/view.html", {"stocktake": stocktake, "items": items},)


@login_required(login_url="/home/login/")
def entry(request):
    stocktake = get_stocktake()
    items = UniqueItem.objects.all()
    try:
        for item in items:
            StocktakeItem.objects.get_or_create(
            name=item.name,
            stocktake=stocktake,
            item=item
            )
    except IntegrityError:
        return render(request, 'stocktake/alreadycomp.html')

    queryset = StocktakeItem.objects.filter(stocktake=stocktake)

    if request.method == "POST":
        formset = StocktakeItemsFormSet(request.POST, queryset=queryset)
        sales = SalesForm(request.POST, instance=stocktake)
        if formset.is_valid() and sales.is_valid:
            stocktake.status = 'Submitted'
            stocktake.user = str(request.user)
            stocktake.completed_at = timezone.now()
            stocktake.save()
            sales.save()
            formset.save()
            update_stock(queryset)
            return render(request, 'stocktake/complete.html')
    else:
        formset = StocktakeItemsFormSet(queryset=queryset)
        sales = SalesForm(instance=stocktake)

    return render(request, "stocktake/entry.html", {
        "formset": formset, "stocktake": stocktake, "sales": sales
    })
    

@login_required(login_url="/home/login/")
def history(request):
    stocktakes = Stocktake.objects.all().order_by('-date')
    context = {
        'stocktakes': stocktakes
    }
    return render(request, "stocktake/history.html", context)