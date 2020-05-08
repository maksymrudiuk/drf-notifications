from core.senders import CeleryDefaultSender
from .notifications import send

send_notification = CeleryDefaultSender.send_notification
