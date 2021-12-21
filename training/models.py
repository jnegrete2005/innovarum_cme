from django.db import models


# Create your models here.
class Course(models.Model):
  """
  Represents a Course for Legacy.

  It's contents will be stored in `Module`s
  """
  name = models.CharField(max_length=200, unique=True)
  img = models.CharField(max_length=200, unique=True)

  def __str__(self) -> str:
    return self.name


class Module(models.Model):
  """
  Represents a Module for a course.

  It will have a name and a list of files.
  """
  name = models.CharField(max_length=200)
  course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='modules')

  def __str__(self) -> str:
    return self.name


class File(models.Model):
  """
  Represents a file url with the display name.
  """
  name = models.CharField(max_length=200)
  url = models.URLField(max_length=240)
  module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='files')
  user = models.ManyToManyField('cme.Bussines', related_name='files', through='UserFile', through_fields=('file', 'user'))

  def __str__(self) -> str:
    return self.name


class UserFile(models.Model):
  """
  Through model for File and User m2m relationship.

  Will contain a done field to check wether the file is finished
  reviewing or not.
  """
  file = models.ForeignKey(File, on_delete=models.CASCADE)
  user = models.ForeignKey('cme.Bussines', on_delete=models.CASCADE)
  done = models.BooleanField(default=False)

  def __str__(self) -> str:
    return f'{self.file} - {self.user} | {self.done}'
