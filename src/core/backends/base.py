from collections import OrderedDict

from django.template import Context, Template
from django.utils.html import strip_tags
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from ..utils import get_object_or_none


class BaseModelNotification:
    """Base model Notification class.

    Arguments:
        notification_model { models.Model } -- Notification db model
        default_subject {str} -- default: [str]

    Implemented methods:
        get_notification
        validate_recipients
        get_subject

    Not Implemented methods:
        send
        perform_send
    """

    model = None
    default_subject = str

    def __init__(self, name: str, recipient: str, context=dict(), *args, **kwargs):
        """ Constructor.

        Arguments:
            name {str} -- notification slug.
            recipient {str} -- recipient list (user email).
            subject_context {dict} -- context to render subject message.
            context {dict} -- context to render notification message.
        """

        self.context = context
        self.notification_template = self.get_notification_template(name)
        self.recipient = recipient
        self._type = self.__class__.__name__

    def send(self, **kwargs):
        """ Not Implemented Method."""
        raise NotImplementedError("Method send must be implemented.")

    def perform_send(self, **kwargs):
        """ Not Implemented Method."""
        raise NotImplementedError("Method perform_send must be implemented.")

    def get_message(self):
        """ Not Implemented Method."""
        raise NotImplementedError("Method get_message must be implemented.")

    def get_subject(self):
        """ Implemented Method.

        Returns:
            [str] -- notification subject or default.
        """

        template = self.get_subject_template()
        return self.validate_subject(template.render(self.context))

    def get_notification_template(self, name: str):
        """ Implemented Method.

        Arguments:
            name {str} -- notification slug.

        Returns:
            [notification_model] -- notification model instance
        """

        obj = get_object_or_none(self.notification_model, slug=name)
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

        if self.notification:
            return Template(self.notification.subject)

    @staticmethod
    def validate_subject(subject: str):
        """ Implemented Method.

        Returns:
            subject {str} -- Notification validated subject.
        """

        return strip_tags(subject).replace('\r', '').replace('\n', '')


class ModelNotification(BaseModelNotification):
    """ Notification class. With provided params. [BaseDBNotification].

    Arguments:
        notification_model { models.Model } -- Notification
        default_subject {str} -- 'Title' for default
    """

    # Prevent python cross-import error
    from ..models import Notification

    model = Notification
    default_subject = 'Subject'
