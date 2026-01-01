from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home import models
from .forms import ItemsForm, UserFormSet

# Create your views here.

@login_required(login_url="/home/login/")
def configure(request):
    groups = ["Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    return render(request, 'configure/configure.html')


@login_required(login_url="/home/login/")
def register_user(request):
    groups = ["Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("configure")
    else:
        form = UserCreationForm()
        
    return render(request, "configure/register.html", {"form": form})


@login_required(login_url="/home/login/")
def item_modify(request):
    groups = ["Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    unique_items = models.UniqueItem.objects.all()
    if request.method == "POST":
        if "add" in request.POST:
            models.UniqueItem.objects.create(name="", buffer=0, stock=0)
            return redirect("item modify")
        elif "delete" in request.POST:
            pk = request.POST.get('delete')
            models.UniqueItem.objects.filter(pk=pk).delete()
            return redirect("item modify")
        else:
            formset = ItemsForm(request.POST, queryset=unique_items)
            if formset.is_valid():
                formset.save()
                return redirect("configure")
    else:
        formset = ItemsForm(queryset=unique_items)
    return render(request, 'configure/items.html', {'formset': formset})


@login_required(login_url="/home/login/")
def user_modify(request):
    groups = ["Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    formset = UserFormSet
    if request.method == "POST":
        formset = UserFormSet(request.POST, queryset=User.objects.all())   
        if formset.is_valid():
            formset.save()
            return redirect('configure')
    else:
        formset = UserFormSet(queryset=User.objects.all())
    return render(request, 'configure/permissions.html', {'formset': formset})
