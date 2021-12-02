from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.db import IntegrityError
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_safe


# Create your views here.
@require_safe
def index(request: WSGIRequest):
  """
  Index view for Legacy App
  """
  return render(request, 'legacy/index.html')


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


@require_http_methods(['GET', 'POST'])
def register_view(request: WSGIRequest):
  """ View to register """
  if request.method == 'POST':
    email = str(request.POST.get('email', None)).strip()
    first = str(request.POST.get('first', None)).strip()
    last = str(request.POST.get('last', None)).strip()
    role = str(request.POST.get('role', None)).strip()
    password = str(request.POST.get('password', None)).strip()

    if not validate_fields(email, first, last, role, password):
      return render(request, 'legacy/register.html', {'message': 'No has llenado uno de los campos.'})

    # Attempt to create user
    try:
      User = get_user_model()
      user = User.objects.create_user(email, first, last, role, password, cme_access=True, is_superuser=False, is_staff=False)
    except IntegrityError:
      return render(request, 'legacy/register.html', {'message': 'Ese mail ya ha sido usado.'})

    login(request, user)
    return redirect('legacy:index')

  else:
    return render(request, 'legacy/register.html')


def validate_fields(**fields) -> bool:
  """
  Function to validate fields.
  Will return false if any of the fields are 'None' or empty.
  """
  for field in fields:
    if field == 'None' or field == '':
      return False

  return True
