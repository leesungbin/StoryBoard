from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from postit.models import Card

post_save.connect(post_save_subscription, sender=Card, dispatch="card_save")
post_delete.connect(post_delete_subscription,
                    sender=Card, dispatch="card_delete")
