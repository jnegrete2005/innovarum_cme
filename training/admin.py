from django.contrib.admin import ModelAdmin, register
from .models import Course, Module, File, UserFile

# Register your models here.


@register(Course)
class CourseAdmin(ModelAdmin):
  list_display = ['name', 'img']


@register(Module)
class ModuleAdmin(ModelAdmin):
  list_display = ['name', 'course']


@register(File)
class FileAdmin(ModelAdmin):
  list_display = ['name', 'url', 'module']


@register(UserFile)
class UserFileAdmin(ModelAdmin):
  list_display = ['file', 'user', 'done']
