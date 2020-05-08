import logging

logger = logging.getLogger('django')


def warning_expiremental(func):
    def wrapper(*args):
        logger.warning('Expiremental functional')
        return func(*args)

    return wrapper
