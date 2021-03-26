from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('post_create', views.post_create, name='post_create'),
    path('post_update/<int:pk>/', views.post_update, name='post_update'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('post_liked/<int:pk>/', views.post_liked, name='post_liked'),
    path('post_unliked/<int:pk>/', views.post_unliked, name='post_unliked'),
]