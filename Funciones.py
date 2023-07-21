# Funciones externas a las clases del MIS

import pandas as pd
import mysql.connector as bd
from credentials import PASS

def lista(columna, nombre = 'Servir', index='ID'):
    lista = pd.read_csv(f'Archivos\{nombre}.csv',delimiter=';', index_col= index, dtype= str)[columna].tolist()
    return lista

def regular_answers(r):
    if r == 'ns': return 'No sabe'
    elif r == 'nr': return 'No respuesta'
    elif r == 'na': return 'No acepta su condicion'
    
class Database():
    def __init__(self, table):
        self.table = table
        self.connect = bd.connect(user='root', password= PASS, database='br', host= 'localhost', port='3307')
        self.cursor = self.connect.cursor()

    def return_id_vih(self, value):
        self.cursor.execute(f'SELECT id_vih FROM vih\
                            INNER JOIN beneficiario ON vih.id_beneficiario = beneficiario.id_beneficiario\
                            WHERE beneficiario.codigo_unico = "{value}"')
        return self.cursor.fetchone()[0]
    
    def return_id_hogar(self, value):
        self.cursor.execute(f'SELECT id_hogar FROM hogar WHERE	hogar = "{value}"')
        return self.cursor.fetchone()[0]

    def insert(self, campos, values):
        self.cursor.execute(f'INSERT INTO {self.table}({campos}) VALUES({values})')
        self.commit()

    def commit(self):
        self.connect.commit()

    def close_connection(self):
        self.connect.close()

#TODO: funcion para verificar que no se le marque ARV `1.9` a beneficiarios que no sean VIH+
#TODO: funcion para verificar personas salidas no firmen ni reciban servicio individual