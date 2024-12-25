from django.urls import path
from Transaction import views

urlpatterns = [
    path('add_quota', views.add_quota, name='add_quota'),
    path('list_quota', views.list_quota, name='list_quota'),
    path('list_transaction', views.list_transaction, name='list_transaction'),


    ]