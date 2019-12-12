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
        _logger.info(res)
        if isinstance(res, (dict, list)):
            pprint(res)
            elms = "{} elementos.".format(len(res))
            print(elms)
            _logger.info(elms)
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
        text_timing = "Tiempo de ejecución de " \
                      "{} -> {}".format(func.__name__, total)
        print(text_timing)
        _logger.info(text_timing)
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
