from datetime import datetime
from typing import List
import copy
import os
import json
from inspect import cleandoc
from secrets import token_hex

from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.db import IntegrityError
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Block, Bussines, Module, Question, Score, Survey, Type
from .send_mail import check_email, send_mail

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

NOT_ALLOWED = 'cme:not_allowed'


def can_enter_cme(user) -> bool:
  return user.cme_access

# Create your views here.


@user_passes_test(can_enter_cme, login_url=NOT_ALLOWED)
def index(request):
  """ Index view (Block 1) """
  return render(request, 'cme/index.html')


@user_passes_test(can_enter_cme, login_url=NOT_ALLOWED)
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


@user_passes_test(can_enter_cme, login_url='cme:login_view')
def survey(request, module: str, s_type: str):
  """
  The survey view. (Block 3)
  Requires the module you are evaluating in and the bussiness type.
  """
  if request.method == 'POST':
    return HttpResponseRedirect(reverse('cme:graph', kwargs={
        'module': module,
        's_type': s_type
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


@user_passes_test(can_enter_cme, login_url=NOT_ALLOWED)
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

      if (((datetime.now().astimezone() - score.date).total_seconds() / 60 / 60 / 20) < 1):
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
    blocks_for_graph[i] = blocks_for_graph[i].replace(' de', '')
    blocks_for_graph[i] = blocks_for_graph[i].replace(' por', '')
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


@user_passes_test(can_enter_cme, login_url=NOT_ALLOWED)
def thanks(request: WSGIRequest):
  """
  The thanks view (Block 5).
  Represents Block 5 and will return thanks.html
  """
  if request.method == 'GET':
    return render(request, 'cme/thanks.html')

  return HttpResponseBadRequest()


def capture(request: WSGIRequest):
  """
  The capture view (Block 6).
  On GET, will return an HTML with a form to capture
  info for potencial new users.
  On POST, it will collect that info and send it to
  Pablo via email.
  """
  if request.method == 'GET':
    if request.user.is_authenticated:
      return HttpResponseRedirect(reverse('cme:index'))

    return render(request, 'cme/capture.html')

  if request.method == 'POST':
    # Get info
    name = str(request.POST['first']).strip()
    last = str(request.POST['last']).strip()
    email = str(request.POST['email']).strip()
    role = str(request.POST['role']).strip()
    company = str(request.POST['company']).strip()

    # Validate email
    if not check_email(email):
      return render(request, 'cme/capture.html', {'msg': 'Email inválido.'}, status=422)

    msg = f"""\
    Buenos días/tardes.

    Una persona ha solicitado el folleto. Aquí envío los datos:
    Nombre: {name}
    Apellido: {last}
    Email: {email}
    Puesto de trabajo: {role}
    Compañía: {company}
    """

    send_mail(os.environ.get('PABLO_EMAIL'), cleandoc(msg), 'Información de usuario.')
    return render(request, 'cme/capture.html')


def create_survey(request: WSGIRequest):
  """
  View to create complete surveys more easily
  """
  if request.method == 'GET':
    return render(request, 'cme/create_survey.html', {
        'modules': [module.code for module in Module.objects.all()],
        'types': [s_type.type for s_type in Type.objects.all()]
    })

  elif request.method == 'POST':
    # Get type and module
    module = request.POST['module']
    module = Module.objects.get(code=module)

    s_type = request.POST['type']
    s_type = Type.objects.get(type=s_type)

    # Create Survey
    survey = Survey.objects.create(module=module, type=s_type)

    # Add blocks and questions
    blocks = request.POST.getlist('blocks', None)
    for i in range(len(blocks)):
      # Get and create block
      blocks[i] = blocks[i].strip()
      blocks[i] = Block.objects.create(survey=survey, name=blocks[i])

      # Get questions
      questions = request.POST.getlist(f'questions-{i}', None)
      for j in range(len(questions)):
        questions[j] = questions[j].strip()
        Question.objects.create(block=blocks[i], text=questions[j])

    return HttpResponseRedirect(reverse('cme:survey', kwargs={
        'module': module.code,
        's_type': s_type.type
    }))


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
      if user.cme_access:
        login(request, user)
        return HttpResponseRedirect(reverse('cme:index'))

      return render(request, 'cme/login.html', {
          'message': 'No tiene acceso a esta sección de la página.'
      })

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
    password = token_hex(3)
    is_staff = request.POST.get('is_staff', 'False') == 'True'
    is_admin = request.POST.get('is_admin', 'False') == 'True'

    # Attempt to create new user
    try:
      if is_admin:
        Bussines.objects.create_superuser(email, first, last, role, password, cme_access=True, is_superuser=is_admin, is_staff=is_staff)
      else:
        Bussines.objects.create_user(email, first, last, role, password, cme_access=True, is_superuser=is_admin, is_staff=is_staff)
    except IntegrityError:
      return render(request, 'cme/register.html', {'message': 'Ese mail ya ha sido usado.'})

    msg = f"""\
      Buenas.

      Hemos validado su solicitud para acceder al Coeficiente de Madurez Empresarial, y ha sido aprovada.
      Podrá entrar con los siguientes datos:
      Su email: {email}
      Contraseña segura asignada: {password}
      """
    send_mail(email, cleandoc(msg), 'Solicitud de acceso al CME aprovada.')

    return HttpResponseRedirect(reverse('cme:index'))

  elif request.method == 'GET':
    return render(request, 'cme/register.html')
