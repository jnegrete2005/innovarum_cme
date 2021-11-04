from django.urls import path

from . import views

app_name = 'cme'
urlpatterns = [
  path('', views.index, name='index')
]