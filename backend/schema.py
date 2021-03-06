import graphene
import postit.schema

class Query(postit.schema.Query, graphene.ObjectType):
    pass


class Mutation(postit.schema.RelayMutation, graphene.ObjectType):
    pass


class Subscription(postit.schema.RelaySubscription, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
