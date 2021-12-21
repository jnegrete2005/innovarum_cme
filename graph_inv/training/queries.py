from ..training_types import Course, TrainingCourseType
from ..legacy_types import Bussines, BusinessType
from graphene_django import DjangoListField

import graphene
from graphql import GraphQLError


class Query(graphene.ObjectType):
  training_courses = DjangoListField(TrainingCourseType, option=graphene.String(), id=graphene.ID(required=False))

  def resolve_training_courses(root, info, option, id=None):
    """ Query for getting all courses """
    # Always return all courses if option is all
    if option == 'all':
      return Course.objects.all()

    # If there is not ID, only allow all
    if not id and option != 'all':
      return GraphQLError('Inicia sesión para acceder a esta sección')

    if option == 'ongoing':
      """ Query to get the ongoing courses by the user """
      u = Bussines.objects.get(id=id)

      course_list = []
      files = u.trios.all()
      modules = list(set(map(lambda file: file.module, files)))
      courses = list(set(map(lambda module: module.course, modules)))

      for course in courses:
        course_length = sum(map(lambda module: module.files.all().count(), course.modules.all()))
        course_files = map(lambda module: module.files.all(), course.modules.all())
        current = 0

        # Iterate through the files in the course
        for files in course_files:
          for file in files:
            if file.userfile_set.filter(user=u)[0].done == True:
              current += 1

        if current != course_length and current > 0:
          course_list.append(course)

      return course_list

    if option == 'done':
      """ Query to get the courses done by the user """
      u = Bussines.objects.get(id=id)

      course_list = []
      files = u.trios.all()
      modules = list(set(map(lambda file: file.module, files)))
      courses = list(set(map(lambda module: module.course, modules)))

      for course in courses:
        course_length = sum(map(lambda module: module.files.all().count(), course.modules.all()))
        course_files = map(lambda module: module.files.all(), course.modules.all())
        current = 0

        # Iterate through the files in the course
        for files in course_files:
          for file in files:
            if file.userfile_set.filter(user=u)[0].done == True:
              current += 1

        if current == course_length:
          course_list.append(course)

      return course_list
