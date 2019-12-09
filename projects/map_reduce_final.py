from ..utils.file_utils import import_from_files
from ..utils.gsod_utils import make_gsod_df_from_file_fwf
from ..utils.decorators import printed, timing
import calendar
from datetime import datetime
import pandas
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


@printed
def ej3(dataframe):
    """
    Por cada estación, el máximo y el mínimo de temperatura registrada.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        ({Dataframe}) -- Dataframe con max y min por stat
    """
    import pandas
    df_res = pandas.DataFrame(columns=['id_stat', 'max', 'min'])
    index = 0
    colname = 'temperature'
    for stat in dataframe['id_stat'].unique():
        stat_df = dataframe[dataframe['id_stat'] == stat]
        max_value = dataframe.iloc[stat_df[colname].idxmax()][colname]
        min_value = dataframe.iloc[stat_df[colname].idxmin()][colname]
        df_res.loc[index] = [stat, max_value, min_value]
        index += 1
    return df_res


@printed
def ej4(dataframe):
    """
    Por cada mes y estación la temperatura máxima y mínima registrada

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información
    """
    df_res = pandas.DataFrame(columns=['id_stat', 'date', 'max', 'min'])

    distinct_dates = dataframe['date'].dt.strftime("%m/%Y"). \
        drop_duplicates().unique().tolist()

    index = 0
    colname = 'temperature'
    # Recorremos todos los meses diferentes
    for date in distinct_dates:
        month, year = date.split("/")
        last_day = calendar.monthrange(int(year), int(month))[1]
        start_date = datetime.strptime(date, "%m/%Y")
        last_date = start_date.replace(day=last_day)

        df = dataframe[(dataframe['date'] > start_date) &
                       (dataframe['date'] <= last_date)]
        # En esta fecha, recorremos las estaciones y obtenemos su máximo
        #  y mínimo
        for stat in df['id_stat'].unique():
            stat_df = dataframe[dataframe['id_stat'] == stat]
            max_value = dataframe.iloc[stat_df[colname].idxmax()][colname]
            min_value = dataframe.iloc[stat_df[colname].idxmin()][colname]
            df_res.loc[index] = [stat, date, max_value, min_value]
            index += 1

    return df_res


@timing
def pandas_final(filepath='sample.txt', from_files=True):
    logger.info("Ejecutando práctica final (MAP-REDUCE)...")

    weather_file_path = filepath
    if from_files:
        weather_file_path = import_from_files(filepath)

    df = make_gsod_df_from_file_fwf(weather_file_path)
    ej1(df)
    ej2(df)
    ej3(df)
    ej4(df)
