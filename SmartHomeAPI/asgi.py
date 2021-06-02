"""
ASGI config for SmartHomeAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartHomeAPI.settings')

from django.core.asgi import get_asgi_application
from django.urls import path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from API.consumers import DeviceConsumer



application = ProtocolTypeRouter({
    # (http->django views is added by default)
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('api/@<str:phonenumber>/devices',DeviceConsumer.as_asgi()),
        ])
    ),
})