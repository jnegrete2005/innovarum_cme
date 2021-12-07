from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'legacy'
urlpatterns = [
    path('', views.index, name='index'),

    # Create URLs
    path('crear/', staff_member_required(views.create_view), name='create'),
    path('crear/quiz/', views.create_quiz, name='create_quiz'),

    # User URLs
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
]
