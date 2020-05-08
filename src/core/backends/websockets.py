from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .base import ModelNotification
from .mixins import JsonContentMixin


channel_layer = get_channel_layer()


class BaseWebSocketNotification(JsonContentMixin, ModelNotification):

    groups = None
    websocket_handler = None

    def send(self, **kwargs):
        """ Method.

        Arguments:
            recipients {list, tuple} -- recipients list (user emails).
        """

        group = self.validate_recipient()
        message = self.get_message()
        self.perform_send(group, message)

    def perform_send(self, recipient, content, **kwargs):
        """ Method.

        Arguments:
            recipients {list, tuple} -- recipients list (user emails).
            content {dict} -- content response in socket.
        """

        async_to_sync(channel_layer.group_send)(
            "{}".format(recipient),
            {"type": "{}".format(self.websocket_handler), "text": content})

    def validate_recipient(self):
        """ Overrided Method.

        Create group name from recipient.

        Returns:
            [list] -- recipient groups in channel.
        """

        super().validate_recipient()

        return self.get_group_name(self.recipient)

    @staticmethod
    def get_group_name(recipient):
        raise NotImplementedError("Method perform send must be implemented.")

    def get_message(self):
        return self.get_content()
