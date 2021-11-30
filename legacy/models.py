from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.db.models.fields.related import ForeignKey


# Create your models here.


class Course(models.Model):
  """
  Represents a Course for Legacy.

  It's contents will be stored in `Module`s
  """
  name = models.CharField(max_length=200, unique=True)
  img = models.ImageField()

  def __str__(self) -> str:
    return f'{self.name}'


class Module(models.Model):
  """
  Represents a Module for a course.

  Module's contents will be stored in `Trio`s
  """
  index = models.PositiveSmallIntegerField(unique=True)
  course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='modules')

  def __str__(self) -> str:
    return f'Módulo {self.index}'


class Quiz(models.Model):
  """
  Represents a Quiz for a `Module`.

  It will have a `name`
  """
  name = models.CharField(max_length=200)
  user = models.ManyToManyField('cme.Bussines', related_name='quizes', through='UserQuiz', through_fields=('quiz', 'user'))

  def __str__(self) -> str:
    return f'{self.name}'


class UserQuiz(models.Model):
  """
  Represents the results for the `Quiz`

  It has the `user`, the `quiz`, and the `results`.

  `results` will be an array of array of numbers. Each array will be a question,
  and the numbers inside will represent the questions. The answered question will
  be represented with a 1, the rest will be 0's.
  """

  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='users')
  user = models.ForeignKey('cme.Bussines', on_delete=models.CASCADE, related_name='presupuestos_quizes')
  score = models.ManyToManyField('Answer', related_name='answered')

  class Meta:
    verbose_name_plural = 'UserQuizes'


class Question(models.Model):
  """
  Represents a question for the quiz.
  """
  name = models.CharField(max_length=200)
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
  """
  It will represent an answer for a question. One will be correct
  """
  name = models.CharField(max_length=200)
  is_correct = models.BooleanField(default=False)
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


class Trio(models.Model):
  """
  Represents the content for a Module.  

  Each `Trio` will have, as it's name says, 3 content fields, plus the
  `Module` it belongs to.

  It will have a `file`, a `video` (which will be a URL to a YT video), and a `quiz`
  (which will be key to `Quiz`)
  """
  file = models.FileField(upload_to='legacy/classes/', max_length=254)
  quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, related_name='trios', null=True)
  video = models.URLField()
  module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='trios')
  user = models.ManyToManyField('cme.Bussines', related_name='trios', through='UserTrio', through_fields=('trio', 'user'))


class UserTrio(models.Model):
  """
  ManyToMany with `User` and `Trio` intermediary.
  `user` is FK to `Bussines`  
  `trio` is FK to `Trio`
  `done` is an Array of booleans of size 3 to determine the `trio`s that are done
  """
  trio = models.ForeignKey(Trio, on_delete=models.CASCADE)
  user = models.ForeignKey('cme.Bussines', on_delete=models.CASCADE)
  done = ArrayField(models.BooleanField(default=False), size=3)
