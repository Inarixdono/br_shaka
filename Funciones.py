# Funciones externas a las clases del MIS

import pandas as pd


def lista(columna, nombre = 'Servir', index='ID', carpeta = 'Archivos'):
    lista = pd.read_csv(f'{carpeta}\{nombre}.csv',delimiter=';', index_col= index, dtype= str)[columna].tolist()
    return lista

def regular_answers(r):
    if r == 'ns': return 'No sabe'
    elif r == 'nr': return 'No respuesta'
    elif r == 'na': return 'No acepta su condicion'
    


#TODO: funcion para verificar que no se le marque ARV `1.9` a beneficiarios que no sean VIH+
#TODO: funcion para verificar personas salidas no firmen ni reciban servicio individual