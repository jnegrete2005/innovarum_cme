from .legacy.queries import Query as LegacyQuery
from .legacy.mutations import Mutation as LegacyMutation

from .training.queries import Query as TrainingQuery

from graphene import Schema


class Query(LegacyQuery, TrainingQuery):
  pass


class Mutation(LegacyMutation):
  pass


schema = Schema(Query, Mutation)
