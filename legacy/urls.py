from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'legacy'
urlpatterns = [
    path('', views.index, name='index'),
    # path('quiz/<int:id>/', login_required(views.quiz_view), name='take_quiz'),

    # Create URLs
    path('crear/', staff_member_required(views.create_view), name='create'),
    path('crear/quiz/', views.create_quiz, name='create_quiz'),
    path('crear/curso/', views.create_course, name='create_course'),

    # User URLs
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
]
