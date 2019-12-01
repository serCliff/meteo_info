from meteo_info.utils.decorators import check_if_file_exists
import os
import logging

logger = logging.getLogger()


def make_random_fractions_file():
    """Make a fractions file with pairs of fractions placed on rows delimited by ;
    """
    import random as rd
    current_path = os.path.join(os.getcwd(), 'files')
    fractions_file = os.path.join(current_path, 'fractions.txt')
    with open(fractions_file, 'w') as f:
        for _ in range(0, rd.randrange(20)):
            f.write(str(rd.randint(1, 20))+";"+str(rd.randint(1, 20))+"\n")
    logger.info("Made fractions file on {}".format(fractions_file))


def get_fractions():
    """Make a list of random fractions elements

    The fractions have the next style:

    If:

        1/2 => [1, 2]

    Then:

        1/2, 2/3, 5/2, ... => [[1, 2], [2, 3], [5, 2], ...]

    Returns:
        {list} -- List of random fractions
    """
    make_random_fractions_file()
    current_path = get_files_path()
    fractions_file = os.path.join(current_path, 'fractions.txt')

    fractions = list()
    with open(fractions_file, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(";")
            fractions.append([int(line[0]), int(line[1])])
        # frac = map(lambda x: x.strip().split(";"), lines)
        # frac = map(lambda x: list(map(int, x)), frac)
        # frac = list(frac)
    logger.info("Getting fractions")
    return fractions


def get_module(_path):
    """Get the current dirname until gets meteo_info

    Arguments:
        _path {str} -- Current path

    Returns:
        {str} -- The path of the meteo_info
    """
    if os.path.basename(_path) == 'meteo_info':
        return _path
    else:
        return get_module(os.path.dirname(_path))


def get_module_path():
    """Returns the exactly path of the module independent where we are

    Returns:
        {str} -- Path of meteo_info in your computer
    """
    return get_module(os.path.dirname(__file__))


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
