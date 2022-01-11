from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'legacy'
urlpatterns = [
    path('', login_required(views.index, login_url='legacy:login'), name='index'),
    # path('quiz/<int:id>/', login_required(views.quiz_view), name='take_quiz'),

    # Create URLs
    path('crear/', staff_member_required(views.create_view, login_url='legacy:login'), name='create'),
    path('crear/quiz/', staff_member_required(views.create_quiz, login_url='legacy:login'), name='create_quiz'),
    path('crear/curso/', staff_member_required(views.create_course, login_url='legacy:login'), name='create_course'),

    # User URLs
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('solicitar/', views.ask, name='ask'),
]
