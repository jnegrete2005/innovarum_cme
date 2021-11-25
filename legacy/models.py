from django.db import models

# Create your models here.


class Course(models.Model):
  """
  Represents a Course for Legacy.
  It's contents will be stored in `Module`s
  """
  name = models.CharField(max_length=200, unique=True)

  def __str__(self) -> str:
    return f'{self.name}'


class Module(models.Model):
  """
  Represents a Module for a course.
  """
  index = models.PositiveSmallIntegerField(unique=True)
  course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='modules')

  def __str__(self) -> str:
    return f'Módulo {self.index}'


class LegacyUser(models.Model):
  """
  Represents a User for Legacy
  """
  base_user = models.OneToOneField('cme.Bussines', on_delete=models.CASCADE, related_name='legacy')
