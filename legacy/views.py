from .send_mail import send_mail
from .models import Course, Module, Quiz, Question, Answer, Trio

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_safe
from django.contrib.auth.decorators import user_passes_test

from inspect import cleandoc
import os


NOT_ALLOWED = 'legacy:ask'


def can_enter_legacy(user) -> bool:
  return user.legacy_access

# Create your views here.


@user_passes_test(can_enter_legacy, login_url=NOT_ALLOWED)
@require_safe
def index(request: WSGIRequest):
  """
  Index view for Legacy App
  """
  return render(request, 'legacy/index.html')


@require_http_methods(['GET', 'POST'])
def quiz_view(request: WSGIRequest, id: int):
  """
  Will return a template to take the quiz.
  """
  if request.method == 'GET':
    return render(request, 'legacy/quiz.html', {'quiz': Quiz.objects.get(id=id)})


# Create URLs
@require_GET
def create_view(request: WSGIRequest):
  """
  Will return a template to choose what you want to create.

  It is not supposed to be used that much.
  """
  return render(request, 'legacy/create.html')


@require_http_methods(['GET', 'POST'])
def create_quiz(request: WSGIRequest):
  """
  Will create a quiz
  """
  if request.method == 'GET':
    return render(request, 'legacy/create_quiz.html')

  # Get and create quiz
  quiz = request.POST.get('quiz').strip()
  quiz = Quiz.objects.create(name=quiz)

  # Get questions
  questions = request.POST.getlist('question', None)

  # Iterate through questions
  for i, question in enumerate(questions):
    question = question.strip()
    question = Question.objects.create(name=question, quiz=quiz)

    # Get answers
    answers = list(map(lambda item: True if item == 'on' else item, request.POST.getlist(f'answer{i + 1}')))

    # Will represent if the current answer is new
    new_answer = True

    # Iterate through answers
    for i, answer in enumerate(answers):
      # Check if the element is a radio
      if answer == True:
        Answer.objects.create(name=answers[i + 1].strip(), is_correct=True, question=question)

        # Set next answer to not new
        new_answer = False

      # If element is not a radio
      if answer != True:
        # If it is an old answer, set new_answer to True for next iteration
        if new_answer == False:
          new_answer = True
          continue

        # If it is a new answer, create it
        else:
          Answer.objects.create(name=answer.strip(), is_correct=False, question=question)

  return redirect('legacy:create_quiz')


@require_http_methods(['GET', 'POST'])
def create_course(request: WSGIRequest):
  """
  Request:
  - POST: Will create a course
  - GET: Will return the template to create
  """
  if request.method == 'GET':
    return render(request, 'legacy/create_course.html')

  # Get course
  course = request.POST.get('course').strip()

  # Get the file for course
  course_img = request.POST.get('course-img')

  # Save course
  course = Course.objects.create(name=course, img=course_img)

  # Get the modules
  modules = request.POST.getlist('module', None)

  # Iterate through the modules
  for i, module in enumerate(modules):
    module = module.strip()
    module = Module.objects.create(index=i + 1, course=course)

    # Get trios
    files = request.POST.getlist(f'file-{i + 1}')
    fileUrls = request.POST.getlist(f'file-url-{i + 1}')
    videos = request.POST.getlist(f'video-{i + 1}')
    quizes = request.POST.getlist(f'quiz-{i + 1}')

    # Create a trio every 2 elements
    for j in range(len(files)):
      # Create the trio
      Trio.objects.create(file=files[j], file_url=fileUrls[j], quiz=quizes[j], video=videos[j], module=module)

  return redirect('legacy:index')


# User URLs
@require_http_methods(['GET', 'POST'])
def login_view(request: WSGIRequest):
  """ View to login in Legacy """
  # User attempted to login
  if request.method == 'POST':
    # Attempt to sign user in
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)

    # Check if authentication is successful
    if user != None:
      login(request, user)
      return redirect('legacy:index')

    return render(request, 'legacy/login.html', {
        'message': 'Email o contraseña inválidos'
    })

  # User just entered the page
  else:
    return render(request, 'legacy/login.html')


@require_GET
def logout_view(request: WSGIRequest):
  """ View to logout in Legacy """
  logout(request)
  return redirect('legacy:index')


@require_http_methods(['POST', 'GET'])
def ask(request: WSGIRequest):
  """ Ask permission to enter Legacy """
  if request.method == 'GET':
    return render(request, 'legacy/ask.html')

  email = str(request.POST.get('email', None)).strip()
  first = str(request.POST.get('first', None)).strip()
  last = str(request.POST.get('last', None)).strip()
  role = str(request.POST.get('role', None)).strip()
  company = str(request.POST.get('company', None)).strip()

  if not validate_fields(email, first, last, role, company):
    return render(request, 'legacy/ask.html', {'message': 'No has llenado uno de los campos.'})

  msg = f"""\
    Buenos días/tardes.

    Una persona ha solicitado acceso a Legacy. Aquí envío los datos:
    Nombre: {first}
    Apellido: {last}
    Email: {email}
    Puesto de trabajo: {role}
    Compañía: {company}
    """

  send_mail(os.environ.get('PABLO_EMAIL'), cleandoc(msg), 'Información de usuario.')
  return render(request, 'legacy/ask.html')


def validate_fields(*fields) -> bool:
  """
  Function to validate fields.
  Will return false if any of the fields are 'None' or empty.
  """
  for field in fields:
    if field == 'None' or field == '':
      return False

  return True
