from django.urls import path
from . import views

urlpatterns = [
    path("latest-news/", views.latest)
]