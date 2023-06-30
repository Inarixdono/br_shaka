# Funciones externas a las clases del MIS

from pandas import read_csv

def lista(columna, nombre = 'Servir', index='ID'):
    lista = read_csv(f'Archivos\{nombre}.csv',delimiter=';', index_col= index, dtype= str)[columna].tolist()
    return lista