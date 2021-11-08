from django.test import TestCase

from ..models import Module, Type, Survey, Question

# Create your tests here.
class SurveyTestCase(TestCase):
	def setUp(self) -> None:
		modules: Module = [

		]