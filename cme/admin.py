from django.contrib import admin

from .models import Bussines, Module, Score, Type, Survey, Block, Question

# Register your models here.
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
	list_display = ['name', 'code']

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
	list_display = ['type']

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
	list_display = ['module', 'type']

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
	list_display = ['name', 'survey']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ['text', 'block']

@admin.register(Bussines)
class BussinesAdmin(admin.ModelAdmin):
	list_display = ['email', 'first', 'last', 'is_staff', 'is_superuser', 'role']

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
	list_display = ['score', 'bussines', 'survey', 'date']
