from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('send-password-change-email/', views.EmailView.as_view(), name='password-change-email'),
    path('reset_password/<uid>/<token>/', views.UserPasswordResetView.as_view(), name='password reset'),
]