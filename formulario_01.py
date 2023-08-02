"""
Shaka
Formularios de registro
Inarixdono
"""

from libreria import Mis
from funciones import lista
from selenium.webdriver.common.keys import Keys
from database import *

rutas_01 = lista('ruta','ard001','id', 'Rutas')

class Identification(Mis):
    
    def w_select(self, ruta, valor):
        e = self.elemento(ruta)
        self.seleccionar(ruta, valor)
        self.esperar_recarga(e)

    def header(self, navigator: str, date: str, user: str, record: str, fapps: str, gender: int):
        
        self.paciente_index = HIVPatient(user, gender, record, fapps, True)

        self.acceder('https://pactbrmis.org/DataEntry/household_identification.aspx?ids_id=')
        self.w_select(rutas_01[0], 1) # Ong
        self.w_select(rutas_01[1], 1) # Sai
        self.send_keys(rutas_01[2], navigator) # Navegador
        self.enviar_fecha(rutas_01[3], date, True) # Fecha
        self.send_keys(rutas_01[4], self.paciente_index.iniciales()[0] + ' ' + \
                       self.paciente_index.iniciales()[1]) # Usuario
        self.send_keys(rutas_01[5], record) # Record
        self.send_keys(rutas_01[6], fapps) # ID Fapps
        self.w_select(rutas_01[7], gender) # Sexo

    def step_1(self, place: int, age: int, has_children = True, enrolled = False):

        self.w_select(rutas_01[8], place) #P1
        self.send_keys(rutas_01[9], Keys.UP * (age - 14)) #P2
        self.w_select(rutas_01[10], 1)
        self.w_select(rutas_01[11], 1)

        for i in range(3):
            p4b = self.elemento(f'//*[@id="MainContent_lstHaitianDescentCategory_{i}"]')
            p4b.click()
            self.esperar_recarga(p4b)

        if age > 17:
            underaged = False
            self.w_select(rutas_01[13], 2)
        else:
            underaged = True
            self.w_select(rutas_01[13], 1)
            r = input('Seleccione la categoria: ')
            self.w_select(rutas_01[14], r)
            has_children = False

        if not underaged:
            if has_children: self.w_select(rutas_01[15], 1)
            else: self.w_select(rutas_01[15], 2)

        if not enrolled: self.w_select(rutas_01[16], 2)
        else: self.w_select(rutas_01[16], 1)

    def step_2(self, consent = True):
        if consent:
            self.w_select(rutas_01[17], 1)
        else:
            self.w_select(rutas_01[17], 2)
            r = input('Razon por la que no quiere entrar al proyecto: ')
            self.elemento(f'//*[@id="MainContent_lstnonConsentReason_{r}"]')
            if r == '3':
                r = input('Otra razón, especifique: ')
                self.enviar_otro(rutas_01[18],rutas_01[19], r)
            
        #TODO: AGREGAR BOTON DE GUARDAR
    

