from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'legacy'
urlpatterns = [
    path('', login_required(views.index), name='index'),
]
