from ..legacy_types import Bussines
from ..training_types import UserFile, UserFileType, File

import graphene


class UpdateUserFile(graphene.Mutation):
  """ Mutation to update the `done` field in a `UserFile` """

  class Arguments:
    file_id = graphene.ID()
    user_id = graphene.ID()
    done = graphene.Boolean()

  file = graphene.Field(UserFileType)

  @classmethod
  def mutate(cls, root, info, file_id: int, user_id: int, done: bool):
    # Get the UserFile
    try:
      uf: UserFile = UserFile.objects.get(file=File.objects.get(pk=file_id), user=Bussines.objects.get(pk=user_id))
      uf.done = done
      uf.save()
    except UserFile.DoesNotExist:
      uf: UserFile = UserFile.objects.create(file=File.objects.get(pk=file_id), user=Bussines.objects.get(pk=user_id), done=done)

    return UpdateUserFile(file=uf)


class Mutation(graphene.ObjectType):
  update_userfile = UpdateUserFile.Field()
