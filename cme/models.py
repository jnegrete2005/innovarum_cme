from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class Module(models.Model):
	"""
	One row represents one of the seven available modules.
	"""
	name = models.CharField(max_length=50, unique=True)
	code = models.CharField(max_length=3, unique=True)
	# description = models.CharField(max_length=200)

	def __str__(self) -> str:
		return self.name 


class Type(models.Model):
	"""
	One row represents one of the 3 types of available businesses.
	"""
	type = models.CharField(max_length=10)

	def __str__(self) -> str:
		return self.type


class Survey(models.Model):
	"""
	This model represent a survey.
	Each survey will have a module and a type to filter each.
	Each survey will also have questions and answers, with a
	final score.
	"""
	module = models.ForeignKey(Module, models.PROTECT, related_name='surveys')
	type = models.ForeignKey(Type, models.PROTECT, related_name='surveys')

	def __str__(self) -> str:
		return f'Encuesta a {self.module}, del tipo {self.type}'

	# TODO: Calculate final score
	def get_score(self):
		"""
		Will get the final score for the survey, collecting the
		punctuation from all the `Questions`
		"""
		score = 0
		for question in self.questions.all():
			score += question.score

		return score


class YesOrNo(models.IntegerChoices):
	"""
	Represent the posible answers with the punctuation.
	"""
	YES = 4, 'Si'
	NO = 0, 'No'


class Question(models.Model):
	"""
	This model represents a question. It will have the question
	itself and a ForeignKey to a `Survey`.
	Each question will have a yes or no answer. If the user
	answers yes, `score` will be equal to 4. Else, `score` will
	be equal to 0.
	"""
	survey = models.ForeignKey(Survey, models.PROTECT, related_name='questions')
	text = models.CharField(max_length=400, unique=True)
	score = models.PositiveSmallIntegerField(default=YesOrNo.NO, choices=YesOrNo.choices)

	def __str__(self) -> str:
		return f'Pregunta: {self.text}\nPuntuación: {self.score}\n{self.survey}'


# TODO
# Create Bussines and BussineScore models 
