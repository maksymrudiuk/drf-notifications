from celery import shared_task
from core.tasks import send as celery_send
from .base import BaseNotificationSingleSender


class SyncDefaultSender(BaseNotificationSingleSender):
    pass


class CeleryDefaultSender(BaseNotificationSingleSender):

    def send(self):
        celery_send.delay(self.module_name, self.slug, self.recipient, self.context)

    # ! Not working yet need research
    @staticmethod
    @shared_task
    def __handler(module_name, slug, recipient, context):
        super(CeleryDefaultSender, CeleryDefaultSender).__handler(
            module_name, slug, recipient, context)
