from django.urls import path
from Reader import views

urlpatterns = [
    path('add_reader', views.add_reader, name='add_reader'),
    path('list_reader', views.list_reader, name='list_reader'),
    path('add_config', views.add_config, name='add_config'),
    path('list_config', views.list_config, name='list_config'),
    path('keep-live', views.keep_live, name='keep_live'),

]