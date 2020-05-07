import logging
from core.utils import import_by_string

logger = logging.getLogger('django')


class BaseNotificationSingleSender:

    app_name = 'core'
    package_name = 'backends'

    def __init__(self, slug, notification_cls: str, recipient: str, context=dict(), *args, **kwargs):
        self.slug = slug
        self.context = context
        self.recipient = recipient
        self.module_name = self.get_module_name(notification_cls)

    def send(self):
        self.__handler(self.module_name, self.slug, self.recipient, self.context)

    @staticmethod
    def __handler(module_name, slug, recipient, context):
        notification_class = import_by_string(module_name)
        notification = notification_class(slug=slug, recipient=recipient, context=context)
        notification.send()

    def get_module_name(self, notification_class):
        return ".".join([self.app_name, self.package_name, notification_class])
