from itertools import chain

from channels.routing import ProtocolTypeRouter, URLRouter

from core.contrib.websockets.auth_middleware import JWTTokenAuthMiddleware
from core.routing import websoket_urlpatterns as core_routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': JWTTokenAuthMiddleware(
        URLRouter(list(chain(
            core_routing,
        )))
    ),
})
