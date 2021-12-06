from .legacy.queries import Query as LegacyQuery
from .legacy.mutations import Mutation as LegacyMutation

from graphene import Schema


class Query(LegacyQuery):
  pass


class Mutation(LegacyMutation):
  pass


schema = Schema(Query, Mutation)
