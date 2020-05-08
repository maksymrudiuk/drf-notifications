import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives

from core.serializers.websockets import WebSocketNotificationSerializer
from core.consumers import NotificationConsumer
from .emails import BaseEmailModelNotification
from .websockets import BaseWebSocketNotification
from .formatters import ContentHTMLFormatter

logger = logging.getLogger('django')


class EmailModelNotification(BaseEmailModelNotification):
    email_class = EmailMessage


class EmailMultiAlternativesModelNotification(BaseEmailModelNotification):

    email_class = EmailMultiAlternatives

    def create(self, **kwargs):
        email = super().create()
        html_content = self.get_content(formatter=ContentHTMLFormatter)
        email.attach_alternative(html_content, "text/html")
        return email


class WebSocketNotification(BaseWebSocketNotification):

    serializer_class = WebSocketNotificationSerializer
    websocket_handler = "notification.send"

    @staticmethod
    def get_group_name(recipient):
        return NotificationConsumer.group_name(recipient)
