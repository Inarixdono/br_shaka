# Funciones externas a las clases del MIS

import pandas as pd

def lista(columna, nombre = 'Servir', index='ID', carpeta = 'Archivos'):
    lista = pd.read_csv(
        f'{carpeta}\{nombre}.csv',
        delimiter=';',
        index_col= index,
        dtype= str)[columna].tolist()
    return lista

def regular_answers(r):
    match r:
        case 'ns':
            return 'No sabe'
        case 'nr':
            return 'No respuesta'
        case 'na':
            return 'No acepta su condicion'
    


#TODO: make a function which verifies not to mark 1.9 to VIH- beneficiaries
#TODO: funcion para verificar personas salidas no firmen ni reciban servicio individual