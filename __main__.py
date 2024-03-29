"""
Módulo que trabaja con datos libres de meteorología
===================================================

Creado como trabajo de fin del módulo de python del máster Big Data UCM


Autor: Sergio del Castillo Baranda - 2019

"""
from utils.file_utils import get_logger_conf
from projects.pandas_final import pandas_final
from projects.map_reduce_final import map_reduce_final
import argparse

import logging.config
import yaml


with open(get_logger_conf()) as f:
    conf = yaml.safe_load(f.read())
    logging.config.dictConfig(conf)


parser = argparse.ArgumentParser(description='Ejecución de la práctica. '
                                             'Por defecto realiza la '
                                             'ejecución mediante el uso de '
                                             'la librería pandas con el '
                                             'fichero de ejemplo '
                                             'sample.txt')
parser.add_argument('-mr', '--map-reduce', dest='mr', required=False,
                    action='store_true',
                    help='Ejecutar usando funcionalidad de map y reduce')
parser.add_argument('-f', '--file', type=str, required=False,
                    help='Ruta archivo tipo gsod.txt')
args = parser.parse_args()

if __name__ == '__main__':
    fromfiles = True
    if args.file:
        fromfiles = False
        filepath = args.file
    else:
        filepath = 'sample.txt'
    if args.mr:
        map_reduce_final(filepath, from_files=fromfiles)
    else:
        pandas_final(filepath, from_files=fromfiles)
