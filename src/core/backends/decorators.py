import logging

logger = logging.getLogger('django')


def logging_sending_errors(func):
    def wrapper(*args):
        _self = args[0]
        try:
            return func(*args)
        except Exception as e:
            logger.error('{} ERROR {}'.format(_self.__class__.__name__, e.__repr__()))

    return wrapper
