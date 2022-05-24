"""Urls de la app core."""

# Django
from django.urls import path

# Vistas
from core import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name="register"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('user/', views.UserAPIView.as_view(), name='user'),
    path('refresh/', views.RefreshAPIView.as_view(), name='refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('forgot/', views.ForgotAPIView.as_view(), name='forgot'),
    path('reset/', views.ResetAPIView.as_view(), name='reset')
]
