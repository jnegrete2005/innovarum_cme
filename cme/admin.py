from django.contrib import admin

from .models import Module, Type, Survey, Question

# Register your models here.
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'code']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
	list_display = ['id', 'type']

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
	list_display = ['id', 'module', 'type']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ['id', 'survey', 'text', 'score']
