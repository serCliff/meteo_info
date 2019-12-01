from meteo_info.utils.decorators import printed
from meteo_info.utils.utils import import_from_files
from datetime import datetime
import pandas
import numpy as np
import os
import logging

logger = logging.getLogger()

ID_STAT = {
    'begin': 0,
    'final': 6,
    'type': 'int',
}
DATE = {
    'begin': 14,
    'final': 22,
    'type': 'date',
}
TEMP = {
    'begin': 25,
    'final': 30,
    'type': 'float',
}
PRESSURE = {
    'begin': 46,
    'final': 52,
    'type': 'float',
}

GSOD_DATA = {
    'id_stat': ID_STAT,
    'date': DATE,
    'temperature': TEMP,
    'pressure': PRESSURE,
}


def parser(value, vtype):
    if vtype == 'int':
        return int(value)
    elif vtype == 'float':
        return float(value)
    elif vtype == 'date':
        return datetime.strptime(value, "%Y%m%d")
    else:
        raise Exception("Value cant be parsed")


def get_gsod_row(dictdata, rowdata):
    # global GSOD_DATA
    for key, value in GSOD_DATA.items():
        rdata = rowdata[value['begin']:value['final']]
        rdata = parser(rdata.strip(), value['type'])
        if key not in dictdata:
            dictdata[key] = [rdata]
        else:
            dictdata[key].append(rdata)


def make_gsod_df_from_file(filepath):
    info = dict()
    with open(filepath, 'r') as f:
        for rowdata in f.readlines():
            get_gsod_row(info, rowdata)
    return pandas.DataFrame(info)


def make_header(df, header):
    df.columns = header


def final():
    logger.warning("Ejecutando práctica final...")
    weather_file = import_from_files('sample.txt')

    df = make_gsod_df_from_file(weather_file)
    print(df)

    # df = pandas.read_csv(weather_file, delimiter="\t", header=None)

    # # df = pandas.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])
    # parser('123.5', 'float')
    # ej = dict()
    # get_gsod_row(ej, '101930 99999  19430429    49.8  5    41.0  5  1013.9  5  9999.9  0    9.9  5    9.8  5   13.0  999.9    57.0*   36.0* 99.99  999.9  010000')
    # get_gsod_row(ej, '101930 99999  19430429    49.8  5    41.0  5  1013.9  5  9999.9  0    9.9  5    9.8  5   13.0  999.9    57.0*   36.0* 99.99  999.9  010000')

    # print(ej)
    print(df['id_stat'].idxmax())
    # print(df.loc[maxi])
    # print(df[df['F'] != 9999.9])
    # print(df[df.iloc[:, 5] != 9999.9])
    # print(df.iloc[:, 5])
