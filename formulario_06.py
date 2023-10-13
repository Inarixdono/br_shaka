"""
    Shaka
    Formulario de servicios
    Inarixdono
"""

from libreria import Mis, DataFrameWrapper
from pandas import read_csv
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from funciones import lista
from math import floor
from database import Database

df = read_csv(r'Archivos\Servir.csv', delimiter= ';', index_col= 'ID',
              dtype= {
                  'general_service': str,
                  'general_donor' : str,
                  'beneficiaries_served': str,
                  'individual_service' : str,
                  'individual_donor' : str})
xpath = DataFrameWrapper(
    read_csv(
        r'paths\ard006.csv', delimiter= ';', index_col= 0).T
)
bd = Database('servicios_shaka')

class Servicio(Mis):

    def __init__(self):
        self.almacen = Database('servicios_shaka')
        super().__init__()

    def _return_service(self, service: str):

        int_service: int = floor(float(service))
        dominium = f'//*[@id="MainContent_mainPanal"]/a[{int_service + 2}]'
        
        match int_service:
            case 1:
                save = xpath.save_health
            case 2:
                save = xpath.save_education
            case 3:
                save = xpath.save_pss
            case 4:
                save = xpath.save_protection
            case 5:
                save = xpath.save_main

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
        self.acceder(xpath.service_link) 

        # Selecciona el hogar y asigna la fecha
        self.seleccionar_hogar(xpath.home_container, df.home[row])
        self.fecha_visita = self.enviar_fecha(xpath.date, df.date[row])

        # Motivo y lugar de visita
        self.seleccionar(xpath.reason, df.reason[row])
        self.seleccionar(xpath.place, df.place[row])

        # Firma
        self.seleccionar(xpath.case_plan, 1)
        caregiver_select = self.seleccionar(xpath.caregiver_list, por='').options
        for caregiver in caregiver_select:
            if caregiver.text[-7:] == df.caregiver[row]:
                caregiver.click()
                self.esperar_recarga(caregiver)
                break
        self.seleccionar(xpath.cargiver_sign, 1)

        # Guarda el encabezado
        self.elemento(xpath.save_header).click()
        self.esperar_alerta() 

    def rotar_beneficiario(self, row: int):

        servicio_general = df.general_service.tolist()[row].split(' ')
        servicio_individual = df.individual_service.tolist()[row].split(' ')
        servir_general = servicio_general[0] != '0'
        miembros = [o.text for o in self.seleccionar(
            xpath.member_list, por= '').options[1:]]

        for beneficiario in miembros:
            
            individual = (beneficiario[-2:] in df.beneficiaries_served[row].split(' '))

            if not servir_general:
                if individual:
                    selected = beneficiario
                else:
                    continue
            else:
                selected = beneficiario

            try:
                self.seleccionar(xpath.member_list, selected , 'texto', True)
            except UnexpectedAlertPresentException:
                print("Beneficiario tiene 21 años")
            else:
                    # Comprueba si el beneficiario esta activo
                if selected.split('-')[1].strip(' ') not in lista('Ben', 'BenSalidos'):
                    age = int(self.elemento(xpath.age).get_attribute('value'))
                    if age in range(17, 21):
                        self.seleccionar(xpath.school, 1)
                        self.seleccionar(xpath.economic_activity, 2)
                    else:
                        self.seleccionar(xpath.school, 3)
                        self.seleccionar(xpath.economic_activity, 3)

                    if str(servicio_individual[0]) != '0' and individual: 
                        self._servir(servicio_individual, 
                                     df.individual_donor.tolist()[row].split(' '), 
                                     not servir_general)
                        
                    if servir_general:
                        self._servir(servicio_general,
                                     df.general_donor.tolist()[row].split(' '))     
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

#main()