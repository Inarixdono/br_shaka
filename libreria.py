
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from funciones import lista
from datetime import datetime
import pyperclip as ctrl
from credentials import USER, PASS

"""

Librerias que no se estan usando de momento en este archivo

import pandas as pd
import pyperclip as ctrl
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
""" 

class Mis:
    def __init__(self):
        self._hoy = datetime.now().strftime('%d/%m/%Y')
        self.driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
        self.wait = WebDriverWait(self.driver,10)
        self.driver.get("https://pactbrmis.org/Account/Login.aspx")
        self._login()
    
    def _login(self): # Iniciar sesion
        self.elemento('//*[@id="txtUsername"]').send_keys(USER)
        self.elemento('//*[@id="txtPassword"]').send_keys(PASS)
        self.elemento('//*[@id="btnLogin"]').click()

    def acceder(self,enlace):
        self.driver.get(enlace)
        
    def elemento(self, ruta):
        elemento = self.driver.find_element('xpath',ruta)
        return(elemento)
    
    def seleccionar_hogar(self, ruta, hogar):
        self.elemento(ruta).click()
        self.elemento('/html/body/span/span/span[1]/input').send_keys(hogar, Keys.ENTER)

    def enviar_fecha(self,ruta, fecha, permite_entrada = False):
        if len(fecha) <= 2: fecha = datetime.strptime(fecha + self._hoy[2:], '%d/%m/%Y').strftime('%d/%m/%Y')
        elif len(fecha) <= 5: fecha = datetime.strptime(fecha + self._hoy[5:], '%d/%m/%Y').strftime('%d/%m/%Y')
        elif len(fecha) <= 8: fecha = datetime.strptime(fecha, '%d/%m/%y').strftime('%d/%m/%Y')
        else: fecha = datetime.strptime(fecha, '%d/%m/%Y').strftime('%d/%m/%Y') # Debe medir minimo 9
        if permite_entrada: self.elemento(ruta).send_keys(fecha, Keys.ENTER)
        else: 
            ctrl.copy(fecha)
            self.elemento(ruta).send_keys(Keys.CONTROL, 'v', Keys.ENTER)

    def seleccionar(self,ruta,valor='',por='index'):

        seleccionar = Select(self.elemento(ruta))

        if por == 'index': seleccionar.select_by_index(valor)
        elif por == 'valor': seleccionar.select_by_value(valor)
        elif por == 'texto': seleccionar.select_by_visible_text(valor)
        return seleccionar
    
    def extraer_cantidad(self, ruta):
        cantidad = len(self.elemento(ruta).find_elements('tag name', 'tr')) - 1
        return cantidad

    def cerrar(self):
        self.driver.close()

    def esperar_recarga(self, referencia):
        self.wait.until(EC.staleness_of(referencia))

    def esperar_alerta(self):
        self.wait.until(EC.alert_is_present()).accept()

XPATH = lista('graduacion','XPATH')

class Graduate(Mis): 

    def tabla(self, n):
        tabla = f'//*[@id="MainContent_gvBenchmark{n}"]/tbody'
        return tabla
    
    def format_preguntas(self, n):
        # Para el punto 
        P = (f'//*[@id="MainContent_gvBenchmark8_ddlChildEnrolledInSchool_{n}"]',
            f'//*[@id="MainContent_gvBenchmark8_ddlChildAttendedSchoolRegularly_{n}"]',
            f'//*[@id="MainContent_gvBenchmark8_ddlChildProgressedToNextGrade_{n}"]',
            f'//*[@id="MainContent_gvBenchmark8_ddlPCGAnswerYesToAllBM8_{n}"]')
        return P

    def encabezado(self):
        self.acceder('https://pactbrmis.org/DataEntry/graduation_benchmark_assessment.aspx')
        self.enviar_fecha(XPATH[0], input('Fecha de evaluacion'), True)
        self.seleccionar_hogar(XPATH[1], input('Codigo del hogar'))

        previousy_assessed = input('Previamente evaluado?')
        self.seleccionar(XPATH[2], previousy_assessed)
        if str(previousy_assessed) == '1':
            self.enviar_fecha(XPATH[3], input('Fecha en que fue evaluado'), True)

    def punto_1(self):
        for i in range(self.extraer_cantidad(self.tabla(1))):
            r = input('Fecha en la que se reporta estatus')
            if r == '1': continue
            elif r == '0': break
            else:
                self.enviar_fecha(f'//*[@id="MainContent_gvBenchmark1_txtDateHIVStatusDocumented_{i}"]', r, True)
    
    def punto_2(self):
            for i in range(self.extraer_cantidad(self.tabla(2))):
                p2a = f'//*[@id="MainContent_gvBenchmark2_ddlAttendingARTAppointments_{i}"]'
                p2b = f'//*[@id="MainContent_gvBenchmark2_ddlTakingARTPillsAsPrescribed_{i}"]'
                if self.elemento(p2a).is_enabled():
                    r = input('Digitar respuestas para punto 2')
                    self.seleccionar(p2a, r[0])
                    self.seleccionar(p2b, r[1])
    
    def punto_3(self):
        beneficiarios = self.extraer_cantidad(self.tabla(3)) / 22
        if int(beneficiarios) != 0:
            for b in range(int(beneficiarios)): # Para repetir por la cantidad de beneficiarios
                respuestas = 0
                
                r = input('Pregunta 3.1')
                for i in range(len(str(r))): # Para repetir en base al input a la pregunta 3.1
                    self.elemento(f'//*[@id="MainContent_gvBenchmark3_cblWaysOfGettingHIV_{b}_{r[i]}_{b}"]').click()
                    respuestas += 1

                r = input('Pregunta 3.2')
                for i in range(len(str(r))): # Para repetir en base al input a la pregunta 3.2
                    self.elemento(f'//*[@id="MainContent_gvBenchmark3_cblWaysOfProtectingAgainstHIV_{b}_{r[i]}_{b}"]').click()
                    respuestas += 1

                r = input('Pregunta 3.3')
                for i in range(len(str(r))): # Para repetir en base al input a la pregunta 3.3
                    self.elemento(f'//*[@id="MainContent_gvBenchmark3_cblWhereHIVPreventionSupport_{b}_{r}_{b}"]').click()
                    if str(r[i]) == '4':
                        self.elemento(f'//*[@id="MainContent_gvBenchmark3_txtWhereHIVPreventionSupportOther_{b}"]')\
                            .send_keys(input('Otro'))
                    respuestas += 1
        
                if respuestas > 4:
                    self.seleccionar(f'//*[@id="MainContent_gvBenchmark3_ddlChildAwareOfHIVRisksAndPreventionMeasures_{b}"]', 1)
                else:
                    self.seleccionar(f'//*[@id="MainContent_gvBenchmark3_ddlChildAwareOfHIVRisksAndPreventionMeasures_{b}"]', 2)

    def punto_4(self):
        p4a = self.extraer_cantidad(self.tabla(4))
        p4b = self.extraer_cantidad(self.tabla('4b'))

        if p4a != 0:
            for i in range(p4a):
                self.seleccionar(f'//*[@id="MainContent_gvBenchmark4_ddlChildMUACMoreThan12_5_{i}"]', 1)
                self.seleccionar(f'//*[@id="MainContent_gvBenchmark4_ddlChildFreeOfAnySignsOfBipedalEdema_{i}"]',1)

        if p4b != 0:
            for i in range(p4b):
                print('agregar rutas') #TODO: AGREGAR RUTAS

    def punto_5(self):
        P = ('//*[@id="MainContent_ddlAbleToPayForMedicalCosts"]',
        '//*[@id="MainContent_ddlAbleToPayForMedicalCostsWithoutCashTransfer"]',
        '//*[@id="MainContent_ddlAbleToPayForMedicalCostsWithoutSellingAnything"]',
        '//*[@id="MainContent_ddlAbleToPayForSchoolSupplies"]',
        '//*[@id="MainContent_ddlAbleToPayForSchoolSuppliesWithoutFinancialAid"]',
        '//*[@id="MainContent_ddlAbleToPayForSchoolSuppliesWithoutSellingAnything"]')
        #TODO: SIMPLIFICAR
        r = input('Punto 5')
        if r == '1a':
            for i in range(6):
                try: self.seleccionar(P[i], 1)
                except NotImplementedError: break
        elif r == '2a':
            for i in range(6):
                try: self.seleccionar(P[i], 2)
                except NotImplementedError: break
        else:
            for i in range(len(str(r))):
                try: self.seleccionar(P[i],int(r[i]))
                except NotImplementedError: break

    def p6to7(self):
        P = ('//*[@id="MainContent_ddlAwareOfAnyPhysicalAbuse"]',
        '//*[@id="MainContent_ddlAwareOfAnySexualAbuse"]',
        '//*[@id="MainContent_ddlChildrenUnderCareOfStableAdultCaregiver"]')

        for i in range(3):
            if i < 2: self.seleccionar(P[i], 2)
            else: self.seleccionar(P[i], 1)
 
    def punto_8(self):
        beneficiarios = self.extraer_cantidad(self.tabla(8))
        if beneficiarios != 0:
            for b in range(beneficiarios):
                for p in range(4):
                    self.seleccionar(self.format_preguntas(b)[p], 1)
