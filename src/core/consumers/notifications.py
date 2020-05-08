import json
import logging
import hashlib

from django.utils.text import slugify

from channels.generic.websocket import AsyncWebsocketConsumer

from .mixins import AsyncJsonWebTokenSocketMixin

logger = logging.getLogger('django')


class NotificationConsumer(AsyncJsonWebTokenSocketMixin, AsyncWebsocketConsumer):
    """
        This Notification consumer handles websocket connections for clients.

        It uses AsyncJsonWebsocketConsumer, which means all the handling
        functionsmust be async functions, and any sync work (like ORM access)
        has to be behind database_sync_to_async or sync_to_async.
    """

    async def connect(self):

        if self.has_jwt_auth_error():
            await self.jwt_auth_error_handling()
        else:
            try:
                await self.channel_layer.group_add(
                    self.group_name(self.scope['user'].email),
                    self.channel_name)
                await self.accept()
                await self.send(
                    text_data=json.dumps({'user': self.scope['user'].email}),
                    close=False)
            except Exception as e:
                logger.error('Connect error. {}'.format(e))
                await self.close()

    async def notification_send(self, event):
        try:
            await self.send(text_data=json.dumps(event['text']), close=False)
        except Exception as e:
            logger.error('Notification sending error. {}'.format(e))

    async def disconnect(self, close_code):
        if await self.has_jwt_auth_error():
            try:
                await self.channel_layer.group_discard(
                    self.group_name(self.scope['user'].email),
                    self.channel_name)
            except Exception as e:
                logger.error('Disconnecting error. {}'.format(e))
        else:
            await super(AsyncWebsocketConsumer, self).disconnect(close_code)

    @staticmethod
    def group_name(user_email):
        result = hashlib.md5(user_email.encode('ascii'))
        group = "group-{}".format(slugify(result.hexdigest()))
        return group
