from graphene import relay, ObjectType, AbstractType, String, Boolean, ID, Field, DateTime, Int, Float, InputObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Card
from graphql_relay import from_global_id


class CardNode(DjangoObjectType):
    class Meta:
        model = Card
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'content': ['icontains'],
            'author': ['exact', 'icontains'],
            'state': ['exact'],
            'importance': ['exact', 'gte', 'lte'],
            'color': ['exact'],
            'date': ['gte', 'lte']
        }
        interfaces = (relay.Node, )


class Query(object):
    node = relay.Node.Field()

    card = relay.Node.Field(CardNode)
    all_cards = DjangoFilterConnectionField(CardNode)


'''
Mutations
'''


class NewCard(relay.ClientIDMutation):
    ok = Boolean()
    card = relay.Node.Field(CardNode)

    class Input:
        author = String(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card()
            card.author = input.author
            card.save()
            return NewCard(card=card, ok=True)
        except Exception as err:
            print("NewCard error : ", err)
            return NewCard(card=None, ok=False)


class UpdateCard(relay.ClientIDMutation):
    ok = Boolean()
    card = relay.Node.Field(CardNode)

    class Input:
        id = ID(required=True)
        title = String(required=False)
        content = String(required=False)
        author = String(required=False)
        date = DateTime(required=False)
        state = String(required=False)
        importance = Int(required=False)
        color = String(required=False)

        x = Float(required=False)
        y = Float(required=False)

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
