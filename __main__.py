"""
Módulo que trabaja con datos libres de meteorología
===================================================

Creado como trabajo de fin del módulo de python del máster Big Data UCM

Autor: Sergio del Castillo Baranda - 2019

"""
from meteo_info.utils.file_utils import get_logger_conf
from meteo_info.projects.pandas_final import pandas_final

import logging.config
import yaml


with open(get_logger_conf()) as f:
    conf = yaml.safe_load(f.read())
    logging.config.dictConfig(conf)


if __name__ == '__main__':
    pandas_final()
