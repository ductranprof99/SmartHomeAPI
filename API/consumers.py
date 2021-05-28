import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Home,Device

class DeviceConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connect",event)
        await self.send({
            "type":"websocket.accept",
        })
        await self.send({
            "type":"websocket.close",
        })

    async def websocket_receive(self,event):
        print("receive",event)

    async def websocket_disconnect(self,event):
        print("disconnect",event)
    

