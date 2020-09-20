from .import views
from django.urls import path

urlpatterns = [
    path('', views.blogPosts, name='blog'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.searchAuto, name='search_auto'),
    path('<str:id>/<slug:slug>', views.blogDetails, name='blog_details'),
    path('category/<slug:slug>/', views.category, name="category"),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
]
