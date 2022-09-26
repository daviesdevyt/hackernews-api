from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("search/", views.search),
    path("filter/", views.filter),
    path("latest/", views.latest),
]