import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives
from .emails import BaseEmailModelNotification
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
