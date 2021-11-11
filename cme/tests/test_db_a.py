from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Module, Type, Survey, Block, Question

# Create your tests here.
class SurveyTestCase(TestCase):
	def setUp(self) -> None:
		# Module
		module = Module.objects.create(
			name='Módulo de Optimización Operacional',
			code='moo'
		)

		# Type
		type = Type.objects.create(type='industrial')

		# Survey
		survey = Survey.objects.create(module=module, type=type)

		# Block
		block = Block.objects.create(
			survey=survey,
			name='Bloque de Comida Rapida'
		)

		# Questions
		questions: Question = [
			Question.objects.create(
				block=block,
				text='Te gusta McDonalds?',
			),
			Question.objects.create(
				block=block,
				text='Te gusta Burger King?',
			),
			Question.objects.create(
				block=block,
				text='16?',
			)
		]

	def test_module(self):
		""" Test Module class """
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
		""" Test Type class """
		Type.objects.get(type='industrial')
		Type.objects.create(type='comercial')

		self.assertEqual(
			Type.objects.first().surveys.first(),
			Survey.objects.first()
		)

		with self.assertRaises(IntegrityError):
			Type.objects.create(type=None)
	
	def test_survey(self):
		""" Test Survey class """
		survey = Survey.objects.first()
		self.assertEqual(survey.module.code, 'moo')
		self.assertEqual(survey.type.type, 'industrial')

		self.assertEqual(
			survey.blocks.first(),
			Block.objects.first()
		)

		with self.assertRaises(IntegrityError):
			Survey.objects.create(module=None)

	
	# TODO: Test block
	def test_block(self):
		""" Test Block class """
		block = Block.objects.first()
		self.assertEqual(block.name, 'Bloque de Comida Rapida')
		self.assertEqual(block.survey, Survey.objects.first())

		with self.assertRaises(IntegrityError):
			Block.objects.create(survey=None)


	def test_question(self):
		""" Test Question class """
		question = Question.objects.first()
		self.assertEqual(question.block, Block.objects.first())

		with self.assertRaises(IntegrityError):
			Question.objects.create(block=None)
