from django.urls import path
from Consumer import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_user', views.add_user, name='add_user'),
    path('list_user', views.list_user, name='list_user'),
    path('add_card', views.add_card, name='add_card'),
    path('list_card', views.list_card, name='list_card')
    ]