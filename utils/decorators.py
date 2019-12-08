from pprint import pprint
from datetime import datetime
import os
import logging

_logger = logging.getLogger()


def printed(func):
    """Decorador usado para imprimir el resultado de una función
    """
    def wrapped(*args, **kwargs):
        _logger.info("Ejecutando {}".format(func.__name__))
        print(func.__name__)
        print(func.__doc__)
        res = func(*args, **kwargs)
        if isinstance(res, dict or list):
            pprint(res)
        else:
            print(res)
        print("==============================================================")
        return res
    return wrapped


def timing(func):
    """Calcula el tiempo de ejecución de una función
    """
    def wrapped(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        end = datetime.now()
        total = end - start
        _logger.info("Tiempo de ejecución de "
                     "{} -> {}".format(func.__name__, total))
        return res
    return wrapped


def check_if_file_exists(func):
    """Check if file exists
    """
    def wrapped(*args, **kwargs):
        res = func(*args, **kwargs)
        if os.path.isfile(res):
            return res
        else:
            res = "The file not exists {}".format(res)
            _logger.error(res)
            raise Exception(res)
    return wrapped
