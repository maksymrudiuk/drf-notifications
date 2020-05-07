from django.contrib.auth import get_user_model

from decouple import config
from core.models import NotificationTemplate
from core.backends.generics import EmailModelNotification, EmailMultiAlternativesModelNotification


def run():
    User = get_user_model()
    notification_slug = NotificationTemplate.objects.all().first().slug
    user = User.objects.get(id=1)
    recipient = 'maksym.rudiuk@gmail.com'
    context = {
        'user': user
    }

    mail = EmailModelNotification(notification_slug, recipient, context)
    mail.send()
