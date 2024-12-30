from django.urls import path
from Consumer import views

urlpatterns = [
    path('home', views.home, name='home'),

    path('add_user', views.add_user, name='add_user'),
    path('list_user', views.list_user, name='list_user'),
    path('delete-consumer/<int:consumer_id>/', views.delete_consumer, name='delete_consumer'),
    path('add_card', views.add_card, name='add_card'),
    path('list_card', views.list_card, name='list_card'),
    path('member/authorize-transaction', views.authorize_transaction, name='authorize_transaction'),
    path('member/get_quota', views.get_quota, name='get_quota')
]