"""
    Shaka
    Formulario de servicios
    Inarixdono
"""

from libreria import Mis
from pandas import read_csv
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from funciones import lista
from math import floor
from database import Database

df = read_csv(r'Archivos\Servir.csv', delimiter= ';', index_col= 'ID',
              dtype= {'beneficiaries_served': str})
bd = Database('servicios_shaka')
XPATH = lista('servicios','XPATH')

class Servicio(Mis):

    def __init__(self):
        self.almacen = Database('servicios_shaka')
        super().__init__()

    def _return_service(self, service: str):

        int_service: int = floor(float(service))
        dominium = f'//*[@id="MainContent_mainPanal"]/a[{int_service + 2}]'
        
        match int_service:
            case 1:
                save = '//*[@id="MainContent_btnsaveHealth"]'
            case 2:
                save = '//*[@id="MainContent_btnsaveEducation"]'
            case 3:
                save = '//*[@id="MainContent_btnsavePSS"]'
            case 4:
                save = '//*[@id="MainContent_btnsaveProtection"]'
            case 5:
                save = '//*[@id="MainContent_btnsave"]'

        return self.almacen.service_path(service), dominium, save
    
    def _servir(self, services: tuple, donors: tuple, save = True):

        for service, donor in zip(services, donors):
            
            service_path, dominium_path, save_path = self._return_service(service)

            if not self.elemento(service_path).is_displayed():
                self.elemento(dominium_path).click()
            self.wait.until(EC.visibility_of(self.elemento(service_path)))
            self.seleccionar(service_path, 1)

            if donor != '0':
                self.seleccionar(self.add_sufix(service_path, 'dnr'), donor)
                
        if save:
            #TODO: SE ESTÁ PRESENTANDO UNA EXCEPCIÓN EN EL GUARDADO DEL DOMINIO DE SALUD
            #      HACER PRUEBAS Y CORREGIR.
            self.elemento(save_path).click()
            self.esperar_alerta() # Espera

    def encabezado(self, row: int): 

        # Entra al formulario de entrada de servicios
        self.acceder("https://pactbrmis.org/DataEntry/service_delivery.aspx?tokenID=&action=") 

        # Selecciona el hogar y asigna la fecha
        self.elemento(XPATH[0]).click() 
        self.elemento(XPATH[1]).send_keys(df.home[row], Keys.ENTER)
        self.fecha_visita = self.enviar_fecha(XPATH[2], df.date[row])

        # Motivo y lugar de visita
        self.seleccionar(XPATH[3], df.reason[row])
        self.seleccionar(XPATH[4], df.place[row])

        # Firma
        self.seleccionar(XPATH[5], 1)
        caregiver_select = self.seleccionar(XPATH[6], por='').options
        for caregiver in caregiver_select:
            if caregiver.text[-7:] == df.caregiver[row]:
                caregiver.click()
                self.esperar_recarga(caregiver)
                break
        self.seleccionar(XPATH[7], 1)

        # Guarda el encabezado
        self.elemento('//*[@id="MainContent_btnsaveMain"]').click()
        self.esperar_alerta() 

    def rotar_beneficiario(self, row: int):

        servicio_general = df.general_service[row].split(' ')
        servicio_individual = df.individual_service[row].split(' ')
        servir_general = servicio_general[0] != '0'
        miembros = [o.text for o in self.seleccionar(XPATH[8], por= '').options[1:]]

        for beneficiario in miembros:
            
            individual = (beneficiario[-2:] in df.beneficiaries_served[row].split(' '))

            if not servir_general:
                if individual:
                    seleccionado = beneficiario
                else:
                    continue
            else:
                seleccionado = beneficiario

            try:
                self.seleccionar(XPATH[8], seleccionado , 'texto', True)
            except UnexpectedAlertPresentException:
                print("Beneficiario tiene 21 años")

            else:
                    # Comprueba si el beneficiario esta activo
                if self.elemento(XPATH[8]).get_attribute('value') not in lista('ID','BenSalidos','Ben'):
                    #TODO: Comprobar el valor que trae el método `get_attribute`.
                    # Comprueba la edad del beneficiario
                    if int(self.elemento(XPATH[9]).get_attribute('value')) in range(17, 21):
                        #TODO: Simplificar el dato de la edad.
                        self.seleccionar(XPATH[10],1)
                        self.seleccionar(XPATH[11],2)
                    else:
                        self.seleccionar(XPATH[10],3)
                        self.seleccionar(XPATH[11],3)

                    # Comprueba si el hogar recibe algun servicio individual
                    if str(servicio_individual[0]) != '0' and individual: 
                        self._servir(servicio_individual, 
                                     df.individual_donor[row].split(' '), 
                                     not servir_general)

                    if servir_general:
                        self._servir(servicio_general, df.general_donor[row].split(' '))
                    
                else:
                    print('Beneficiario salido')
    
    def guardar_registro(self, row: int):
        columns = [i for i in range(11) if i not in [0, 1, 4, 5]]
        bd.insert_service('{}, "{}", {}, {}, "{}", "{}", "{}", "{}", "{}"'.format(
            bd.return_id_home(df.home[row]), self.fecha_visita, *df.iloc[row, columns]))

def main():

    sesion = Servicio()
    familias_servidas = df.home

    for i in range(0 , len(familias_servidas)):
        if familias_servidas[i] not in lista('Hogar','FamSalidas'):
            sesion.encabezado(i)
            sesion.rotar_beneficiario(i)
            print(f'Servicio {i + 1} de {len(familias_servidas)} digitado')
        elif input('Familia salida, desea continuar?') == 's':
            sesion.rotar_beneficiario(i)
        else: 
            print('Familia salida, no servida.')
        sesion.guardar_registro(i)
    
    sesion.almacen.close_connection()
    sesion.cerrar()

main()

