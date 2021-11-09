from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
		return f'{self.module} - {self.type.type.capitalize()}'

	def get_score(self):
		"""
		Will get the final score for the survey, collecting the
		punctuation from all the `Blocks`
		"""
		score = 0
		for block in self.blocks.all():
			score += block.get_score()

		return score


class Block(models.Model):
	"""
	This will group 5 questions, and then it will go to `Survey`.
	It will have a `name`, representing the category for the 5 questions,
	and the `survey` it belongs to.
	Get score will get the score of the 5 questions.
	"""
	survey = models.ForeignKey(Survey, models.PROTECT, related_name='blocks')
	name = models.CharField(max_length=300)

	def __str__(self) -> str:
		return f'{self.name}\n{self.survey}'

	def get_score(self):
		""" Get the score of the 5 questions. """
		score = 0
		for question in self.questions.all():
			score = question.score

		return score


class YesOrNo(models.IntegerChoices):
	"""
	Represent the posible answers with the punctuation.
	"""
	YES = 4, 'Si'
	NO = 0, 'No'
	UNDEFINED = -1, 'Indefinido'


class Question(models.Model):
	"""
	This model represents a question. It will have the question
	itself and a ForeignKey to a `Block`.
	Each question will have a yes or no answer. If the user
	answers yes, `score` will be equal to 4. Else, `score` will
	be equal to 0.
	"""
	block = models.ForeignKey(Block, models.PROTECT, related_name='questions')
	text = models.CharField(max_length=400, unique=True)
	score = models.SmallIntegerField(default=YesOrNo.UNDEFINED, choices=YesOrNo.choices)

	def __str__(self) -> str:
		return f'{self.text}'


# class Bussines(AbstractBaseUser, PermissionsMixin):
# 	"""
# 	This model is a custom user model that represent a bussiness
# 	"""
# 	email = models.EmailField(unique=True)
# 	first = models.CharField(max_length=150)
# 	last = models.CharField(max_length=150)
# 	is_staff = models.BooleanField(default=False)
# 	is_active = models.BooleanField(default=True) # TODO: make it false.
