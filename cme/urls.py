from django.urls import path

from . import views

app_name = 'cme'
urlpatterns = [
  path('', views.index, name='index'),
	path('<str:module>/', views.company_picker, name='picker'),
	path('<str:module>/<str:type>', views.survey, name='survey'),
]