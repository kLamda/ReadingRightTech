from django.urls import path

from . import views

app_name = 'shopping'

urlpatterns = [
    path('index', views.view_list, name="index"),
    path('add', views.add_list, name='add'),
    path('update', views.update_list, name="update")
]