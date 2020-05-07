# from core.senders import CeleryDefaultSender
from .notifications import send

# send_notification__class = CeleryDefaultSender.__handler

__all__ = ['send']
