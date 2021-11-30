from typing import List, Tuple
from calendar import monthrange
from datetime import date

import requests
import json
import os
import csv
import mimetypes

from django.shortcuts import redirect, render
from django.http.response import HttpResponse

DAYS = {
    'Lunes': 0,
    'Martes': 1,
    'Miércoles': 2,
    'Jueves': 3,
    'Viernes': 4,
    'Sábado': 5,
    'Domingo': 6,
}

MONTHS = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12,
}


# Create your views here.


def index(request):
  """
  Will return index.html
  """
  if request.method == 'GET':
    return render(request, 'presupuestos/index.html')


def get_csv(request):
  """
  Will get the final csv.

  1. Will call the Notion table.
  2. Will filter the info.
  3. Will process the info.
  4. Will return the csv file.
  """
  # Call the Notion table
  response = get_info()

  # Get simplified version of the results
  tables = filter_info(response)

  # Get the name separated rows
  name_separated = name_separate(tables)

  # Get all the dates from all the names
  name_dates = dates_by_name(name_separated)

  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  filepath = BASE_DIR + '/presupuestos/presp.csv'

  write_to_csv(name_separated, name_dates, filepath)

  path = open(filepath, 'r')
  mime_type, _ = mimetypes.guess_type(filepath)
  request = HttpResponse(path, content_type=mime_type)

  # Return with download
  request['Content-Disposition'] = f'attachment; filename="presp.csv"'

  return request


def get_info():
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

  return response


def filter_info(response) -> list:
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


def name_separate(filtered_info: List[List]) -> List[List[List]]:
  """
  Will get the `filtered_info` and separate it through different names.
  Will return this.
  """
  current_name = ''
  current_row = []
  name_separated = []

  for row in filtered_info:
    # First iteration
    if current_name == '':
      # Set the current name
      current_name = row[0]

      current_row.append(row)
      continue

    if current_name == row[0]:
      current_row.append(row)

    else:
      # Append the finished current_row to the final name_sepated list
      name_separated.append(current_row)
      current_row = [row]
      current_name = row[0]

  name_separated.append(current_row)

  return name_separated


def dates_by_name(name_separated: List[List[List]]) -> List[List[List[Tuple[str, bool]]]]:
  """ Get the dates of all the names """
  group_dates = []
  row_dates = []
  name_dates = []

  for group in name_separated:
    row_dates = []

    for row in group:
      name_dates = []

      days: List[bool] = row[3:]
      for date in all_dates(MONTHS[row[1]]):
        name_dates.append((date.strftime('%d-%m-%Y'), days[date.weekday()]))

      row_dates.append(name_dates)

    group_dates.append(row_dates)

  return group_dates


def all_dates(month: int, year=date.today().year or int) -> List[date]:
  """
  Will return all the dates from a month
  """
  nb_days = monthrange(year, month)[1]

  return [date(year, month, day) for day in range(1, nb_days+1)]


def write_to_csv(name_separated: List[List[List]], name_dates: List[List[List[Tuple[str, bool]]]], path):
  """ Will get the `presp.csv` and write the data collected into it """

  # Header for the csv
  header = ['Nombre', 'Categoría 1', 'Categoría 2', 'Presupuesto', 'Fecha']

  costs = get_costs(name_separated, name_dates)
  data = get_rows(name_separated, name_dates, costs)

  data.reverse()

  # Open the file with 'w+' mode to truncate it
  with open(path, 'w+', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # Add the header
    writer.writerow(header)

    # Write the rows of the data
    writer.writerows(data)


def get_costs(name_separated: List[List[List]], name_dates: List[List[List[Tuple[str, bool]]]]) -> List[List[int]]:
  """ Will return the cost divided for each name """
  costs = []
  month_cost = []

  for i, name in enumerate(name_dates):
    month_cost = []
    for j, month in enumerate(name):
      cost_div = 0
      for day in month:
        if day[1]:
          cost_div += 1

      month_cost.append(round(name_separated[i][j][2] / cost_div, 2))

    costs.append(month_cost)

  return costs


def get_rows(names: List[List[List]], dates: List[List[List[Tuple[str, bool]]]], costs: List[List[int]]) -> List[List]:
  """
  Will get the rows for the CSV
  """

  rows = []

  for i, name in enumerate(dates):
    for j, month in enumerate(name):
      for date in month:
        rows.append([names[i][j][0], None, None, costs[i][j] if date[1] else 0, date[0]])

  return rows
