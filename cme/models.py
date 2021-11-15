from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.postgres.fields import ArrayField

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
	Each survey will also have questions and answers.
	"""
	module = models.ForeignKey(Module, models.PROTECT, related_name='surveys')
	type = models.ForeignKey(Type, models.PROTECT, related_name='surveys')

	def __str__(self) -> str:
		return f'{self.module} - {self.type.type.capitalize()}'


class Block(models.Model):
	"""
	This will group 5 questions, and then it will go to `Survey`.
	It will have a `name`, representing the category for the 5 questions,
	and the `survey` it belongs to.
	"""
	survey = models.ForeignKey(Survey, models.PROTECT, related_name='blocks')
	name = models.CharField(max_length=300)

	def __str__(self) -> str:
		return f'{self.name}'


class Question(models.Model):
	"""
	This model represents a question. It will have the question
	itself and a ForeignKey to a `Block`.
	Each question will have a yes or no answer. If the user
	answers yes, `score` will be equal to 4. Else, `score` will
	be equal to 0.
	"""
	block = models.ForeignKey(Block, models.PROTECT, related_name='questions')
	text = models.CharField(max_length=400)

	def __str__(self) -> str:
		return f'{self.text}'


# Side B
class CustomAccountManager(BaseUserManager):
	def create_user(self, email, first, last, role, password, **other_fields):
		if not email:
			raise ValueError('You must provide an email address')

		user: Bussines = self.model(
			email=self.normalize_email(email),
			first=first,
			last=last,
			role=role,
			**other_fields
		)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_superuser(self, email, first, last, role, password, **other_fields):
		other_fields.setdefault('is_superuser', True)
		other_fields.setdefault('is_staff', True)
		other_fields.setdefault('is_active', True)

		if other_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must be assigned to is_superuser=True.')
		if other_fields.get('is_staff') is not True:
			raise ValueError('Superuser must be assigned to is_staff=True.')
		if other_fields.get('is_active') is not True:
			raise ValueError('Superuser must be assigned to is_active=True.')

		return self.create_user(email, first, last, role, password, **other_fields)


class Bussines(AbstractBaseUser, PermissionsMixin):
	"""
	This model is a custom user model that represent a bussiness
	"""
	email = models.EmailField(unique=True)
	first = models.CharField(max_length=150)
	last = models.CharField(max_length=150)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	role = models.CharField(max_length=300)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first', 'last', 'role']

	objects = CustomAccountManager()

	def __str__(self) -> str:
		return self.first + ' ' + self.last


class Score(models.Model):
	"""
	This will represent a score for a user
	"""
	score = ArrayField(models.PositiveSmallIntegerField())
	bussines = models.ForeignKey(Bussines, on_delete=models.CASCADE, related_name='scores')
	survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='scores')
	date: datetime = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return str(self.score)

	def get_score(self) -> int:
		return sum(self.score)
