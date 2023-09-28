"""
    Shaka
    Formulario de servicios
    Inarixdono
"""

from libreria import Mis
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from funciones import lista
from math import floor
from database import Database

HOGAR = lista('Hogar')
XPATH = lista('servicios','XPATH')
almacen = Database('servicios_shaka')

class Servicio(Mis):

    def __init__(self):
        self.almacen = Database('servicios_shaka')
        self.campos = 'id_hogar, fecha_visita, motivo, lugar, servicio_general, donante_general, beneficiarios_servidos, servicio_individual, donante_individual'
        super().__init__()

    def _return_service(self, service: str):

        int_service: int = floor(float(service))
        dominium = f'//*[@id="MainContent_mainPanal"]/a[{int_service + 2}]'
        
        match int_service:
            case 1: save = '//*[@id="MainContent_btnsaveHealth"]'
            case 2: save = '//*[@id="MainContent_btnsaveEducation"]'
            case 3: save = '//*[@id="MainContent_btnsavePSS"]'
            case 4: save = '//*[@id="MainContent_btnsaveProtection"]'
            case 5: save = '//*[@id="MainContent_btnsave"]'

        return self.almacen.service_path(service), dominium, save
    
    def _servir(self, services: tuple, donors: tuple, save = True):

        for service, donor in zip(services, donors):
            
            service_path, dominium_path, save_path = self._return_service(service)

            if not self.elemento(service_path).is_displayed():
                self.elemento(dominium_path).click()
            self.wait.until(EC.visibility_of(self.elemento(service_path)))
            self.seleccionar(service_path, 1)

            if donor != '0':
                donor_path = service_path[:-2] + '_dnr' + service_path[-2:]
                self.seleccionar(donor_path, donor)
        if save:
            self.elemento(save_path).click()
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
        caregiver = lista('caregiver')[fila]
        for i in self.seleccionar(XPATH[6], por='').options:
            if i.text[-7:] == caregiver:
                i.click()
                self.esperar_recarga(i)
                break
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
        miembros = [o.text for o in self.seleccionar(XPATH[8], por= '').options[1:]]

        for beneficiario in miembros:
            
            individual = (beneficiario[-2:] in lista('B_SERVIDO')[fila].split(' '))

            if not servir_general:

                if individual: seleccionado = beneficiario
                else: continue

            else: seleccionado = beneficiario

            try: self.seleccionar(XPATH[8], seleccionado , 'texto', True)

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

                    # Comprueba si el hogar recibe algun servicio individual
                    if str(servicio_individual[0]) != '0' and individual: 
                        self._servir(servicio_individual, lista('D_BENSERV')[fila].split(' '), not servir_general)

                    if servir_general:
                        self._servir(servicio_general, lista('D_GENERAL')[fila].split(' '))
                    
                else:
                    print('Beneficiario salido')
    
    def guardar_registro(self):
        self.almacen.insert(self.campos, self.valores)

def main():

    sesion = Servicio()
    familias_servidas = lista('Hogar')

    for i in range(0 , len(familias_servidas)):
        if not familias_servidas[i] in lista('Hogar','FamSalidas'):
            sesion.encabezado(i)
            sesion.rotar_beneficiario(i)
            print(f'Servicio {i + 1} de {len(familias_servidas)} digitado')
        elif input('Familia salida, desea continuar?') == 's':
            sesion.rotar_beneficiario(i)
        else: print('Familia salida, no servida.')
        sesion.guardar_registro()
    
    sesion.almacen.close_connection()
    sesion.cerrar()

main()