from django.urls import path
from . import views

urlpatterns = [
    path("", views.configure, name="configure"),
    path("register", views.register_user, name="register"),
    path("items", views.item_modify, name="item modify"),
    path("permissions", views.user_modify, name="user modify")
]