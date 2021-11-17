from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'cme'
urlpatterns = [
    path('', login_required(views.index), name='index'),
    path('terminar/', login_required(views.thanks), name='thanks'),
    path('<str:module>/', login_required(views.company_picker), name='picker'),
    path('<str:module>/<str:s_type>/', login_required(views.survey), name='survey'),
    path('<str:module>/<str:s_type>/graph/', login_required(views.graph), name='graph'),

    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', login_required(views.register), name='register')
]
