from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from API.consumers import DeviceConsumer



application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('@<str:phonenumber>/devices',DeviceConsumer),
            path('@<str:phonenumber>/devices/<int:deviceOrder>',DeviceConsumer),
        ])
    ),
})