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
from utils.file_utils import check_file_extension
import pandas
import logging

logger = logging.getLogger()

GSOD_DATA_FWF = {
    'id_stat': 0,
    'date': 2,
    'temperature': 3,
    'pressure': 7,
}


def make_gsod_df_from_file_fwf(filepath):
    """Genera un dataframe con los datos de un fichero de tipo gsod
    almacenados en un fichero existente en filepath

    Se hicieron 4 pruebas:

        - 1ª Generando un dict y al acabar generar dataframe
        - 2ª Generando un dataframe directamente
        - 3ª Generando multiples dict y pasándolo a dataframe en partes
        - 4ª Utilizando la herramienta read_fwf de pandas

    Conclusión:

        Se utilizó la 3ª porque la 1ª consumía demasiada ram con archivos
        demasiado grandes y la 2ª consumía demasiado tiempo en la lectura
        (el doble que la primera). Con la tercera a penas aumentamos un
        poco el tiempo y la ram está mucho más liberada. Sin embargo, la
        cuarta opción acaba siendo la más óptima, consume poca
        ram, tarda el doble en leer los registros pero a su favor tarda menos
        en realizar las operaciones ejecutadas sobre el dataframe.


    Arguments:
        filepath {str} -- Ruta del fichero gsod con el que trabajar
    Returns:
        {Dataframe} -- Pandas dataframe con la info del fichero
    """
    check_file_extension(filepath)
    logger.info("Leyendo archivo {}".format(filepath))
    my_df = pandas.read_fwf(filepath, header=None)
    df = my_df.loc[:, list(GSOD_DATA_FWF.values())]
    df.columns = GSOD_DATA_FWF.keys()
    df['date'] = pandas.to_datetime(df['date'], format="%Y%m%d")
    logger.info("Dataframe obtenido correctamente.")

    return df
