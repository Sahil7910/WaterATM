from django.urls import path
from Site import views

urlpatterns = [
    path('add_site', views.add_site, name='add_site'),
    path('list_sites', views.list_sites, name='list_sites'),
    path('delete-site/<int:site_id>/', views.delete_site, name='delete_site'),

]