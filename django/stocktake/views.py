from django.shortcuts import render, redirect
from .models import Stocktake, StocktakeItem
from .forms import StocktakeItemsFormSet, SalesForm
from .services import get_stocktake, update_stock, update_state, get_date
from home.models import UniqueItem
from django.db.utils import IntegrityError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

@login_required(login_url="/home/login/")
def stocktake(request):
    groups = ["Staff", "Manager", "Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    return render(request, 'stocktake/stocktake.html')


@login_required(login_url="/home/login/")
def stocktake_view(request, slug):
    groups = ["Staff", "Manager", "Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    stocktake = get_object_or_404(Stocktake, slug=slug)
    items = StocktakeItem.objects.filter(stocktake=stocktake)
    return render(request, "stocktake/view.html", {"stocktake": stocktake, "items": items},)


@login_required(login_url="/home/login/")
def entry(request):
    groups = ["Staff", "Manager", "Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    request.session.modified = True
    stocktake = get_stocktake(str(request.user))
    items = UniqueItem.objects.all()
    try:
        for item in items:
            StocktakeItem.objects.get_or_create(
            name=item.name,
            stocktake=stocktake,
            item=item
            )
    except IntegrityError as i:
        print(i)
        return render(request, 'stocktake/alreadycomp.html')

    queryset = StocktakeItem.objects.filter(stocktake=stocktake).order_by("id")

    paginator = Paginator(queryset, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    formset = StocktakeItemsFormSet(queryset=page_obj.object_list)
    sales = SalesForm(instance=stocktake)

    if request.method == "POST":
        formset = StocktakeItemsFormSet(request.POST, queryset=page_obj.object_list)
        sales = SalesForm(request.POST, instance=stocktake)
        instances = formset.save(commit=False)
        for obj in instances:
            if obj.counted is None:
                obj.counted = 0
            obj.save()
        if 'final' in request.POST:
            if formset.is_valid() and sales.is_valid():
                stocktake.status = 'Submitted'
                stocktake.user = str(request.user)
                stocktake.completed_at = timezone.now()
                for obj in queryset:
                     if obj.counted is None:
                          obj.counted = 0
                          obj.save()
                stocktake.save()
                sales.save()
                formset.save()
                update_stock(queryset)
                return render(request, 'stocktake/complete.html')
        if 'save' in request.POST:
                stocktake.user = str(request.user)
                stocktake.save()
                sales.save()
                formset.save()
                return redirect('stocktake') 
        if 'next' in request.POST and page_obj.has_next():
                stocktake.save()
                sales.save()
                formset.save()
                return redirect(f"{request.path}?page={page_obj.next_page_number()}")
        if 'prev' in request.POST and page_obj.has_previous():
                stocktake.save()
                sales.save()
                formset.save()
                return redirect(f"{request.path}?page={page_obj.previous_page_number()}")
        return redirect(f"{request.path}?page={page_number}")

    return render(request, "stocktake/entry.html", {
        "formset": formset, "stocktake": stocktake, "sales": sales, "page_obj": page_obj
    })
    

@login_required(login_url="/home/login/")
def history(request):
    update_state(get_date())
    stocktakes = Stocktake.objects.all().order_by('-date')
    context = {
        'stocktakes': stocktakes
    }
    return render(request, "stocktake/history.html", context)