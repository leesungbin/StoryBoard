import channels
from channels.routing import ProtocolTypeRouter
import django
import channels_graphql_ws
import schema

class MyGraphqlWsConsumer(channels_graphql_ws.GraphqlWsConsumer):
    """Channels WebSocket consumer which provides GraphQL API."""
    schema = schema.schema

    # Uncomment to send keepalive message every 42 seconds.
    # send_keepalive_every = 42

    # Uncomment to process requests sequentially (useful for tests).
    # strict_ordering = True

    async def on_connect(self, payload):
        """New client connection handler."""
        # You can `raise` from here to reject the connection.
        print("New client connected!")

# application = ProtocolTypeRouter({
#     # Empty for now (http->django views is added by default)
# })

application = channels.routing.ProtocolTypeRouter({
    'websocket': channels.routing.URLRouter([
        django.urls.path('graphql/', MyGraphqlWsConsumer),
    ])
})