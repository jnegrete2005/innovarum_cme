from graphene_django import DjangoObjectType, DjangoListField

from legacy.models import Course, Module, Quiz, UserQuiz, Question, Answer, Trio, UserTrio
from cme.models import Bussines


class CourseType(DjangoObjectType):
  class Meta:
    model = Course
    fields = '__all__'


class ModuleType(DjangoObjectType):
  class Meta:
    model = Module
    fields = '__all__'


class QuizType(DjangoObjectType):
  class Meta:
    model = Quiz
    fields = '__all__'


class UserQuizType(DjangoObjectType):
  class Meta:
    model = UserQuiz
    fields = '__all__'


class QuestionType(DjangoObjectType):
  class Meta:
    model = Question
    fields = '__all__'


class AnswerType(DjangoObjectType):
  class Meta:
    model = Answer
    fields = '__all__'


class UserTrioType(DjangoObjectType):
  class Meta:
    model = UserTrio
    fields = '__all__'


class TrioType(DjangoObjectType):
  class Meta:
    model = Trio
    fields = '__all__'


class BusinessType(DjangoObjectType):
  class Meta:
    model = Bussines
    fields = '__all__'
