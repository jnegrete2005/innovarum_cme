import requests
import json
import os

from django.shortcuts import redirect, render
from requests.api import head

# Create your views here.


def index(request):
  """
  Will return index.html
  """
  if request.method == 'GET':
    return render(request, 'presupuestos/index.html')


def get_db(request):
  """
  Will call to Notion API to get the info
  """

  url = f'https://api.notion.com/v1/databases/{os.environ.get("NOTION_DATABASE_ID")}/query'

  headers = {
      'Authorization': f'Bearer {os.environ.get("NOTION_KEY")}',
      'Content-Type': 'application/json',
      'Notion-Version': '2021-08-16'
  }

  data = {
      'sorts': [
          {
              'property': 'title',
              'direction': 'ascending',
          }
      ]
  }

  response = requests.post(url, json=data, headers=headers)
  print(response.text)

  return redirect('presupuestos:index')
