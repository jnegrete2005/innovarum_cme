from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'legacy'
urlpatterns = [
    path('', views.index, name='index'),

    # User URLs
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
]
