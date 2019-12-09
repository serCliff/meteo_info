from utils.file_utils import import_from_files
from utils.gsod_utils import make_gsod_df_from_file_fwf
from utils.decorators import printed, timing
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

    return values[0] < incorrect, values[1] < incorrect


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

    mapped = map(correct_indexes_from_df, data_list)
    return len(list(filter(lambda x: x[0] and x[1], list(mapped))))


@printed
def ej2(dataframe):
    """
    La estación con menor número de datos correctos.

    Arguments:
        dataframe {Dataframe} -- Dataframe del que se obtendrá la información

    Returns:
        ({int},{int}) -- Estación, Número de datos
    """


    data_list = dataframe.loc[:, ['id_stat',
                                  'temperature',
                                  'pressure']].values.tolist()
    res = list(map(lambda x: (x[0], correct_indexes_from_df((x[1], x[2]))),
                   data_list))
    res2 = list(map(lambda x: (x[0], 1) if x[1][0] and x[1][1] else (x[0], 0),
                    res))
    # TODO: Revisar reduce para que cuente sólo lo que debería
    res3 = reduce(lambda x, y: (x[0], x[1] + y[1]) if x[0] == y[0], res2)
    # min_general_correct_values = len(dataframe.index)
    # stat_with_min_correct_values = 0
    # return (stat_with_min_correct_values, min_general_correct_values)


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
