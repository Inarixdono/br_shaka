"""
Shaka
Base de datos
Inarixdono
"""

import mysql.connector as bd
from credentials import PASS

class Home:
    def __init__(self) -> None:
        self.id_gestor: int
        self.id_hogar: int
        self.home_code: str

class HomeMember(Home):

    def __init__(self, argname: str, argender: int, argage):
        self.id_hogar: int
        self.name = argname
        self.surname = argname
        self.gender = argender # 1 = M, 2 = F
        self.rol: int
        self.age: int = argage
        self.birth_date: str
        self.member_code: str
        self.__sname()
        self.__ssurname()

    def __sname(self):
        self.name = [self.name[0], self.name.split(' ')[0]]

    def __ssurname(self):
        nsurname = ''
        ssurname = ''
        for i in self.surname.split(' ')[1:]:
            nsurname += i + ' '
            ssurname += i[0]
        self.surname = [ssurname, nsurname.rstrip()]
    

class HIVPatient(HomeMember):
    def __init__(self, argname, argender, argage, argrecord, argfapps, argindex= False):
        self.index : bool = argindex
        self.record: str = argrecord
        self.fapps: str = argfapps
        super().__init__(argname, argender, argage)

class Database():
    def __init__(self, table):
        self.table = table
        self.connect = bd.connect(user='root', password= PASS,
                                  database='br', host= 'localhost', port='3307')
        self.cursor = self.connect.cursor()

    def return_id_vih(self, value: str):
        self.cursor.execute(f'SELECT return_id_vih("{value}")')
        return self.cursor.fetchone()[0]
    
    def return_id_hogar(self, value: str):
        self.cursor.execute(f'SELECT return_id_hogar("{value}")')
        return self.cursor.fetchone()[0]
    
    def return_comunidad(self, value):
        self.cursor.execute(f"SELECT comunidad.nombre AS 'Comunidad', distrito.nombre AS 'Distrito', municipio.nombre AS 'Municipio', provincia.nombre AS 'Provincia' FROM comunidad\
                              INNER JOIN distrito ON comunidad.id_distrito = distrito.id_distrito\
                              INNER JOIN municipio ON distrito.id_municipio = municipio.id_municipio\
                              INNER JOIN provincia ON municipio.id_provincia = provincia.id_provincia\
                              WHERE comunidad.nombre = '{value}'")
        return self.cursor.fetchone()

    def service_path(self, code: str):
        self.cursor.execute(f'SELECT return_service_xpath({code})')
        return self.cursor.fetchone()[0]

    def insert(self, campos, values):
        self.cursor.execute(f'INSERT INTO {self.table}({campos}) VALUES({values})')
        self.commit()

    def commit(self):
        self.connect.commit()

    def close_connection(self):
        self.connect.close()

#TODO: COMPROBAR QUE LOS PATH ESTEN FUNCIONANDO CORRECTAMENTE