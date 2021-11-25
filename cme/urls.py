from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from . import views

LOGIN_URL = 'cme:login'

app_name = 'cme'
urlpatterns = [
    path('', views.capture, name='capture'),
    path('cme/', login_required(views.index, login_url=LOGIN_URL), name='index'),
    path('terminar/', login_required(views.thanks, login_url=LOGIN_URL), name='thanks'),
    path('crear-encuesta/', staff_member_required(views.create_survey, login_url=LOGIN_URL), name='create_survey'),
    path('<str:module>/', login_required(views.company_picker, login_url=LOGIN_URL), name='picker'),
    path('<str:module>/<str:s_type>/', login_required(views.survey, login_url=LOGIN_URL), name='survey'),
    path('<str:module>/<str:s_type>/graph/', login_required(views.graph, login_url=LOGIN_URL), name='graph'),

    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', staff_member_required(views.register, login_url=LOGIN_URL), name='register')
]
