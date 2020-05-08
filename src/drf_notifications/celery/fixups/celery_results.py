# from __future__ import absolute_import, unicode_literals
from celery import signals
from kombu.utils import cached_property, symbol_by_name


def fixup(app):
    """Install Django fixup if settings module environment is set."""
    return DjangoFixup(app).install()


class DjangoFixup(object):
    """Fixup installed when using Django."""

    def __init__(self, app):
        self.app = app

    @cached_property
    def model(self):
        return symbol_by_name('django_celery_results.models:TaskResult')

    def install(self):
        # # Need to add project directory to path.
        # # The project directory has precedence over system modules,
        # # so we prepend it to the path.
        # sys.path.insert(0, os.getcwd())
        #
        # self._settings = symbol_by_name('django.conf:settings')
        signals.after_task_publish.connect(self.on_task_publish)

        return self

    def autodiscover_tasks(self):
        # just fix for attribute error
        return []

    def on_task_publish(self, **kwargs):
        """
        Receiver that save published task to db like :meth:`_store_result`
        of :class:`DatabaseBackend`

        Keyword Args:
            sender (Any): The sender of the signal.
                Either a specific object or :const:`None`.
            body (Any): The body of the task.
            headers (Any): Message headers.
            exchange (kombu.Exchange, str):
                if queue is str, specifies exchange name.
            routing_key (str): if queue is str, specifies binding key.
        """
        headers = kwargs['headers']
        task_id = headers.get('id')

        defaults = {
            'task_name': headers.get('task'),
            'task_args': headers.get('argsrepr'),
            'task_kwargs': headers.get('kwargsrepr'),
            'content_type': 'application/json',
            'content_encoding': 'utf-8',
        }

        self.model.objects.get_or_create(task_id=task_id, defaults=defaults)
