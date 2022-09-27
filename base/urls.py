from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("latest-news/", views.latest),
    path("filter-news/", views.filter_news),
    path("top-news", views.top_posts),
    path("search/", views.search),
    path("add-item/", views.add_item),
    path("view-comments/<int:id>", views.view_comments),
]