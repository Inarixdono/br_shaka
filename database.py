"""
Shaka
Base de datos
Inarixdono
"""

import mysql.connector as bd
from credentials import PASS

class Home:
    id_gestor: int
    id_hogar: int
    home_code: str

class HomeMember:

    def __init__(self, argname: str, argender: int):
        self.id_hogar: int
        self.name: str = argname
        self.gender: int = argender
        self.rol: int
        self.age: int
        self.birth_date: str
        self.member_code: str

    def iniciales(self):
        r = self.name.split(' ')
        return r[0][0], r[1][0]
    

class HIVPatient(HomeMember):
    def __init__(self, argname, argender, argrecord, argfapps, argindex = False):
        self.index : bool = argindex
        self.record: str = argrecord
        self.fapps: str = argfapps
        super().__init__(argname, argender)



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