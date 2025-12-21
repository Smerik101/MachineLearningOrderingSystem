from django.shortcuts import render

# Create your views here.

def ordering(request):
    return render(request, 'ordering/ordering.html')