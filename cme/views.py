from django.http.response import Http404
from django.shortcuts import render

MODULE_CODE_TO_TEXT = {
	'moo': 'Módulo de Optimización Operacional', 
	'msc': 'Módulo de Sostenibilidad Corporativa',
	'mpc': 'Módulo de Productividad Comercial',
	'mve': 'Módulo de Visión y Ejecución',
	'mfe': 'Módulo de Finanzas Estratéticas',
	'mcp': 'Módulo de Control de Presupuesto',
	'moc': 'Módulo de Optimización de Costos',
}

AVAILABLE_TYPES = [ 'comercial', 'servicios', 'industria' ]

# Create your views here.
def index(request):
	""" Index view (block 1) """
	return render(request, 'cme/index.html')

def company_picker(request, module: str):
	""" View to pick which type of company you belong to. (block 2) """
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
	The survey view. 
	Requires the module you are evaluating in and the bussiness type.
	"""
	# Validate module
	try:
		module_name = MODULE_CODE_TO_TEXT[module.lower()]
	except KeyError:
		raise Http404('Página no encontrada.')

	# Validate type
	type = type.lower()
	if type not in AVAILABLE_TYPES:
		raise Http404('Página no encontrada.')

	
	return render(request, 'cme/survey.html', {
		'module_name': module_name,
		'type': type.capitalize()
	})
