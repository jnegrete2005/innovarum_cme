from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from . import views

app_name = 'cme'
urlpatterns = [
    path('', views.capture, name='capture'),
    path('cme/', login_required(views.index), name='index'),
    path('terminar/', login_required(views.thanks), name='thanks'),
    path('crear-encuesta/', staff_member_required(views.create_survey), name='create_survey'),
    path('<str:module>/', login_required(views.company_picker), name='picker'),
    path('<str:module>/<str:s_type>/', login_required(views.survey), name='survey'),
    path('<str:module>/<str:s_type>/graph/', login_required(views.graph), name='graph'),

    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', login_required(views.register), name='register')
]
