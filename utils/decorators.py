from pprint import pprint
import os
import logging

_logger = logging.getLogger()


def printed(func):
    """Decorator used to print the result of a function
    """
    def wrapped(*args):
        res = func(*args)
        if isinstance(res, dict or list):
            pprint(res)
        else:
            print(res)
        return res
    return wrapped


def check_if_file_exists(func):
    """Check if file exists
    """
    def wrapped(*args):
        res = func(*args)
        if os.path.isfile(res):
            return res
        else:
            res = "The file not exists {}".format(res)
            _logger.error(res)
            raise Exception(res)
    return wrapped
