from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import authenticate, login, logout

from .models import Module, Survey, Type

MODULE_CODE_TO_TEXT = {
	'moo': 'Módulo de Optimización Operacional', 
	'msc': 'Módulo de Sostenibilidad Corporativa',
	'mpc': 'Módulo de Productividad Comercial',
	'mve': 'Módulo de Visión y Ejecución',
	'mfe': 'Módulo de Finanzas Estratéticas',
	'mcp': 'Módulo de Control de Presupuesto',
	'moc': 'Módulo de Optimización de Costos',
}

AVAILABLE_TYPES = [ 'comercial', 'servicios', 'industrial' ]

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

def survey(request, module: str, type: str):
	"""
	The survey view. (Block 3)
	Requires the module you are evaluating in and the bussiness type.
	"""
	if request.method == 'POST':
		return HttpResponseRedirect(reverse('cme:graph', kwargs={
			'module': module,
			'type': type
		}))

	# Validate module
	try:
		module = module.lower()
		module_name = MODULE_CODE_TO_TEXT[module.lower()]
	except KeyError:
		raise Http404('Página no encontrada.')

	# Validate type
	type_text = type = type.lower()
	if type_text not in AVAILABLE_TYPES:
		raise Http404('Página no encontrada.')

	# Get the Module and Type
	module = Module.objects.get(code=module)
	type = Type.objects.get(type=type)

	# Get survey
	survey = Survey.objects.get(module=module, type=type)
	
	return render(request, 'cme/survey.html', {
		'module_name': module_name,
		'type': type_text.capitalize(),
		'survey': survey,
	})

def graph(request: WSGIRequest, module: str, type: str):
	"""
	The graph view. (Block 4)
	Only will allow if you where redirected.
	"""
	return render(request, 'cme/graph.html', { 
		'survey': Survey.objects.get(
			module=Module.objects.get(code=module),
			type=Type.objects.get(type=type)
		) 
	})

# Log in and out views here
def login(request: WSGIRequest):
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
		else:
			return render(request, 'cme/login.html', {
				'message': 'Email o contraseña inválidos'
			})
	
	# User just entered the page
	elif request.method == 'GET':
		return render(request, 'cme/login.html')

	# Bad request
	else:
		return HttpResponseBadRequest()

def logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('cme:index'))
