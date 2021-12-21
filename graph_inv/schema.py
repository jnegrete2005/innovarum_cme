from .legacy.queries import Query as LegacyQuery
from .legacy.mutations import Mutation as LegacyMutation

from .training.queries import Query as TrainingQuery
from .training.mutations import Mutation as TrainingMutation

from graphene import Schema


class Query(LegacyQuery, TrainingQuery):
  pass


class Mutation(LegacyMutation, TrainingMutation):
  pass


schema = Schema(Query, Mutation)
