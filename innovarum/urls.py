"""innovarum_cme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from graphene_django.views import GraphQLView


def admin_required(function=None):
  actual_decorator = user_passes_test(
      lambda u: u.is_superuser,
      login_url='/legacy/login',
      redirect_field_name=''
  )
  if function:
    return actual_decorator(function)
  return actual_decorator


urlpatterns = [
    path('', lambda request: redirect('cme:index', permanent=False)),
    path('admin/', admin.site.urls),
    path('cme/', include('cme.urls')),
    path('pres/', include('presupuestos.urls')),
    path('legacy/', include('legacy.urls')),
    path('graphql', GraphQLView.as_view(graphiql=False)),
    path('graphiql', admin_required(GraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
  urlpatterns += (
      static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
      static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  )
