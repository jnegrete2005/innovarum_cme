from typing import List
from ..legacy_types import UserTrioType, UserTrio, Trio, Bussines

import graphene


class UpdateUserTrio(graphene.Mutation):
  """ Mutation to update the `done` field in a `UserTrio` """
  class Arguments:
    trio_id = graphene.ID()
    user_id = graphene.ID()
    done = graphene.List(graphene.Boolean, required=True)

  trio = graphene.Field(UserTrioType)

  @classmethod
  def mutate(cls, root, info, trio_id: int, user_id: int, done: List[bool]):
    # Get the UserTrio
    try:
      ut: UserTrio = UserTrio.objects.get(trio=Trio.objects.get(pk=trio_id), user=Bussines.objects.get(pk=user_id))
      ut.done = done
      ut.save()
    except UserTrio.DoesNotExist:
      ut: UserTrio = UserTrio.objects.create(trio=Trio.objects.get(pk=trio_id), user=Bussines.objects.get(pk=user_id), done=done)

    return UpdateUserTrio(trio=ut)


class Mutation(graphene.ObjectType):
  update_usertrio = UpdateUserTrio.Field()
