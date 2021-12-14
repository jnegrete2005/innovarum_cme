from ..types import CourseType, Course, BusinessType, Bussines, UserTrio, Trio
from graphene_django import DjangoListField

import graphene
from graphql import GraphQLError


class Query(graphene.ObjectType):
  courses = DjangoListField(CourseType, option=graphene.String(), id=graphene.ID(required=False))
  course = graphene.Field(CourseType, id=graphene.ID())
  user = graphene.Field(BusinessType, id=graphene.ID())

  def resolve_courses(root, info, option, id=None):
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
      trios = u.trios.all()
      modules = list(set(map(lambda trio: trio.module, trios)))
      courses = list(set(map(lambda module: module.course, modules)))

      for course in courses:
        course_trios = map(lambda module: module.trios.all(), course.modules.all())

        # Iterate through the trios in the course
        for trios in course_trios:
          for trio in trios:
            print(trio.usertrio_set.first().done)
            if trio.usertrio_set.first().done != [True, True, True] and trio.usertrio_set.first().done != [False, False, False]:
              course_list.append(course)
              continue

      return course_list

    if option == 'done':
      """ Query to get the courses done by the user """
      u = Bussines.objects.get(id=id)

      course_list = []
      trios = u.trios.all()
      modules = list(set(map(lambda trio: trio.module, trios)))
      courses = list(set(map(lambda module: module.course, modules)))

      for course in courses:
        course_length = sum(map(lambda module: module.trios.all().count(), course.modules.all()))
        course_trios = map(lambda module: module.trios.all(), course.modules.all())
        current = 0

        # Iterate through the trios in the course
        for trios in course_trios:
          for trio in trios:
            if trio.usertrio_set.first().done == [True, True, True]:
              current += 1

        if current == course_length:
          course_list.append(course)

      return course_list

  def resolve_course(root, info, id):
    """ Query for getting specific course """
    return Course.objects.get(pk=id)

  def resolve_user(root, info, id):
    """ Query for getting a user """
    return Bussines.objects.get(pk=id)
