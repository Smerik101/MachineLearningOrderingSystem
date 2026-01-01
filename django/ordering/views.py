from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url="/home/login/")
def ordering(request):
    groups = ["Manager", "Admin"]
    if not request.user.groups.filter(name__in=groups).exists():
        return render(request, 'access_denied.html')
    return render(request, 'ordering/ordering.html')