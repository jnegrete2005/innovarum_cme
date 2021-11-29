from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'presupuestos'
urlpatterns = [
    path('', staff_member_required(views.index, login_url='cme:login'), name='index'),
    path('get/', staff_member_required(views.get_csv, login_url='cme:login'), name='getDb'),
]
