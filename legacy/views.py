from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest


# Create your views here.
def index(request: WSGIRequest):
  """
  Index view for Legacy App
  """
  return render(request, 'legacy/index.html')
