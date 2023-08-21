from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from funciones import lista
from database import Database
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
        return self.driver.find_element('xpath',ruta)
        
    def seleccionar_hogar(self, ruta, hogar):
        ref = self.elemento(ruta)
        self.elemento(ruta).click()
        self.elemento('/html/body/span/span/span[1]/input').send_keys(hogar, Keys.ENTER)
        self.esperar_recarga(ref)

    def enviar_fecha(self,ruta, fecha, permite_entrada = False):
        if len(fecha) <= 2: fecha = datetime.strptime(fecha + self._hoy[2:], '%d/%m/%Y').strftime('%d/%m/%Y')
        elif len(fecha) <= 5: fecha = datetime.strptime(fecha + self._hoy[5:], '%d/%m/%Y').strftime('%d/%m/%Y')
        elif len(fecha) <= 8: fecha = datetime.strptime(fecha, '%d/%m/%y').strftime('%d/%m/%Y')
        else: fecha = datetime.strptime(fecha, '%d/%m/%Y').strftime('%d/%m/%Y') # Debe medir minimo 9
        if permite_entrada: self.elemento(ruta).send_keys(fecha, Keys.ENTER)
        else: 
            ctrl.copy(fecha)
            self.elemento(ruta).send_keys(Keys.CONTROL, 'v', Keys.ENTER)
        return datetime.strptime(fecha, '%d/%m/%Y').strftime('%Y-%m-%d')
    
    def send_keys(self, path, value):
        self.elemento(path).send_keys(value)
    
    def enviar_otro(self,ruta,ruta_otro,valor):
        self.elemento(ruta).click()
        self.esperar_recarga(self.elemento(ruta))
        self.elemento(ruta_otro).send_keys(valor)

    def seleccionar(self, ruta, valor = '', por = 'index', wait = False):
        
        ref = self.elemento(ruta)
        seleccionar = Select(ref)

        match por:
            case 'index': seleccionar.select_by_index(valor)
            case 'valor': seleccionar.select_by_value(valor)
            case 'texto': seleccionar.select_by_visible_text(valor)
            case '': return seleccionar
            case _: print('Invalid selection method')

        if wait: self.esperar_recarga(ref)

    def extraer_cantidad(self, ruta):
        return len(self.elemento(ruta).find_elements('tag name', 'tr')) - 1
        
    def cerrar(self):
        self.driver.close()

    def esperar_recarga(self, referencia):
        self.wait.until(EC.staleness_of(referencia))

    def esperar_alerta(self):
        self.wait.until(EC.alert_is_present()).accept()

XPATH = lista('graduacion','XPATH')

class Graduate(Mis): 

    def tabla(self, n):
        return f'//*[@id="MainContent_gvBenchmark{n}"]/tbody' 
    
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

class Adherencia(Mis):
    def __init__(self):
        self.adherencia = Database('adherencia')
        self.campos = 'id_vih, fecha_adherencia, abandono'
        self.valores = ''
        super().__init__()

    def parte1(self, primera_vez = False, abandono = False):

        self.campos = 'id_vih, fecha_adherencia, abandono'
        self.valores = ''

        self.acceder('https://pactbrmis.org/DataEntry/adherence.aspx')
        fecha_adherencia = self.enviar_fecha('//*[@id="MainContent_txtAdherenceDate"]',input('Fecha actual'))
        hogar = input('Código del hogar')
        self.seleccionar_hogar('//*[@id="select2-MainContent_cboHHList-container"]', hogar)
        beneficiario = input("Beneficiario")
        self.seleccionar_hogar('//*[@id="select2-MainContent_cboHHMember-container"]',f'{hogar}/{beneficiario}')
        beneficiario = self.elemento('//*[@id="select2-MainContent_cboHHMember-container"]').get_attribute('title').split(' ')[0]
        edad = input('Edad')
        self.elemento('//*[@id="MainContent_txtAgeYear"]').send_keys(edad)

        if primera_vez:
            self.seleccionar('//*[@id="MainContent_cboFirstAssessment"]', 1) # Pregunta #1
            self.seleccionar('//*[@id="MainContent_cboAtiId"]', 1) # Pregunta #2
            fecha = input('Fecha de inicio de ARV')
            self.enviar_fecha('//*[@id="MainContent_txtArtInitiatedDate"]',fecha) # Pregunta #2b
        else: self.seleccionar('//*[@id="MainContent_cboFirstAssessment"]', 2) # Pregunta #1

        self.valores += f'{self.adherencia.return_id_vih(beneficiario)},"{fecha_adherencia}"'

        if abandono:

            falta_cita = {'A': [0,'Falta de recursos para ir al SAI'],
                'B': [1,'El SAI está muy lejos del hogar'],
                'C': [2,'Está muy enfermo para viajar'],
                'D': [3,'Necesita permiso de su pareja para ir al SAI'],
                'E': [4,'Por el trabajo'],
                'F': [5,'No tiene con quien dejar a los niños'],
                'G': [6,'Temor por ser indocumentado'],
                'H': [7,'No quiere que nadie lo vea'],
                'I': [8,'Temor por que descubran su estatus VIH'],
                'J': [9,'Por estigma y discriminación'],
                'K': [10,'Transporte no disponible por COVID-19'],
                'L': [11,'El SAI está cerrado por COVID-19'],
                'M': [12,'Horarios de atención limitados en el SAI'],
                'N': [13,'No hablan creole en el SAI'],
                'O': [14,'No le gusta el SAI'],
                'X': [15,'Otro']}

            self.seleccionar('//*[@id="MainContent_cboMissedClinicAppointment"]', 1) # Pregunta #4
            self.esperar_recarga(self.elemento('//*[@id="MainContent_cboMissedClinicAppointment"]'))
            self.seleccionar('//*[@id="MainContent_cboHamfId"]', input('Frecuencia de abandono')) # Pregunta #5
            razon = input('Por qué falta a su cita?').upper()
            otro = '//*[@id="MainContent_cblHivAppointmentMissed_15"]'
            txt = '//*[@id="MainContent_txtHivAppointmentMissedOther"]'
            if razon == 'X':
                falta_cita[razon][1] = input('Otro')
                self.enviar_otro(otro, txt, falta_cita[razon][1])
            else:
                self.elemento(f'//*[@id="MainContent_cblHivAppointmentMissed_{falta_cita[razon][0]}"]').click() # Pregunta #6
            self.campos += ', razon'
            self.valores += f', "Si", "{falta_cita[razon][1]}"'
        else:
            self.seleccionar('//*[@id="MainContent_cboMissedClinicAppointment"]', 2) # Pregunta #4
            self.esperar_recarga(self.elemento('//*[@id="MainContent_cboMissedClinicAppointment"]'))
            self.valores += ', "No"'  

        self.seleccionar('//*[@id="MainContent_cboPlwhMember"]', 1) # Pregunta #7

    def parte2(self, abandono = False):
            
        if not abandono:
            proxima_cita = self.enviar_fecha('//*[@id="MainContent_txtArtVisitDate"]', input("Próxima cita"))
            self.seleccionar('//*[@id="MainContent_cboAmId"]', 2) # Pregunta #8
            self.campos += f', proxima_cita'
            self.valores += f', "{proxima_cita}"'
        else:
            
            dejar_pastillas = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,'I':8,
                                'NA': 'No acepta su condición', 'NQ': 'No quiere tomar ARV',
                                'NN': 'No necesita ARV'}

            self.elemento('//*[@id="MainContent_chkArtVisitDateDontKnow"]').click() # Pregunta #8
            self.esperar_recarga(self.elemento('//*[@id="MainContent_chkArtVisitDateDontKnow"]'))
            self.seleccionar('//*[@id="MainContent_cboAmId"]', 1) # Pregunta #9
            self.esperar_recarga(self.elemento('//*[@id="MainContent_cboAmId"]'))
            self.elemento('//*[@id="MainContent_txtArtMissedDays"]').\
                send_keys(input('Cuantos dias ha dejado de tomar sus medicamentos')) # Pregunta #10
            
            r = input('Razón por la que dejó de tomar ARV').upper()
            otro = '//*[@id="MainContent_cblArtMissedReason_9"]'
            txt = '//*[@id="MainContent_txtArtMissedReason"]'
            if r == 'X':  # Pregunta #11
                self.enviar_otro(otro,txt,input('Otro'))
            elif not r in ['NA','NQ','NN']:
                self.elemento(f'//*[@id="MainContent_cblArtMissedReason_{dejar_pastillas[r]}"]').click()
            else:
                self.enviar_otro(otro,txt,dejar_pastillas[r])
            
            r = input('Problema para obtener sus medicamento?')
            otro = '//*[@id="MainContent_cblArtObtainChallenges_11"]'
            txt = '//*[@id="MainContent_txtArtObtainChallengesOther"]'
            problemas_arv = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,'I':8,
                                'J':9, 'K':10 ,'NA': 'No acepta su condición', 'NQ': 'No quiere tomar ARV',
                                'NN': 'No necesita ARV'}
            self.seleccionar('//*[@id="MainContent_cboArtObtainChallenges"]', r) # Pregunta #12
            
            if r == '1':
                self.esperar_recarga(self.elemento('//*[@id="MainContent_cboArtObtainChallenges"]'))
                r = input('Que problemas tiene?').upper()
                if r == 'X':  # Pregunta #12b
                    self.enviar_otro(otro,txt,input('Otro'))
                elif not r in ['NA','NQ','NN']:
                    self.elemento(f'//*[@id="MainContent_cblArtObtainChallenges_{problemas_arv[r]}"]').click()
                else:
                    self.enviar_otro(otro,txt,problemas_arv[r])
        
        r = input('Preguntas 13 y 14') # Pregunta #13 y #14
        self.seleccionar('//*[@id="MainContent_cboArtTillNextAppointment"]', r[0])
        self.seleccionar('//*[@id="MainContent_cboAmsId"]', r[1])
        if r[1] == '4':
            otro = input('Cuantos meses recibio?')
            self.elemento('//*[@id="MainContent_txtArtMonthsSupplyOther"]').send_keys(f'{otro} meses')
    
    def parte3(self): 
        fecha_cv = input('Fecha de carga viral\nSi no se ha hecho cv escribe "no"')
        if fecha_cv != 'no':
            self.seleccionar('//*[@id="MainContent_cboYndkIdEverVLTest"]', 1) # Pregunta #15
            self.esperar_recarga(self.elemento('//*[@id="MainContent_cboYndkIdEverVLTest"]'))
            fecha_cv = self.enviar_fecha('//*[@id="MainContent_txtViralTestDate"]', fecha_cv) # Pregunta #16
            resultado_cv = input('Resultado de carga viral')
            self.campos += ', fecha_cv, resultado_cv' 
            self.valores += f', "{fecha_cv}", {resultado_cv}'
            self.elemento('//*[@id="MainContent_txtViralTestResult"]').send_keys(resultado_cv, Keys.ENTER) # Pregunta #17
        else: 
            self.seleccionar('//*[@id="MainContent_cboYndkIdEverVLTest"]', 2) # Pregunta #15
            self.elemento('//*[@id="MainContent_btnSave"]').click()
        
        self.adherencia.insert(self.campos, self.valores)

        self.esperar_alerta()