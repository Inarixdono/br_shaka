"""
    Shaka
    Formulario de servicios
    Inarixdono

"""

from libreria import Mis
#import time
#from datetime import datetime
#import pyperclip as ctrl
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from funciones import lista, Database

HOGAR = lista('Hogar')
XPATH = lista('servicios','XPATH')
almacen = Database('servicios_shaka')

class Servicio(Mis):

    def __init__(self):
        self.almacen = Database('servicios_shaka')
        self.campos = 'id_hogar, fecha_visita, motivo, lugar, servicio_general, donante_general, beneficiarios_servidos, servicio_individual, donante_individual'
        super().__init__()

    def _return_service(self, service: str):

        SERVICIOS = {'1.9':['//*[@id="MainContent_cboyn_art_retention"]'],
                     '1.10':['//*[@id="MainContent_cboyn_initiate_hts_refereal"]'],
                     '1.38':['//*[@id="MainContent_cboCovid19Education"]'],
                     '1.40':['//*[@id="MainContent_cboOtherWashMaterialDistribution"]','//*[@id="MainContent_cboOtherWashMaterialDistribution_dnr"]'],
                     '2.4':['//*[@id="MainContent_cboyn_community_homework"]'],
                     '5.9':['//*[@id="MainContent_cboFoodDeliveryservice"]','//*[@id="MainContent_cboFoodDeliveryservice_dnr"]'],
                     '5.11':['//*[@id="MainContent_cboVocationalTraining"]','//*[@id="MainContent_cboVocationalTraining_dnr"]'],
                     '1.2':['//*[@id="MainContent_cboyn_wash"]'],
                     '1.6':['//*[@id="MainContent_cboyn_hiv_prevention_edu"]'],
                     '1.11':['//*[@id="MainContent_cboyn_complete_hts_refereal"]']}

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
    
    def _servir(self, servicios, donantes, guardar = True):
        for i in range(len(servicios)):
            
            servicio = self._return_service(servicios[i])

            if not self.elemento(servicio[0][0]).is_displayed():
                #time.sleep(0.5)
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
        self.valores = ''
        self.acceder("https://pactbrmis.org/DataEntry/service_delivery.aspx?tokenID=&action=") 

        # Selecciona el hogar y asigna la fecha
        hogar = HOGAR[fila]
        self.elemento(XPATH[0]).click() 
        self.elemento(XPATH[1]).send_keys(hogar, Keys.ENTER)
        fecha_visita = self.enviar_fecha(XPATH[2],lista('FechaVisita')[fila])

        # Motivo y lugar de visita
        motivo = lista('MotivoVisita')[fila]
        lugar = lista('EntregaEn')[fila]
        self.seleccionar(XPATH[3], motivo)
        self.seleccionar(XPATH[4], lugar)

        # Firma
        self.seleccionar(XPATH[5], 1)
        self.seleccionar(XPATH[6], lista('Idcare')[fila], 'valor') #TODO: Cambiar metodo de seleccion de cuidador
        self.esperar_recarga(self.elemento(XPATH[6]))
        self.seleccionar(XPATH[7], 1)
        
        # Agregar datos al string
        self.valores += f'{self.almacen.return_id_hogar(hogar)}, "{fecha_visita}", {motivo}, {lugar}'

        # Guarda el encabezado
        self.elemento('//*[@id="MainContent_btnsaveMain"]').click()
        self.esperar_alerta() 

    def rotar_beneficiario(self, fila): # Hace un recorrido entre los beneficiarios y le va marcando su servicio 

        self.valores += f', "{lista("S_GENERAL")[fila]}", "{lista("D_GENERAL")[fila]}", "{lista("B_SERVIDO")[fila]}", "{lista("SERVBEN")[fila]}", "{lista("D_BENSERV")[fila]}"'

        servicio_general = lista('S_GENERAL')[fila].split(' ')
        servicio_individual = lista('SERVBEN')[fila].split(' ')
        servir_general = servicio_general[0] != '0'
        miembros = list()

        for i in self.seleccionar(XPATH[8],por='').options[1:]:
            miembros.append(i.text)

        for beneficiario in miembros: 
            
            individual = (beneficiario[-2:] in lista('B_SERVIDO')[fila].split(' '))

            if not servir_general:

                if individual: seleccionado = beneficiario
                else: continue

            else: seleccionado = beneficiario

            self.seleccionar(XPATH[8], seleccionado , 'texto')

            try: self.esperar_recarga(self.elemento(XPATH[8]))

            except UnexpectedAlertPresentException: print("Beneficiario tiene 21 años")

            else:
                    # Comprueba si el beneficiario esta activo
                if not self.elemento(XPATH[8]).get_attribute('value') in lista('ID','BenSalidos','Ben'): 
                        
                    # Comprueba la edad del beneficiario
                    if int(self.elemento(XPATH[9]).get_attribute('value')) in range(17, 21): 
                        self.seleccionar(XPATH[10],1)
                        self.seleccionar(XPATH[11],2)
                    else:
                        self.seleccionar(XPATH[10],3)
                        self.seleccionar(XPATH[11],3)

                    # Comprueba si el hogar recibe algun servicio individua   
                    if str(servicio_individual[0]) != '0' and individual: 
                        self._servir(servicio_individual, lista('D_BENSERV')[fila].split(' '), not servir_general)

                    if servir_general: 
                        self._servir(servicio_general, lista('D_GENERAL')[fila].split(' '))
                    
                else:
                    print('Beneficiario salido')
    
    def guardar_registro(self):
        self.almacen.insert(self.campos, self.valores)
