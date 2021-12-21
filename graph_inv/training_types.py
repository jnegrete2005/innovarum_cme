from graphene_django import DjangoObjectType

from training.models import Course, Module, File, UserFile


class TrainingCourseType(DjangoObjectType):
  class Meta:
    model = Course
    fields = '__all__'


class TrainingModuleType(DjangoObjectType):
  class Meta:
    model = Module
    fields = '__all__'


class FileType(DjangoObjectType):
  class Meta:
    model = File
    fields = '__all__'


class UserFileType(DjangoObjectType):
  class Meta:
    model = UserFile
    fields = '__all__'
