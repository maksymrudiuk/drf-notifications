import logging
import traceback

logger = logging.getLogger('django')


def logging_sending_errors(func):
    def wrapper(*args):
        _self = args[0]
        try:
            return func(*args)
        except Exception as e:
            logger.error('{} ERROR {}'.format(_self.__class__.__name__, e.__repr__()))
            raise e
            # traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            # traceback.print_tb(traceback_str)

    return wrapper
