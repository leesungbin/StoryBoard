import graphene
import postit.schema


class Query(postit.schema.Query, graphene.ObjectType):
    pass


class Mutation(postit.schema.RelayMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
# schema = graphene.Schema(query=Query)
