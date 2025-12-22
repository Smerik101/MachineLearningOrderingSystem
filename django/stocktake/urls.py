from django.urls import path
from . import views

urlpatterns = [
    path("", views.stocktake, name="stocktake"),
    path("entry", views.entry, name="stocktake entry"),
    path("history", views.history, name="stocktake history"),
    path("<slug:slug>", views.stocktake_view, name="stocktake view")
]