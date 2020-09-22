from graphene import relay, ObjectType, AbstractType, String, Boolean, ID, Field, DateTime, Int, Float, InputObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.connection.arrayconnection import offset_to_cursor
from .models import Card
from graphql_relay import from_global_id

from graphene_subscriptions.events import CREATED

from rx import Observable


class CardNode(DjangoObjectType):
    class Meta:
        model = Card
        interfaces = (relay.Node, )
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'content': ['icontains'],
            'author': ['exact', 'icontains'],
            'state': ['exact'],
            'importance': ['exact', 'gte', 'lte'],
            'color': ['exact'],
            'date': ['gte', 'lte']
        }


class CardConnection(relay.Connection):
    class Meta:
        node = CardNode
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'content': ['icontains'],
            'author': ['exact', 'icontains'],
            'state': ['exact'],
            'importance': ['exact', 'gte', 'lte'],
            'color': ['exact'],
            'date': ['gte', 'lte']
        }


class Query(object):
    node = relay.Node.Field()

    card = relay.Node.Field(CardNode)
    all_cards = DjangoFilterConnectionField(CardNode)
    # all_cards = relay.ConnectionField(CardConnection)


'''
Mutations
'''


CardEdge = CardNode._meta.connection.Edge


class NewCard(relay.ClientIDMutation):
    ok = Boolean()
    card_edge = Field(CardEdge)
    # card = Field(CardNode)

    class Input:
        author = String(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card()
            card.author = input.author
            card.save()
            edge = CardEdge(cursor=offset_to_cursor(0), node=CardNode)
            return NewCard(card_edge=edge, ok=True)
        except Exception as err:
            print("NewCard error : ", err)
            return NewCard(card_edge=None, ok=False)


class UpdateCard(relay.ClientIDMutation):
    ok = Boolean()
    card = Field(CardNode)

    class Input:
        id = ID(required=True)
        title = String(required=False)
        content = String(required=False)
        author = String(required=False)
        date = DateTime(required=False)
        state = String(required=False)
        importance = Int(required=False)
        color = String(required=False)

        x = Int(required=False)
        y = Int(required=False)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card.objects.get(pk=from_global_id(input.id)[1])
            for key in input:
                if key is not "id":
                    setattr(card, key, getattr(input, key))
            card.save()
            return UpdateCard(card=card, ok=True)
        except Exception as err:
            print("UpdateCard error : ", err)
            return UpdateCard(card=None, ok=False)


class DeleteCard(relay.ClientIDMutation):
    ok = Boolean()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card.objects.get(pk=from_global_id(input.id)[1])
            card.delete()
            return DeleteCard(ok=True)
        except Exception as err:
            print("DeleteCard error : ", err)
            return DeleteCard(ok=False)


class RelayMutation(AbstractType):
    new_card = NewCard.Field()
    update_card = UpdateCard.Field()
    delete_card = DeleteCard.Field()


class Subscription(ObjectType):
    hello = String()
    card_created = Field(CardNode)

    def resolve_hello(root, info):
        return Observable.interval(3000) \
            .map(lambda i: "hello world!")

    def resolve_card_created(root, info):
        return root.filter(
            lambda event:
            event.operation == CREATED and
            isinstance(event.instance, Card)
        ).map(lambda event: event.instance)
