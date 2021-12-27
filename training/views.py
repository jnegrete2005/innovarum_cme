from .models import Course, Module, File

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.storage import default_storage
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_safe


# Create your views here.
@require_safe
def index(request: WSGIRequest):
  """
  Index view for Training App
  """
  return render(request, 'training/index.html')


@require_http_methods(['GET', 'POST'])
def create_view(request: WSGIRequest):
  """
  Will create a course.
  """
  if request.method == 'GET':
    return render(request, 'training/create_course.html')

  # Get course info
  course = request.POST.get('course').strip()
  course_img = request.POST.get('course_img').strip()

  # Create course
  final_course = Course.objects.create(name=course, img=course_img)

  # Get modules
  modules = request.POST.getlist('module', None)

  # Iterate through the modules
  for i, module in enumerate(modules):
    module = module.strip()
    module = Module.objects.create(name=module, course=final_course)

    # Get files with their types
    names = request.POST.getlist(f'name-{i + 1}')
    files = request.POST.getlist(f'file-{i + 1}')
    types = request.POST.getlist(f'type-{i + 1}')

    # Create files
    for j in range(len(files)):
      File.objects.create(name=names[j], url=files[j], file_type=int(types[j]), module=module)

  return redirect('training:index')

# User URLs


@require_http_methods(['GET', 'POST'])
def login_view(request: WSGIRequest):
  """ View to login in training """
  # User attempted to login
  if request.method == 'POST':
    # Attempt to sign user in
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)

    # Check if authentication is successful
    if user != None:
      login(request, user)
      return redirect('training:index')

    return render(request, 'training/login.html', {
        'message': 'Email o contraseña inválidos'
    })

  # User just entered the page
  else:
    return render(request, 'training/login.html')


@require_GET
def logout_view(request: WSGIRequest):
  """ View to logout in Training """
  logout(request)
  return redirect('training:index')


# @require_http_methods(['GET', 'POST'])
# def register_view(request: WSGIRequest):
#   """ View to register """
#   if request.method == 'POST':
#     email = str(request.POST.get('email', None)).strip()
#     first = str(request.POST.get('first', None)).strip()
#     last = str(request.POST.get('last', None)).strip()
#     role = str(request.POST.get('role', None)).strip()
#     password = str(request.POST.get('password', None)).strip()

#     if not validate_fields(email, first, last, role, password):
#       return render(request, 'training/register.html', {'message': 'No has llenado uno de los campos.'})

#     # Attempt to create user
#     try:
#       User = get_user_model()
#       user = User.objects.create_user(email, first, last, role, password, cme_access=True, is_superuser=False, is_staff=False)
#     except IntegrityError:
#       return render(request, 'training/register.html', {'message': 'Ese mail ya ha sido usado.'})

#     login(request, user)
#     return redirect('training:index')

#   else:
#     return render(request, 'training/register.html')


# def validate_fields(*fields) -> bool:
#   """
#   Function to validate fields.
#   Will return false if any of the fields are 'None' or empty.
#   """
#   for field in fields:
#     if field == 'None' or field == '':
#       return False

#   return True
