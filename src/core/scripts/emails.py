from django.contrib.auth import get_user_model
from core.models import NotificationTemplate
# from core.backends.generics import EmailModelNotification, EmailMultiAlternativesModelNotification
from core.senders import CeleryDefaultSender, SyncDefaultSender


def run():
    User = get_user_model()
    notification_slug = NotificationTemplate.objects.all().first().slug
    user = User.objects.get(id=1)
    recipient = 'maksym.rudiuk@gmail.com'
    context = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    sender = CeleryDefaultSender(
        notification_slug,
        'WebSocketNotification',
        recipient,
        context
    )
    sync_sender = SyncDefaultSender(
        notification_slug,
        'WebSocketNotification',
        recipient,
        context
    )
    # sender.send()
    sync_sender.send()
