from collections import OrderedDict

from django.template import Template, Context
from django.utils.html import strip_tags
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from core.senders.default import SyncDefaultSender
from core.utils import get_object_or_none
from .decorators import logging_sending_errors


class BaseModelNotification:

    model = None
    default_subject = str

    def __init__(self, slug: str, recipient: str, context=dict(), sender=SyncDefaultSender, *args, **kwargs):
        """ Constructor.

        Arguments:
            name {str} -- notification slug.
            recipient {str} -- recipient list (user email).
            subject_context {dict} -- context to render subject message.
            context {dict} -- context to render notification message.
        """

        self.notification = self.get_notification_template(slug)
        self.context = context
        self.recipient = recipient
        self._type = self.__class__.__name__
        self.sender = sender

    def send(self, **kwargs):
        """ Not Implemented Method."""
        raise NotImplementedError("Method send must be implemented.")

    @logging_sending_errors
    def perform_send(self, instance):
        """ Not Implemented Method."""
        raise NotImplementedError("Method perform send must be implemented.")

    def get_message(self):
        """ Not Implemented Method."""
        raise NotImplementedError("Method get_message must be implemented.")

    def get_subject(self):
        """ Implemented Method.

        Returns:
            [str] -- notification subject or default.
        """

        template = self.get_subject_template()
        context = self.get_context(convert=True)
        return self.validate_subject(template.render(context))

    def get_context(self, convert=False) -> Context:
        if self.context and isinstance(self.context, (dict, OrderedDict)):
            if self.notification.template and not convert:
                return self.context
            return Context(self.context)
        else:
            raise TypeError("Context must be a dict.")

    def get_notification_template(self, slug: str):
        """ Implemented Method.

        Arguments:
            slug {str} -- notification slug.

        Returns:
            [model] -- notification model instance
        """

        obj = get_object_or_none(self.model, slug=slug)
        if not obj:
            raise ObjectDoesNotExist()
        return obj

    def validate_recipient(self) -> (list, tuple):
        """ Implemented Method.

        Returns:
            recipients {list, tuple} -- valid recipients list (user emails).

        Raise`s:
            TypeError {Exception} -- if [recipients] is not a list or tuple.
            ValidationError {Exception} -- if validation is failture.
        """

        if not isinstance(self.recipient, str):
            raise TypeError("Recipient must be a str.")

        try:
            validate_email(self.recipient)
        except ValidationError:
            raise ValidationError('Enter valid recipient email.')
        else:
            return self.recipient

    def get_subject_template(self) -> Template:
        """ Implemented Method.

        Returns:
            subject {Template} -- Notification subject template.
        """

        subject_template = self.validate_template_string(self.notification.subject)
        return Template(subject_template)

    @staticmethod
    def validate_subject(subject: str):
        """ Implemented Method.

        Returns:
            subject {str} -- Notification validated subject.
        """
        return strip_tags(subject).replace('\r', '').replace('\n', '')

    @staticmethod
    def validate_template_string(template_string):

        clean_template = template_string

        replace_map = (
            ("{{ ", "{{"),
            (" }}", "}}"),
            ("&nbsp;}}", "}}"),
            ("{{&nbsp;", "{{"),
        )

        for _from, _to in replace_map:
            clean_template = clean_template.replace(_from, _to)

        return clean_template


class ModelNotification(BaseModelNotification):
    """ Notification class. With provided params. [BaseDBNotification].

    Arguments:
        notification_model { models.Model } -- Notification
        default_subject {str} -- 'Title' for default
    """

    # Prevent python cross-import error
    from ..models import NotificationTemplate

    model = NotificationTemplate
    default_subject = 'Subject'
