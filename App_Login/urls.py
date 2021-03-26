from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('profile/', views.profile_page, name='profile_page'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('other_profile/<str:username>/', views.other_profile, name='other_profile'),
    path('follow/<str:username>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('change_password/', views.change_password, name='change_password'),

    path('password_reset/',
    auth_views.PasswordResetView.as_view(template_name='App_Login/password_reset.html'),
    name='password_reset'),

    path('password_reset/done/',
    auth_views.PasswordResetDoneView.as_view(template_name='App_Login/password_reset_done.html'),
    name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name='App_Login/password_reset_confirm.html'),
    name='password_reset_confirm'),

    path('password_reset_complete/',
    auth_views.PasswordResetCompleteView.as_view(template_name='App_Login/password_reset_complete.html'),
    name='password_reset_complete')
]
