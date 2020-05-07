from celery import shared_task
from core.utils import import_by_string


@shared_task
def send(module_name, slug, recipient, context):
    notification_class = import_by_string(module_name)
    notification = notification_class(slug=slug, recipient=recipient, context=context)
    notification.send()
