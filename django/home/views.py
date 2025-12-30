from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login/")
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect(index)
    else:     
        form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect(login_view)

