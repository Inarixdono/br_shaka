from libreria import Mis
from database import Database
from selenium.webdriver.common.keys import Keys

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
        else: self.seleccionar('//*[@id="MainContent_cboFirstAssessment"]', 2, wait= True) # Pregunta #1

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

            self.seleccionar('//*[@id="MainContent_cboMissedClinicAppointment"]', 1, wait= True) # Pregunta #4
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
            self.seleccionar('//*[@id="MainContent_cboMissedClinicAppointment"]', 2, wait = True) # Pregunta #4
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
            self.seleccionar('//*[@id="MainContent_cboAmId"]', 1, wait= True) # Pregunta #9
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
            self.seleccionar('//*[@id="MainContent_cboYndkIdEverVLTest"]', 1, wait= True) # Pregunta #15
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

    def main(arg_abandono: bool = False):
        sesion = Adherencia()
        while True:
            try:
                sesion.parte1(abandono= arg_abandono)
                sesion.parte2(arg_abandono)
                sesion.parte3()
            except ValueError: break
        print('ya')

        sesion.adherencia.close_connection()
        sesion.cerrar()