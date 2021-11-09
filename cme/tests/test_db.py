from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Module, Type, Survey, Question, YesOrNo

# Create your tests here.
class SurveyTestCase(TestCase):
	def setUp(self) -> None:
		# Modules
		module: Module = Module.objects.create(
			name='Módulo de Optimización Operacional',
			code='moo'
		)

		# Types
		type: Type = Type.objects.create(type='industrial')

		# Surveys
		survey = Survey.objects.create(module=module, type=type)

		# Questions
		questions: Question = [
			Question.objects.create(
				survey=survey,
				text='Te gusta McDonalds?',
				score=YesOrNo.YES
			),
			Question.objects.create(
				survey=survey,
				text='Te gusta Burger King?',
				score=YesOrNo.NO
			),
			Question.objects.create(
				survey=survey,
				text='16?',
				score=YesOrNo.YES
			)
		]

	def test_module(self):
		Module.objects.get(code='moo')
		Module.objects.create(name='Módulo de Productividad Comercial', code='mpc')

		self.assertEqual(
			Module.objects.first().surveys.first(),
			Survey.objects.first()
		)

		with self.assertRaises(IntegrityError):
			Module.objects.create(name=None)
			Module.objects.create(code=None)


	def test_type(self):
		Type.objects.get(type='industrial')
		Type.objects.create(type='comercial')

		self.assertEqual(
			Type.objects.first().surveys.first(),
			Survey.objects.first()
		)

		with self.assertRaises(IntegrityError):
			Type.objects.create(type=None)
	
	def test_survey(self):
		survey = Survey.objects.first()
		self.assertEqual(survey.module.code, 'moo')
		self.assertEqual(survey.type.type, 'industrial')

		self.assertEqual(
			survey.questions.first(),
			Question.objects.first()
		)

		with self.assertRaises(IntegrityError):
			Survey.objects.create(module=None)

	def test_question(self):
		question = Question.objects.first()
		self.assertEqual(question.survey, Survey.objects.first())

		with self.assertRaises(IntegrityError):
			Question.objects.create(survey=None)
