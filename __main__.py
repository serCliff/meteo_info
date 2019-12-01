"""
Módulo que trabaja con datos libres de meteorología
===================================================

Creado como trabajo de fin del módulo de python del máster Big Data UCM

Autor: Sergio del Castillo Baranda - 2019

"""
from meteo_info.utils.utils import get_logger_conf
from meteo_info.projects.final import final

import logging.config
import yaml


with open(get_logger_conf()) as f:
    conf = yaml.safe_load(f.read())
    logging.config.dictConfig(conf)


if __name__ == '__main__':
    final()
