from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'presupuestos'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('get/', login_required(views.get_db), name='getDb'),
]
