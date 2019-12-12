from utils.file_utils import import_from_files
from utils.gsod_utils import make_gsod_df_from_file_fwf
from utils.decorators import printed, timing
from itertools import groupby
from functools import reduce
import calendar
from datetime import datetime
import pandas
import logging

logger = logging.getLogger()


def correct_indexes_from_df(values, incorrect=9999.9):
    """Obtiene del dataframe el conjunto de índices correctos

    - Un dato es correcto si no es 9999.9
    - Si se desea utilizar otro filtro, introducir por argumento
        otro valor

    Las columnas comprobadas son 'temperature' y 'pressure'

    Arguments:
        values ({float}, {float}) -- Datos que serán filtrados

    Keyword Arguments:
        incorrect {float} -- Filtro cuando un valor es incorrecto
                             (default: {9999.9})

    Returns:
        ({Bool}, {Bool}) -- En cada campo comprobará si el dato es correcto
    """
    res = 1 if values[0] < incorrect and values[1] < incorrect else 0
    return res


@printed
def ej1(dataframe):
    """
    Número de filas con datos de temperatura y presión (ambos) correctos.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        {int} -- Número de filas con datos correctos
    """
    data_list = dataframe.loc[:, ['temperature', 'pressure']].values.tolist()

    mapped_data = list(map(correct_indexes_from_df, data_list))
    return len(list(filter(lambda x: x, mapped_data)))


@printed
def ej2(dataframe):
    """
    La estación con menor número de datos correctos.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        [({int},{int})] -- Estación, Número de datos
    """
    # Mapeado de estaciones correctas e incorrectas
    data_list = dataframe.loc[:, ['id_stat',
                                  'temperature',
                                  'pressure']].values.tolist()
    res_per_stat = list(map(lambda x:
                        (int(x[0]), correct_indexes_from_df((x[1], x[2]))),
                        data_list))
    # Agrupando por estación, obtengo los totales
    total_grouped = [reduce(lambda x, y: (x[0], x[1] + y[1]), stat)
                     for _, stat in groupby(sorted(res_per_stat),
                                            lambda x: x[0])]

    # Obtengo el valor menor
    min_value = min([value[1] for value in total_grouped])

    # Filtro por los valores menores encontrado
    return list(filter(lambda x: x[1] == min_value, total_grouped))


@printed
def ej3(dataframe):
    """
    Por cada estación, el máximo y el mínimo de temperatura registrada.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        [(id_stat, max, min)] -- Lista con max y min por stat
    """
    data_list = dataframe.loc[:, ['id_stat',
                                  'temperature']].values.tolist()

    # Mapeo valores de temperaturas (temp, max, min)
    total_mapped = list(map(lambda x: (int(x[0]), x[1], x[1]), data_list))

    # Agrupo obteniendo el maximo y minimo de cada estacion
    total_grouped = [reduce(lambda x, y: (x[0],
                                          max(x[1], y[1]),
                                          min(x[2], y[2])), stat)
                     for _, stat in groupby(sorted(total_mapped),
                                            lambda x: x[0])]
    return total_grouped


@printed
def ej4(dataframe):
    """
    Por cada mes y estación la temperatura máxima y mínima registrada

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        [(id_stat, date, max, min)] -- Lista con max y min por stat y fecha
    """
    data_list = dataframe.loc[:, ['id_stat',
                                  'date',
                                  'temperature']].values.tolist()

    # Mapeo valores de temperaturas (temp, max, min)
    total_mapped = list(map(lambda x: (int(x[0]),
                                       x[1].strftime("%m/%Y"),
                                       x[2],
                                       x[2]), data_list))

    # Agrupo obteniendo el maximo y minimo de cada estacion
    total_grouped = [reduce(lambda x, y: (x[0],
                                          x[1],
                                          max(x[2], y[2]),
                                          min(x[3], y[3])), stat)
                     for _, stat in groupby(sorted(total_mapped),
                                            lambda x: x[0] and x[1])]
    return total_grouped


@timing
def map_reduce_final(filepath='sample.txt', from_files=True):
    logger.info("Ejecutando práctica final usando "
                "funcionalidad de (MAP-REDUCE)...")

    weather_file_path = filepath
    if from_files:
        weather_file_path = import_from_files(filepath)

    df = make_gsod_df_from_file_fwf(weather_file_path)
    ej1(df)
    ej2(df)
    ej3(df)
    ej4(df)
