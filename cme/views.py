from datetime import datetime
import json
from typing import List
import copy

from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.db import IntegrityError
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Bussines, Module, Score, Survey, Type

MODULE_CODE_TO_TEXT = {
    'moo': 'Módulo de Optimización Operacional',
    'msc': 'Módulo de Sostenibilidad Corporativa',
    'mpc': 'Módulo de Productividad Comercial',
    'mve': 'Módulo de Visión y Ejecución',
    'mfe': 'Módulo de Finanzas Estratéticas',
    'mcp': 'Módulo de Control de Presupuesto',
    'moc': 'Módulo de Optimización de Costos',
}

AVAILABLE_TYPES = ['comercial', 'servicios', 'industrial']

# Create your views here.


def index(request):
  """ Index view (Block 1) """
  return render(request, 'cme/index.html')


def company_picker(request, module: str):
  """ View to pick which type of company you belong to. (Block 2) """
  try:
    module_name = MODULE_CODE_TO_TEXT[module.lower()]
  except KeyError:
    raise Http404('Página no encontrada.')

  return render(request, 'cme/picker.html', {
      'module_name': module_name,
      'module_code': module.lower(),
  })


def survey(request, module: str, s_type: str):
  """
  The survey view. (Block 3)
  Requires the module you are evaluating in and the bussiness type.
  """
  if request.method == 'POST':
    return HttpResponseRedirect(reverse('cme:graph', kwargs={
        'module': module,
        'type': s_type
    }))

  # Validate module
  try:
    module = module.lower()
    module_name = MODULE_CODE_TO_TEXT[module.lower()]
  except KeyError:
    raise Http404('Página no encontrada.')

  # Validate type
  type_text = s_type = s_type.lower()
  if type_text not in AVAILABLE_TYPES:
    raise Http404('Página no encontrada.')

  # Get the Module and Type
  module = Module.objects.get(code=module)
  s_type = Type.objects.get(type=s_type)

  # Get survey
  survey = Survey.objects.get(module=module, type=s_type)

  return render(request, 'cme/survey.html', {
      'module_name': module_name,
      'type': type_text.capitalize(),
      'survey': survey,
  })


def graph(request: WSGIRequest, module: str, s_type: str):
  """
  The graph view. (Block 4)
  Only will allow if you where redirected.
  """
  # Validate module
  try:
    module = module.lower()
    MODULE_CODE_TO_TEXT[module.lower()]
  except KeyError:
    raise Http404('Página no encontrada.')

  # Validate type
  type_text = s_type = s_type.lower()
  if type_text not in AVAILABLE_TYPES:
    raise Http404('Página no encontrada.')

  # Get the Module and Type
  module = Module.objects.get(code=module)
  s_type = Type.objects.get(type=s_type)

  # Get survey
  survey = Survey.objects.get(module=module, type=s_type)

  # Get user
  user = Bussines.objects.get(pk=request.user.id)

  # Get score
  if request.method == 'GET':
    score = Score.objects.filter(bussines=user, survey=survey)
    score = score[len(score) - 1]

  else:
    data = json.loads(request.body)
    # Get last score
    try:
      score = Score.objects.filter(bussines=user, survey=survey)
      score = score[len(score) - 1]

      if (((score.date - datetime.now().astimezone()).total_seconds() / 60 / 60 / 20) < 1):
        score.score = data.get('scores')
        score.save()
      else:
        score = Score.objects.create(bussines=user, survey=survey, score=data.get('scores'))

    except AssertionError or Score.DoesNotExist:
      score = Score.objects.create(bussines=user, survey=survey, score=data.get('scores'))

  if settings.DEBUG:
    score = Score.objects.first()

  blocks: List[str] = [block.name for block in survey.blocks.all()]

  blocks_for_graph = copy.copy(blocks)
  for i in range(len(blocks_for_graph)):
    blocks_for_graph[i] = blocks_for_graph[i].replace('de', '')
    blocks_for_graph[i] = blocks_for_graph[i].replace('por', '')
    blocks_for_graph[i] = blocks_for_graph[i].split()

  context = {
      'blocks': blocks,
      'scores': score.score,
      'overall': sum(score.score),
      'date': score.date.strftime('%d/%m/%Y'),
      'survey': str(survey),
      'blocks_for_graph': blocks_for_graph
  }

  if request.method == 'GET':
    return render(request, 'cme/graph.html', context)

  return JsonResponse(context, status=200)


def thanks(request: WSGIRequest):
  """
  The thanks view.
  Represents Block 5 and will return thanks.html
  """
  if request.method == 'GET':
    return render(request, 'cme/thanks.html')

  return HttpResponseBadRequest()


# Log in and out views here


def login_view(request: WSGIRequest):
  # User attempted to login
  if request.method == 'POST':
    # Attempt to sign user in
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)

    # Check if authentication is successful
    if user != None:
      login(request, user)
      return HttpResponseRedirect(reverse('cme:index'))

    return render(request, 'cme/login.html', {
        'message': 'Email o contraseña inválidos'
    })

  # User just entered the page
  elif request.method == 'GET':
    return render(request, 'cme/login.html')

  # Bad request
  return HttpResponseBadRequest()


def logout_view(request: WSGIRequest):
  logout(request)
  return HttpResponseRedirect(reverse('cme:index'))


def register(request: WSGIRequest):
  if request.method == 'POST':
    email = request.POST['email']
    first = request.POST['first']
    last = request.POST['last']
    role = request.POST['role']
    password = request.POST['password']
    is_staff = request.POST['is_staff'] == 'on'
    is_admin = request.POST['is_admin'] == 'on'

    # Attempt to create new user
    try:
      if is_admin:
        user = Bussines.objects.create_superuser(email, first, last, role, password, is_superuser=is_admin, is_staff=is_staff)
      else:
        user = Bussines.objects.create_user(email, first, last, role, password, is_superuser=is_admin, is_staff=is_staff)
    except IntegrityError:
      return render(request, 'cme/register.html', {'message': 'Ese mail ya ha sido usado.'})

    return HttpResponseRedirect(reverse('cme:index'))

  elif request.method == 'GET':
    return render(request, 'cme/register.html')
