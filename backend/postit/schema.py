from graphene import relay, ObjectType, AbstractType, String, Boolean, ID, Field, DateTime, Int, Float, InputObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.connection.arrayconnection import offset_to_cursor
from .models import Card
# from .subscription import CardHasCreated
from graphql_relay import from_global_id
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


class Query(object):
    node = relay.Node.Field()

    card = relay.Node.Field(CardNode)
    all_cards = DjangoFilterConnectionField(CardNode)
    # all_cards = relay.ConnectionField(CardConnection)


'''
Subscriptions
'''

from channels_graphql_ws import Subscription
class Test(Subscription):
    """Simple GraphQL subscription."""

    # Subscription payload.
    text = String()

    # class Arguments:
    #     """That is how subscription arguments are defined."""
    #     arg1 = String()
    #     arg2 = String()

    @staticmethod
    def subscribe(root, info):
        """Called when user subscribes."""
        print("subscribed!!")
        # Return the list of subscription group names.
        return ['group1']

    @staticmethod
    def publish(payload, info):
        """Called to notify the client."""

        # Here `payload` contains the `payload` from the `broadcast()`
        # invocation (see below). You can return `MySubscription.SKIP`
        # if you wish to suppress the notification to a particular
        # client. For example, this allows to avoid notifications for
        # the actions made by this particular client.
        print("publish : ", payload)
        return Test(text='Something has happened!')

class CardHasCreated(Subscription):
    sender = String()
    card = Field(CardNode)
    
    class Arguments:
        group = String()

    @staticmethod
    def subscribe(self, info, group):
        return [group]

    @staticmethod
    def publish(self, info):
        return CardHasCreated(sender=self.sender, card=self.card)
    
    @classmethod
    def announce(cls, group, sender, card):
        cls.broadcast(
            group=group,
            payload={"sender": sender, "card": card},
        )

class RelaySubscription(ObjectType):
    test = Test.Field()
    card_has_created = CardHasCreated.Field()

'''
Mutations
'''

class CardEdge(ObjectType):
    node = Field(CardNode)
    cursor = String()

class MutationWithSubscription(relay.ClientIDMutation):
    text = String()
    @classmethod
    def mutate(cls, root, info, input):
        t="hello subs"
        Test.broadcast()
        return MutationWithSubscription(text=t)

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
            card_edge = CardEdge(
                cursor=offset_to_cursor(Card.objects.count()), node=card)

            CardHasCreated.announce("group1", card.author, card)
            return NewCard(card_edge=card_edge, ok=True)
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
                if key != "id":
                    setattr(card, key, getattr(input, key))
            card.save()
            return UpdateCard(card=card, ok=True)
        except Exception as err:
            print("UpdateCard error : ", err)
            return UpdateCard(card=None, ok=False)


class DeleteCard(relay.ClientIDMutation):
    ok = Boolean()
    id = ID()

    class Input:
        id = ID(required=True)

    @classmethod
    def mutate(cls, root, info, input):
        try:
            card = Card.objects.get(pk=from_global_id(input.id)[1])
            card.delete()
            return DeleteCard(ok=True, id=input.id)
        except Exception as err:
            print("DeleteCard error : ", err)
            return DeleteCard(ok=False)


class RelayMutation(AbstractType):
    new_card = NewCard.Field()
    update_card = UpdateCard.Field()
    delete_card = DeleteCard.Field()
    with_subscription = MutationWithSubscription.Field()
