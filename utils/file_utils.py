"""
Conjunto de herramientas para el tratamiento de ficheros

Autor: Sergio del Castillo Baranda - 2019

Funciones:

    get_module_path -- Obtiene la ruta del módulo

    get_files_path -- Obtiene la ruta de la carpeta files

    import_from_files(fichero) -- Importa un fichero de files

    get_conf_path -- Obtiene la carpeta conf

    get_logger_conf -- Obtiene el fichero de configuracion

    get_log_path -- Obtiene ruta para un log y la situa en
                    una carpeta llamada log

"""
from meteo_info.utils.decorators import check_if_file_exists
import os
import logging

logger = logging.getLogger()


def _get_module(_path):
    """Get the current dirname until gets meteo_info

    Arguments:
        _path {str} -- Current path

    Returns:
        {str} -- The path of the meteo_info
    """
    if os.path.basename(_path) == 'meteo_info':
        return _path
    else:
        return _get_module(os.path.dirname(_path))


def get_module_path():
    """Returns the exactly path of the module independent where we are

    Returns:
        {str} -- Path of meteo_info in your computer
    """
    return _get_module(os.path.dirname(__file__))


def get_files_path():
    """Return the files path

    Returns:
        {str} -- Files path
    """
    os.path.abspath(__file__)
    return os.path.join(get_module_path(), 'files')


@check_if_file_exists
def import_from_files(filename):
    """Return the path of the filename placed on meteo_info/files/

    Arguments:
        filename {str} -- Name of file

    Returns:
        {str} -- Path of the filename placed on .../meteo_info/files/
    """
    res = os.path.join(get_files_path(), filename)
    logger.info("Importing {} from files".format(filename))
    return res


def get_conf_path():
    """Return the conf path

    Returns:
        {str} -- .../meteo_info/conf/ path
    """
    return os.path.join(get_module_path(), 'conf')


def get_logger_conf():
    """Returns the logger configuration file

    Returns:
        {str} -- Path of logger.yaml
    """
    return os.path.join(get_conf_path(), 'logger.yaml')


@check_if_file_exists
def get_log_path():
    """Return the log path to be used always the same

    Returns:
        {str} -- Path of app.log
    """
    return os.path.join(os.path.join(get_module_path(), 'log'), 'app.log')
