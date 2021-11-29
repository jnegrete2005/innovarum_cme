import requests
import json
import os
import csv
import mimetypes

from django.shortcuts import redirect, render
from requests.api import head
from django.http.response import HttpResponse

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

  # Query the db to get all the rows
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
  response = json.loads(requests.post(url, json=data, headers=headers).text)

  # Get simplified version of the results
  tables = get_info(response)

  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  filepath = BASE_DIR + '/presupuestos/presp.csv'

  write_to_csv(tables, filepath)

  path = open(filepath, 'r')
  mime_type, _ = mimetypes.guess_type(filepath)
  response = HttpResponse(path, content_type=mime_type)

  # Return with download
  response['Content-Disposition'] = f'attachment; filename="presp.csv"'

  return response


def get_info(response) -> list:
  """ Will get the info from the response of Notion table query in a simplified way """

  # Value to return
  final_results = []

  days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
  order = ['Name', 'Mes', 'Presupuesto'] + days

  # Iterate through every row of the table
  for result in response['results']:
    row = {}

    # Iterate through the properties of the row
    for property in result['properties']:

      # Add the value of the day
      if property in days:
        row[property] = result['properties'][property]['checkbox']

      # Add the name, month or presupuesto
      else:
        if property == 'Presupuesto':
          row[property] = result['properties'][property]['number']
          continue

        elif property == 'Mes':
          name = 'rich_text'

        else:
          name = 'title'

        row[property] = result['properties'][property][name][0]['text']['content']

    row = list(row.get(property) for property in order)

    # Append the simplified contents to the results
    final_results.append(row)

  return final_results


def write_to_csv(data: list, path):
  """ Will get the `presp.csv` and write the data collected into it """

  # Header for the csv
  header = ['Name', 'Mes', 'Presupuesto', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

  # Open the file with 'w+' mode to truncate it
  with open(path, 'w+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # Add the header
    writer.writerow(header)

    # Write the rows of the data
    writer.writerows(data)
