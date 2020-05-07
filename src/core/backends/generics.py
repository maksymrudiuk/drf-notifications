import logging

from django.core.mail import EmailMessage, EmailMultiAlternatives
from .emails import BaseEmailModelNotification
from .formatters import ContentHTMLFormatter

logger = logging.getLogger('django')


class EmailModelNotification(BaseEmailModelNotification):
    """ EmailMessageNotification class [BaseEmailModelNotification].

    Arguments:
        email_class {type} -- EmailMessage
    """

    email_class = EmailMessage


class EmailMultiAlternativesModelNotification(BaseEmailModelNotification):
    """ EmailMultiAlternativesNotification class [BaseEmailModelNotification]

    Arguments:
        email_class {type} -- EmailMultiAlternatives
    Overrided Methods:
        create
    """

    email_class = EmailMultiAlternatives

    def create(self, **kwargs):
        """ Overrided Method.

        Add html content to alternatives.

        Arguments:
            recipients {list, tuple} -- recipients list (user emails).

        Returns:
            [email_class] -- email class instance
        """

        email = super().create()
        html_content = self.get_context(formatter=ContentHTMLFormatter)
        email.attach_alternative(html_content, "text/html")
        return email
