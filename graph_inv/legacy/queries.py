from ..types import CourseType, Course, BusinessType, Bussines

import graphene
from graphene_django import DjangoListField


class Query(graphene.ObjectType):
  courses = DjangoListField(CourseType)
  course = graphene.Field(CourseType, id=graphene.ID())
  user = graphene.Field(BusinessType, id=graphene.ID())

  def resolve_courses(root, info):
    """ Query for getting all courses """
    return Course.objects.all()

  def resolve_course(root, info, id):
    """ Query for getting specific course """
    return Course.objects.get(pk=id)

  def resolve_user(root, info, id):
    """ Query for getting a user """
    return Bussines.objects.get(pk=id)
