"""
Shaka
Formularios de registro
Inarixdono
"""

from libreria import Mis
from selenium.webdriver.common.keys import Keys
from funciones import lista
from database import *

rutas_01 = lista('ruta','ard001','id', 'paths')

class Identification(Mis):
    
    def __header(self, navigator: str, date: str, user: str, record: str, fapps: str, gender: int, age: int):
        
        self.paciente_index = HIVPatient(user, gender, age, record, fapps, True)

        self.acceder('https://pactbrmis.org/DataEntry/household_identification.aspx?ids_id=')
        self.seleccionar(rutas_01[0], 1, wait= True) # Ong
        self.seleccionar(rutas_01[1], 1, wait= True) # Sai
        self.send_keys(rutas_01[2], navigator) # Navegador
        self.enviar_fecha(rutas_01[3], date, True) # Fecha
        self.send_keys(rutas_01[4], self.paciente_index.name[0], ' ', self.paciente_index.surname[0]) # Usuario
        self.send_keys(rutas_01[5], record) # Record
        self.send_keys(rutas_01[6], fapps) # ID Fapps
        self.seleccionar(rutas_01[7], gender, wait= True) # Sexo

    def __step_1(self, place: int, has_children = True, enrolled = False):

        self.seleccionar(rutas_01[8], place, wait= True) #P1
        self.send_keys(rutas_01[9], Keys.UP * (self.paciente_index.age - 14)) #P2
        self.seleccionar(rutas_01[10], 1, wait= True)
        self.seleccionar(rutas_01[11], 1, wait= True)

        for i in range(3):
            p4b = self.elemento(f'//*[@id="MainContent_lstHaitianDescentCategory_{i}"]')
            p4b.click()
            self.esperar_recarga(p4b)

        if self.paciente_index.age > 17:
            underaged = False
            self.seleccionar(rutas_01[13], 2, wait= True)
        else:
            underaged = True
            self.seleccionar(rutas_01[13], 1, wait= True)
            r = input('Seleccione la categoria: ')
            self.seleccionar(rutas_01[14], r, wait= True)
            has_children = False

        if not underaged:
            if has_children: self.seleccionar(rutas_01[15], 1, wait= True)
            else: self.seleccionar(rutas_01[15], 2, wait= True)

        if not enrolled: self.seleccionar(rutas_01[16], 2, wait= True)
        else: self.seleccionar(rutas_01[16], 1, wait= True)

    def __step_2(self, consent = True):

        if consent:
            self.seleccionar(rutas_01[17], 1, wait= True)
            self.paciente_index.home_code = self.elemento(rutas_01[20]).get_attribute('value')
        else:
            self.seleccionar(rutas_01[17], 2, wait= True)
            r = input('Razon por la que no quiere entrar al proyecto: ')
            self.elemento(f'//*[@id="MainContent_lstnonConsentReason_{r}"]')
            if r == '3':
                r = input('Otra razón, especifique: ')
                self.enviar_otro(rutas_01[18],rutas_01[19], r)
            
        #TODO: AGREGAR BOTON DE GUARDAR
    
    def main_test():
        sesion = Identification()
        sesion.__header('asdad','05/07/2023', 'Horacio vaque', '585', '25565', 1, 24)
        sesion.__step_1(1)
        sesion.__step_2()
        sesion.cerrar()

del rutas_01
rutas_03 = lista('ruta','ard003','id', 'paths')

class Register(Identification):

    def __init__(self, new = True, home = '', name = '', gender = 0, age = 0, record = '', fapps = ''):
        self.acceso = Database('hogar')
        if not new:
            self.paciente_index = HIVPatient(name, gender, age, record, fapps)
            self.paciente_index.home_code = home
        super().__init__()
    
    def header(self, gestor, community, verification_date):

        address = self.acceso.return_comunidad(community)
        self.verification_date = verification_date
        self.acceder('https://pactbrmis.org/DataEntry/household_register.aspx?hh_id=')

        self.seleccionar_hogar(rutas_03[0], self.paciente_index.home_code)
        self.seleccionar(rutas_03[2], 4, wait= True) # Sai
        self.seleccionar(rutas_03[3], 1) # Supervisor
        self.seleccionar(rutas_03[4], gestor) # Gestor

        self.seleccionar_hogar(rutas_03[5], address[3]) # Provincia
        self.seleccionar_hogar(rutas_03[6], address[2]) # Municipio
        self.seleccionar(rutas_03[7], address[1], 'texto', True) # Distrito
        self.seleccionar(rutas_03[8], address[0], 'texto', True) # Comunidad

        self.send_keys(rutas_03[9], (self.paciente_index.name[0], ' ', self.paciente_index.surname[0])) # Usuario
        self.enviar_fecha(rutas_03[10], self.verification_date) # Fecha de verificacion

    def contact_mode(self, r: tuple):

        self.seleccionar(rutas_03[11], str(r[0]), 'texto', True) # P1
        self.seleccionar(rutas_03[12], str(r[1]), 'texto', True)
        self.seleccionar(rutas_03[13], r[2], wait= True)

        match r[2]:
            case 1: self.seleccionar(rutas_03[14], r[3], wait= True)
            case 2: self.seleccionar(rutas_03[15], r[3], wait= True)
    
    def step_1(self, principal_caregiver: bool, location: int, proxima_cita, pcg_name = ''):

        self.send_keys(rutas_03[16], Keys.UP * (self.paciente_index.age - 14)) # P6
        self.seleccionar(rutas_03[17], 1, wait= True) # P7
        self.seleccionar(rutas_03[18], 1, wait= True) # P8

        for i in range(3): # P8b
            p8b = self.elemento(f'//*[@id="MainContent_lstHaitianDescentCategory_{i}"]')
            p8b.click()
            self.esperar_recarga(p8b)

        if self.paciente_index.age > 17: # P9
            underaged = False
            self.seleccionar(rutas_03[19], 2, wait= True)
        else:
            underaged = True
            self.seleccionar(rutas_03[19], 1, wait= True)
            r = input('Seleccione la categoria: ')
            self.seleccionar(rutas_03[20], r, wait= True)

        if not underaged: # P10
            self.seleccionar(rutas_03[21], 1, wait= True)

        if principal_caregiver: # P13
            self.principal_caregiver = self.paciente_index
            self.seleccionar(rutas_03[22], 1, wait= True)

        else: # P14
            self.secondary_caregiver = self.paciente_index
            self.principal_caregiver = HomeMember(pcg_name, 0, 0)
            self.seleccionar(rutas_03[22], 2)
            self.send_keys(rutas_03[23], (self.principal_caregiver.name[0], ' ', self.principal_caregiver.surname[0]))
            self.seleccionar(rutas_03[24], 1)
        
        self.seleccionar(rutas_03[26], 1, wait= True) # P15
        self.seleccionar(rutas_03[27], location, wait= True)
        self.enviar_fecha(rutas_03[28], self.verification_date)
        #TODO: BOTON DE GUARDAR

        self.enviar_fecha(rutas_03[31], self.verification_date)
        self.enviar_fecha(rutas_03[32], proxima_cita)
        #TODO: BOTON DE GUARDAR
        

respuestas = [0, 1, 2, 1]
prueba = Register(False, 'PU/GRE/CG/0004', 'Junina Petite Home', 2, 25, '859', '85695')
prueba.header(1, 'Muñoz', '03/08/2023')
prueba.contact_mode(respuestas)
prueba.step_1(True)
prueba.cerrar()