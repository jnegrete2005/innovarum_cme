from ..types import CourseType, Course

import graphene
from graphene_django import DjangoListField


class Query(graphene.ObjectType):
  courses = DjangoListField(CourseType)

  def resolve_courses(root, info):
    return Course.objects.all()
