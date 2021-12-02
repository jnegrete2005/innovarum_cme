from django.contrib.admin import ModelAdmin, register
from .models import Course, Module, Quiz, Question, Answer, Trio, UserQuiz, UserTrio

# Register your models here.


@register(Course)
class CourseAdmin(ModelAdmin):
  list_display = ['name', 'img']


@register(Module)
class ModuleAdmin(ModelAdmin):
  list_display = ['index', 'course']


@register(Quiz)
class QuizAdmin(ModelAdmin):
  list_display = ['name']


@register(UserQuiz)
class UserQuizAdmin(ModelAdmin):
  list_display = ['user', 'quiz']


@register(Question)
class QuestionAdmin(ModelAdmin):
  list_display = ['name', 'quiz']


@register(Answer)
class AnswerAdmin(ModelAdmin):
  list_display = ['name', 'is_correct', 'question']


@register(Trio)
class TrioAdmin(ModelAdmin):
  list_display = ['id', 'file', 'quiz', 'video', 'module']


@register(UserTrio)
class UserTrioAdmin(ModelAdmin):
  list_display = ['trio', 'user', 'done']
