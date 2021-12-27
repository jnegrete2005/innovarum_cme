from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'training'
urlpatterns = [
    path('', views.index, name='index'),

    # Create Course
    path('crear/', staff_member_required(views.create_view), name='create'),

    # User URLs
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    # path('register', views.register_view, name='register'),
]
