from datetime import datetime
from django.test import TestCase

from ..models import Bussines, Score, Module, Type, Survey, Block, Question

# Create your tests here
class UserScoreTestCase(TestCase):
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
		questions = [
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

		# Bussiness
		b = Bussines.objects.create(
			email='test@test.com',
			first='Test',
			last='User',
			role='Test Role'
		)

	# Tests for users
	def test_new_superuser(self):
		super_user = Bussines.objects.create_superuser('test@supertest.com', 'Test', 'User', 'Test Role', 'Password')

		self.assertEqual(super_user.email, 'test@supertest.com')
		self.assertEqual(super_user.first, 'Test')
		self.assertEqual(super_user.last, 'User')
		self.assertEqual(super_user.role, 'Test Role')

		self.assertTrue(super_user.is_superuser)
		self.assertTrue(super_user.is_staff)
		self.assertTrue(super_user.is_active)

		self.assertEqual(str(super_user), 'Test User')

		with self.assertRaises(ValueError):
			Bussines.objects.create_superuser(
				email='testuser@supertest.com', first='Test', last='User', role='Test Role', password='password', is_superuser=False
			)

		with self.assertRaises(ValueError):
			Bussines.objects.create_superuser(
				email='testuser@supertest.com', first='Test', last='User', role='Test Role', password='password', is_staff=False
			)

		with self.assertRaises(ValueError):
			Bussines.objects.create_superuser(
				email='testuser@supertest.com', first='Test', last='User', role='Test Role', password='password', is_active=False
			)

	def test_new_user(self):
		user = Bussines.objects.create_user(email='testuser@testmail.com', first='Test', last='User', role='Test Role', password='password')

		self.assertEqual(user.email, 'testuser@testmail.com')
		self.assertEqual(user.first, 'Test')
		self.assertEqual(user.last, 'User')
		self.assertEqual(user.role, 'Test Role')

		self.assertFalse(user.is_superuser)
		self.assertFalse(user.is_staff)
		self.assertTrue(user.is_active)

		with self.assertRaises(ValueError):
			Bussines.objects.create_user(email='', first='Test', last='User', role='Test Role', password='password')

	def test_score(self):
		""" Test for functionalities of score """
		# Get the user to create the score
		user = Bussines.objects.first()

		# Score
		score: Score = Score.objects.create(
			score=[20, 12, 13, 14, 16],
			bussines=user,
			survey=Survey.objects.first()
		)
		self.assertEqual(75, score.get_score())
