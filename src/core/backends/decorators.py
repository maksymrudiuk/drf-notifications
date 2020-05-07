import logging

logger = logging.getLogger('django')


def logging_sending_errors(attr):
    def _log_send_errors(func):
        def wrapper(self, *args):
            try:
                func()
            except Exception as e:
                logger.error('{} ERROR {}'.format(self.__class__.__name__, e))
