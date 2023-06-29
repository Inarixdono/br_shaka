"""
    Shaka
    Formulario de servicios
    Inarixdono

"""

from libreria import Mis
import pandas as pd
import time
from datetime import datetime
import pyperclip as ctrl
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

class Servicio(Mis):

    def __init__(self):

        self.HOGAR = self.lista('Hogar')
        self.XPATH = self.lista('xPath','XPATH')
        super().__init__()

    def lista(self, columna, nombre = 'Servir', index='ID'):
        lista = pd.read_csv('Archivos\\'+ nombre +'.csv',delimiter=';', index_col= index, dtype= str)[columna].tolist()
        return(lista)
    
    def return_service(service: str):

        SERVICIOS = {'1.9':['//*[@id="MainContent_cboyn_art_retention"]'],
                    '1.10':['//*[@id="MainContent_cboyn_initiate_hts_refereal"]'],
                    '1.38':['//*[@id="MainContent_cboCovid19Education"]'],
                    '1.40':['//*[@id="MainContent_cboOtherWashMaterialDistribution"]','//*[@id="MainContent_cboOtherWashMaterialDistribution_dnr"]'],
                    '2.4':['//*[@id="MainContent_cboyn_community_homework"]'],
                    '5.9':['//*[@id="MainContent_cboFoodDeliveryservice"]','//*[@id="MainContent_cboFoodDeliveryservice_dnr"]'],
                    '1.2':['//*[@id="MainContent_cboyn_wash"]']}

        DOMINIO = {'Salud':'//*[@id="MainContent_mainPanal"]/a[3]',
                'Educación':'//*[@id="MainContent_mainPanal"]/a[4]',
                'Fortalecimiento':'//*[@id="MainContent_mainPanal"]/a[7]'}

        GUARDAR = {'Salud':'//*[@id="MainContent_btnsaveHealth"]',
                    'Fortalecimiento':'//*[@id="MainContent_btnsave"]',
                    'Educación':'//*[@id="MainContent_btnsaveEducation"]',
                    'Encabezado':'//*[@id="MainContent_btnsaveMain"]'}
        
        if 1 < float(service) < 2:
            dominio = 'Salud'
        elif 2 < float(service) < 3:
            dominio = 'Educación'
        elif 5 < float(service) < 6:
            dominio = 'Fortalecimiento'

        return SERVICIOS[service], DOMINIO[dominio], GUARDAR[dominio]
    
    def servir(self, servicios, donantes, guardar = True):
        for i in range(len(servicios)):
            
            servicio = self.return_service(servicios[i])

            if not self.elemento(servicio[0][0]).is_displayed():
                time.sleep(0.5)
                self.elemento(servicio[1]).click()
            self.wait.until(EC.visibility_of(self.elemento(servicio[0][0])))
            self.seleccionar(servicio[0][0],1)
            if donantes[i] != '0':
                self.seleccionar(servicio[0][1],donantes[i])
        if guardar:
            self.elemento(servicio[2]).click()
            self.esperar_alerta() # Espera

    def encabezado(self, fila): 

        # Entra al formulario de entrada de servicios
        self.acceder("https://pactbrmis.org/DataEntry/service_delivery.aspx?tokenID=&action=") 

        # Selecciona el hogar y asigna la fecha
        self.elemento(self.XPATH[0]).click() 
        self.elemento(self.XPATH[1]).send_keys(self.HOGAR[fila], Keys.ENTER)
        set_fecha = datetime.strptime(self.lista('FechaVisita')[fila], '%d/%m/%Y')
        fecha = set_fecha.strftime('%d/%m/%Y')
        ctrl.copy(fecha)
        self.elemento(self.XPATH[2]).send_keys(Keys.CONTROL, 'v', Keys.ENTER)

        # Motivo y lugar de visita
        self.seleccionar(self.XPATH[3], self.lista('MotivoVisita')[fila], 'texto')
        self.seleccionar(self.XPATH[4], self.lista('EntregaEn')[fila],'texto' )

        # Firma
        self.seleccionar(self.XPATH[5], 'Si', 'texto')
        self.seleccionar(self.XPATH[6], self.lista('Idcare')[fila], 'valor')
        time.sleep(1) #TODO: MEJORAR ESTA ESPERA
        self.seleccionar(self.XPATH[7], 'Si', 'texto')
        
        # Guarda el encabezado
        self.elemento(self.GUARDAR['Encabezado']).click()
        self.esperar_alerta() 

    def rotar_beneficiario(self, fila): # Hace un recorrido entre los beneficiarios y le va marcando su servicio 

        servicio_general = self.lista('S_GENERAL')[fila].split(' ')
        servicio_individual = self.lista('SERVBEN')[fila].split(' ')
        servir_general = servicio_general[0] != '0'
        miembros = list()

        for i in self.seleccionar(self.XPATH[8],por='').options[1:]:
            miembros.append(i.text)

        for beneficiario in miembros: 
            
            individual = (beneficiario[-2:] in self.lista('B_SERVIDO')[fila].split(' '))

            if not servir_general:

                if individual: seleccionado = beneficiario
                else: continue

            else: seleccionado = beneficiario

            self.elemento(self.return_service('1.9')[1]).click()
            time.sleep(0.5)
            self.seleccionar(self.XPATH[8], seleccionado , 'texto')

            try: self.wait.until(EC.invisibility_of_element(self.elemento(self.return_service('1.9')[0][0])))

            except UnexpectedAlertPresentException: 
                print("Beneficiario tiene 21 años")
                self.elemento(self.return_service('1.9')[1]).click()  
                time.sleep(0.6) 

            else:
                    # Comprueba si el beneficiario esta activo
                if not self.elemento(self.XPATH[8]).get_attribute('value') in self.lista('ID','BenSalidos','Ben'): 
                        
                    # Comprueba la edad del beneficiario
                    if int(self.elemento(self.XPATH[9]).get_attribute('value')) in range(17, 21): 
                        self.seleccionar(self.XPATH[10],1)
                        self.seleccionar(self.XPATH[11],2)
                    else:
                        self.seleccionar(self.XPATH[10],3)
                        self.seleccionar(self.XPATH[11],3)

                    # Comprueba si el hogar recibe algun servicio individua   
                    if str(servicio_individual[0]) != '0' and individual: 
                        self.servir(servicio_individual, self.lista('D_BENSERV')[fila].split(' '), not servir_general)
                    
                    if servir_general: 
                        self.servir(servicio_general, self.lista('D_GENERAL')[fila].split(' '))
                    
                else:
                    print('Beneficiario salido')  
                    self.elemento(self.return_service('1.9')[1]).click() 
                    time.sleep(0.6) 
