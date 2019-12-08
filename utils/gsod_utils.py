"""
Conjunto de métodos que facilitan el trabajo con ficheros tipo gsod

Autor: Sergio del Castillo Baranda - 2019

Datos:

    GSOD_DATA: Diccionario con la estructura de los elementos
                necesarios del fichero gsod

Funciones:

    parser(valor, tipo) -- Función que parsea un valor str a un objeto
                especificado en el tipo

    get_gsod_row(diccionario, línea) -- Método que introduce la
                info de una línea de un archivo gsod en un diccionario

    make_gsod_df_from_file(ruta) -- Genera un dataframe de un fichero
                gsod almacenado en la ruta

"""
from utils.file_utils import check_if_file_exists
from utils.file_utils import check_file_extension
from datetime import datetime
import pandas
import numpy as np
import logging

logger = logging.getLogger()

_ID_STAT = {
    'begin': 0,
    'final': 6,
    'type': 'int',
}
_DATE = {
    'begin': 14,
    'final': 22,
    'type': 'date',
}
_TEMP = {
    'begin': 25,
    'final': 30,
    'type': 'float',
}
_PRESSURE = {
    'begin': 46,
    'final': 52,
    'type': 'float',
}

GSOD_DATA = {
    'id_stat': _ID_STAT,
    'date': _DATE,
    'temperature': _TEMP,
    'pressure': _PRESSURE,
}


def parser(value, vtype):
    """Parsea un valor al tipo definido

    Arguments:
        value {str} -- Valor para parsear
        vtype {str} -- Tipo para parsear

    Raises:
        Exception: Lanza un error si el tipo no puede ser parseado

    Returns:
        {str,int,date} -- Valor formateado
    """
    try:
        if vtype == 'int':
            return int(value)
        elif vtype == 'float':
            return float(value)
        elif vtype == 'date':
            return datetime.strptime(value, "%Y%m%d")
        else:
            raise
    except Exception as e:
        logger.error(e)
        raise Exception("Valor {0} no puede ser "
                        "parseado a {1}".format(value, vtype))


def get_gsod_row(dictdata, rowdata):
    """Rellena el diccionario con la información de una línea de un fichero gsod
    Arguments:
        dictdata {dict} -- Diccionario a rellenar
        rowdata {str} -- Línea con formato gsod
    """
    # global GSOD_DATA
    for key, value in GSOD_DATA.items():
        rdata = rowdata[value['begin']:value['final']]
        rdata = parser(rdata.strip(), value['type'])
        if key not in dictdata:
            dictdata[key] = [rdata]
        else:
            dictdata[key].append(rdata)


def make_gsod_df_from_file(filepath):
    """Genera un dataframe con los datos de un fichero de tipo gsod
    almacenados en un fichero existente en filepath

    Se hicieron 3 pruebas:

        - 1ª Generando un dict y al acabar generar dataframe
        - 2ª Generando un dataframe directamente
        - 3ª Generando multiples dict y pasándolo a dataframe en partes

    Conclusión:

        Se utilizó la 3ª porque la 1ª consumía demasiada ram con archivos
        demasiado grandes y la 2ª consumía demasiado tiempo en la lectura
        (el doble que la primera). Con la tercera a penas aumentamos un 
        poco el tiempo y la ram está mucho más liberada.


    Arguments:
        filepath {str} -- Ruta del fichero gsod con el que trabajar
    Returns:
        {Dataframe} -- Pandas dataframe con la info del fichero
    """
    check_file_extension(filepath)
    logger.info("Leyendo archivo {}".format(filepath))

    info = dict()
    df = pandas.DataFrame(columns=GSOD_DATA.keys())

    with open(filepath, 'r') as f:
        lines = f.readlines()
        total = len(lines)
        dict_size = int(total*0.1)
        index = 0
        for rowdata in lines:
            get_gsod_row(info, rowdata)
            if index % dict_size == 0 or index == total-1 or index == 0:
                a = pandas.DataFrame(info, columns=GSOD_DATA.keys())
                df = df.append(a)
                info = dict()
                index += 1
                per = round(index / total * 100, 2)
                logger.info("Leyendo {}/{} {}%".format(index, total, per))
            else:
                index += 1
    logger.info("Dataframe obtenido correctamente.")
    return df
