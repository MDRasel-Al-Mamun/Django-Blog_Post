from django.urls import path
from .import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profileUpdate, name='update'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('favourite/<int:id>/', views.favourite, name='favourite'),
    path('profile/favourite/', views.favourite_list, name='favourite_list'),
    path('like/', views.like, name='like'),
    path('thumbs/', views.thumbs, name='thumbs'),
]
