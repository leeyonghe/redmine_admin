from django.urls import path
from . import views

app_name = 'redmine'

urlpatterns = [
    path('', views.index, name='index'),
] 