from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import your custom views

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('goodbye/', views.goodbye, name='goodbye')
]

