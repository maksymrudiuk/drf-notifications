from celery import shared_task
from core.celery import task_method
# from core.tasks import send as celery_send
from .base import BaseNotificationSingleSender


class SyncDefaultSender(BaseNotificationSingleSender):
    pass


class CeleryDefaultSender(BaseNotificationSingleSender):

    def send(self):
        self.send_notification.delay(self.module_name, self.slug, self.recipient, self.context)

    # ! Strange code
    @staticmethod
    @shared_task(name="core.CeleryDefaultSender.send_notification", bind=True, filter=task_method)
    def send_notification(task, module_name, slug, recipient, context, *args, **kwargs):
        super(CeleryDefaultSender, CeleryDefaultSender).send_notification(
            module_name=module_name,
            slug=slug,
            recipient=recipient,
            context=context,
            *args,
            **kwargs
        )
