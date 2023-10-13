
from libreria import Mis, DataFrameWrapper
from pandas import read_csv
from database import Database
from selenium.webdriver.common.keys import Keys

xpath = DataFrameWrapper(
    read_csv(
        r'paths\ard011.csv', delimiter= ';', index_col= 0).T
)
bd = Database('adherencia')

class Adherencia(Mis):
    def __init__(self):
        self.campos = 'id_vih, fecha_adherencia, abandono'
        self.valores = ''
        super().__init__()

    def parte1(self, primera_vez = False, abandono = False):

        self.campos = 'id_vih, fecha_adherencia, abandono'
        self.valores = ''

        self.acceder(xpath.adherence_link)
        adherence_date = self.enviar_fecha(xpath.adherence_date, input('Fecha actual'))
        hogar = input('Código del hogar')
        self.seleccionar_hogar(xpath.home_container, hogar)
        beneficiario = input("Beneficiario")
        self.seleccionar_hogar(xpath.member_container,f'{hogar}/{beneficiario}')
        beneficiario = self.elemento(
            xpath.member_container).get_attribute('title').split(' ')[0]
        #TODO: CAMBIAR METODO DE CONSEGUIR EL CODIGO DEL BENEFICIARIO
        #TODO: EVALUAR SI ESTA VARIABLE ES NECESARIA
        edad = input('Edad')
        self.elemento(xpath.age).send_keys(edad)

        if primera_vez:
            self.seleccionar(xpath.question_1, 1)
            self.seleccionar(xpath.question_2a, 1)
            fecha = input('Fecha de inicio de ARV')
            self.enviar_fecha(xpath.question_2b,fecha)
        else:
            self.seleccionar(xpath.question_1, 2, wait= True)

        self.valores += f'{bd.return_id_vih(beneficiario)},"{adherence_date}"'

        if abandono:

            falta_cita = {
                'A': [0,'Falta de recursos para ir al SAI'],
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

            self.seleccionar(xpath.question_4, 1, wait= True)
            self.seleccionar(xpath.question_5, input('Frecuencia de abandono'))
            razon = input('Por qué falta a su cita?').upper()
            if razon == 'X':
                falta_cita[razon][1] = input('Otro')
                self.enviar_otro(self.add_sufix(
                    xpath.question_6, 15), xpath.question_6o, falta_cita[razon][1])
            else:
                self.elemento(self.add_sufix(
                    xpath.question_6, [razon][0])).click()
            self.campos += ', razon'
            self.valores += f', "Si", "{falta_cita[razon][1]}"'
        else:
            self.seleccionar(xpath.question_4, 2, wait = True)
            self.valores += ', "No"'  

        self.seleccionar(xpath.question_7, 1)

    def parte2(self, abandono = False):
            
        if not abandono:
            proxima_cita = self.enviar_fecha(xpath.question_8a, input("Próxima cita"))
            self.seleccionar(xpath.question_9, 2)
            self.campos += ', proxima_cita'
            self.valores += f', "{proxima_cita}"'
        else:
            
            dejar_pastillas = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
                               'I':8,'NA': 'No acepta su condición',
                               'NQ': 'No quiere tomar ARV','NN': 'No necesita ARV'}

            self.elemento(xpath.question_8b).click()
            self.esperar_recarga(self.elemento(xpath.question_8b))
            self.seleccionar(xpath.question_9, 1, wait= True)
            self.elemento(xpath.question_10).send_keys(
                input('Cuantos dias ha dejado de tomar sus medicamentos'))
            
            r = input('Razón por la que dejó de tomar ARV').upper()
            if r == 'X':  # Pregunta #11
                self.enviar_otro(self.add_sufix(
                    xpath.question_11, 9), xpath.question_11o, input('Otro'))
            elif r not in ['NA','NQ','NN']:
                self.elemento(self.add_sufix(
                    xpath.question_11, dejar_pastillas[r])).click()
            else:
                self.enviar_otro(self.add_sufix(
                    xpath.question_11, 9), xpath.question_11o, dejar_pastillas[r])
            
            r = input('Problema para obtener sus medicamento?')
            otro = '//*[@id="MainContent_cblArtObtainChallenges_11"]'
            problemas_arv = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
                             'I':8, 'J':9, 'K':10 ,'NA': 'No acepta su condición',
                             'NQ': 'No quiere tomar ARV', 'NN': 'No necesita ARV'}
            self.seleccionar(xpath.question_12a, r)
            
            if r == '1':
                self.esperar_recarga(self.elemento(xpath.question_12a))
                r = input('Que problemas tiene?').upper()
                if r == 'X':  # Pregunta #12b
                    self.enviar_otro(self.add_sufix(
                        xpath.question_12r, 11), xpath.question_12o, input('Otro'))
                elif r not in ['NA','NQ','NN']:
                    self.elemento(self.add_sufix(
                        xpath.question_12r, problemas_arv[r])).click()
                else:
                    self.enviar_otro(self.add_sufix(
                        xpath.question_12r, 11), xpath.question_12o, problemas_arv[r])
        
        r = input('Preguntas 13 y 14')
        self.seleccionar(xpath.question_13, r[0])
        self.seleccionar(xpath.question_14, r[1])
        if r[1] == '4':
            otro = input('Cuantos meses recibio?')
            self.elemento(xpath.question_14o).send_keys(f'{otro} meses')
    
    def parte3(self): 
        fecha_cv = input('Fecha de carga viral\nSi no se ha hecho cv escribe "no"')
        if fecha_cv != 'no':
            self.seleccionar(xpath.question_15, 1, wait= True)
            fecha_cv = self.enviar_fecha(xpath.question_16, fecha_cv)
            resultado_cv = input('Resultado de carga viral')
            self.campos += ', fecha_cv, resultado_cv' 
            self.valores += f', "{fecha_cv}", {resultado_cv}'
            self.elemento(xpath.question_17).send_keys(resultado_cv, Keys.ENTER)
        else: 
            self.seleccionar(xpath.question_15, 2)
            self.elemento(xpath.btn_save).click()
        
        bd.insert(self.campos, self.valores)
        self.esperar_alerta()

    def main(arg_abandono: bool = False):
        sesion = Adherencia()
        while True:
            try:
                sesion.parte1(abandono= arg_abandono)
                sesion.parte2(arg_abandono)
                sesion.parte3()
            except ValueError: 
                break
        print('ya')

        sesion.adherencia.close_connection()
        sesion.cerrar()