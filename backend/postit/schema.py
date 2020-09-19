from graphene import relay, ObjectType, AbstractType, String, Boolean, ID, Field, DateTime, Int, InputObjectType
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
Input types
'''


# class NewCardInput(InputObjectType):
#     author = String(required=True)


# class UpdateCardInput(InputObjectType):
#     id = ID()
#     title = String()
#     content = String(required=False)
#     date = DateTime()
#     state = String()
#     importance = Int()
#     color = String()


'''
Mutations
'''


class TestMutation(relay.ClientIDMutation):
    ok = Boolean()

    class Input:
        pass

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        return TestMutation(ok=True)


class NewCard(relay.ClientIDMutation):
    ok = Boolean()
    card = relay.Node.Field(CardNode)

    # class Arguments:
    #     card_data = NewCardInput(required=True)
    class Input:
        author = String(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            # print("@@", input)
            card = Card()
            card.author = input.author
            card.save()
            return NewCard(card=card, ok=True)
        except Exception as err:
            print("NewCard err : ", err)
            return NewCard(card=None, ok=False)


class UpdateCard(relay.ClientIDMutation):
    ok = Boolean()
    card = relay.Node.Field(CardNode)

    # class Arguments:
    #     cards_data = UpdateCardInput(required=True)
    class Input:
        id = ID()
        title = String()
        content = String(required=False)
        author = String()
        date = DateTime()
        state = String()
        importance = Int()
        color = String()

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card.objects.get(pk=from_global_id(input.id)[1])
            card.title = input.title
            card.content = input.content
            card.author = input.author
            card.date = input.date
            card.state = input.state
            card.importance = input.importance
            card.color = input.color
            card.save()
            return UpdateCard(card=card, ok=True)
        except Exception as err:
            print("UpdateCard err : ", err)
            return UpdateCard(card=None, ok=False)


class DeleteCard(relay.ClientIDMutation):
    ok = Boolean()

    class Input:
        id = ID()

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