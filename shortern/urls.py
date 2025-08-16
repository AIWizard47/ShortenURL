# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<str:code>", views.goto, name="goto"),
]
