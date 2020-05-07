import logging

from django.conf import settings

from .base import ModelNotification
from .mixins import TemplateContentMixin
from .decorators import logging_sending_errors
from .formatters import ContentTextFormatter


logger = logging.getLogger('django')


class BaseEmailModelNotification(TemplateContentMixin, ModelNotification):

    email_class = None
    from_email = settings.EMAIL_HOST_USER

    def get_email_class(self):
        assert self.email_class is not None, (
            "'%s' should either include a `email_class` attribute."
            % self.__class__.__name__
        )

        return self.email_class

    def create(self, **kwargs):

        self.validate_recipient()
        message = self.get_message()

        Email = self.get_email_class()

        return Email(
            subject=self.get_subject(),
            body=message,
            from_email=self.from_email,
            to=[self.recipient]
        )

    def get_message(self):
        return self.get_content(formatter=ContentTextFormatter)

    def send(self, **kwargs):
        email = self.create()
        self.perform_send(email)

    @logging_sending_errors()
    def perform_send(self, instance, **kwargs):
        instance.send()
