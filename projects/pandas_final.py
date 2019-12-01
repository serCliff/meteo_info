from meteo_info.utils.file_utils import import_from_files
from meteo_info.utils.gsod_utils import make_gsod_df_from_file
from meteo_info.utils.decorators import printed
import logging

logger = logging.getLogger()


def correct_indexes_from_df(df, incorrect=9999.9):
    """Obtiene del dataframe el conjunto de índices correctos

    - Un dato es correcto si no es 9999.9
    - Si se desea utilizar otro filtro, introducir por argumento
        otro valor

    Las columnas comprobadas son 'temperature' y 'pressure'

    Arguments:
        df {Dataframe} -- Datos que serán filtrados

    Keyword Arguments:
        incorrect {float} -- Filtro cuando un valor es incorrecto
                             (default: {9999.9})

    Returns:
        {list} -- Lista de índices del dataframe que son correctos
    """
    return df[(df['temperature'] < incorrect) &
              (df['pressure'] < incorrect)].index


@printed
def ej1(dataframe):
    """
    Número de filas con datos de temperatura y presión (ambos) correctos.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información
    
    Returns:
        {int} -- Número de filas con datos correctos
    """
    return len(correct_indexes_from_df(dataframe))


@printed
def ej2(dataframe):
    """
    La estación con menor número de datos correctos.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        ({int},{int}) -- Estación, Número de datos
    """

    min_general_correct_values = len(dataframe.index)
    stat_with_min_correct_values = 0
    # Recorremos todas las estaciones
    for stat in dataframe['id_stat'].unique():
        stat_df = dataframe[dataframe['id_stat'] == stat]
        min_stat_incorrect = len(correct_indexes_from_df(stat_df))
        # Almacenamos la estación con menor número de datos correctos
        if min_stat_incorrect < min_general_correct_values:
            min_general_correct_values = min_stat_incorrect
            stat_with_min_correct_values = stat
    return (stat_with_min_correct_values, min_general_correct_values)


def ej3(dataframe):
    """
    Por cada estación, el máximo y el mínimo de temperatura registrada.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información
    """
    pass


def ej4(dataframe):
    """
    Por cada mes y estación la temperatura máxima y mínima registrada

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información
    """
    pass


def pandas_final(filename='sample.txt'):
    logger.info("Ejecutando práctica final...")
    weather_file = import_from_files(filename)

    df = make_gsod_df_from_file(weather_file)
    ej1(df)
    ej2(df)
