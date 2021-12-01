from .legacy.queries import Query as LegacyQuery

from graphene import Schema


class Query(LegacyQuery):
  pass


schema = Schema(query=Query)
