import pandas as pd
import pyperclip as ctrl 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
from datetime import datetime

# Datos

fam_salidas = pd.read_csv('Archivos\FamSalidas.csv', delimiter = ';', index_col = 'Hogar')['ID'].tolist()
ben_salidos = pd.read_csv('Archivos\BenSalidos.csv', delimiter = ';', index_col = 'Ben')['ID'].tolist()
XPATH = pd.read_csv('Archivos\XPATH.csv', delimiter = ";", index_col = "ID",)['xPath'].tolist()
HOGAR = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Hogar'].tolist()
FECHA = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['FechaVisita'].tolist()
MOTIVO = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['MotivoVisita'].tolist()
LUGAR = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['EntregaEn'].tolist()
CUIDADOR = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Idcare'].tolist()
SERV1 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Serv1'].tolist()
SERV2 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Serv2'].tolist()
SERV3 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Serv3'].tolist()
SERV4 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Serv4'].tolist()
DNR1 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Don1'].tolist()
DNR2 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Don2'].tolist()
DNR3 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Don3'].tolist()
DNR4 = pd.read_csv('Archivos\Servir.csv', delimiter = ";", index_col = "ID",)['Don4'].tolist()

SERVICIOS = {'1.9':'//*[@id="MainContent_cboyn_art_retention"]',
             '1.4':'//*[@id="MainContent_cboOtherWashMaterialDistribution"]',
             '5.9':'//*[@id="MainContent_cboFoodDeliveryservice"]',
             '1.2':'//*[@id="MainContent_cboyn_wash"]'}

DONANTE = {'1.4':'//*[@id="MainContent_cboOtherWashMaterialDistribution_dnr"]',
           '5.9':'//*[@id="MainContent_cboFoodDeliveryservice_dnr"]'}

DOMINIO = {'Salud':'//*[@id="MainContent_mainPanal"]/a[3]',
           'Fortalecimiento':'//*[@id="MainContent_mainPanal"]/a[7]'}

GUARDAR = {'Salud':'//*[@id="MainContent_btnsaveHealth"]',
            'Fortalecimiento':'//*[@id="MainContent_btnsave"]',
            'Encabezado':'//*[@id="MainContent_btnsaveMain"]'}

driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
wait = WebDriverWait(driver,10)

def login(): # Iniciar sesion
    driver.get("https://pactbrmis.org/Account/Login.aspx")
    driver.find_element('xpath','//*[@id="txtUsername"]').send_keys("jenielwtf@gmail.com")
    driver.find_element('xpath','//*[@id="txtPassword"]').send_keys("1qazxsw2")
    driver.find_element('xpath','//*[@id="btnLogin"]').click()   

def Elemento(ruta):
    Elemento = driver.find_element('xpath',ruta)
    return(Elemento)

def encabezado(col): 

    # Entra al formulario de entrada de servicios
    driver.get("https://pactbrmis.org/DataEntry/service_delivery.aspx?tokenID=&action=") 

    # Selecciona el hogar y asigna la fecha
    Elemento(XPATH[0]).click() 
    Elemento(XPATH[1]).send_keys(HOGAR[col], Keys.ENTER)
    set_fecha = datetime.strptime(FECHA[col], '%d/%m/%Y')
    fecha = set_fecha.strftime('%d/%m/%Y')
    ctrl.copy(fecha)
    Elemento(XPATH[2]).send_keys(Keys.CONTROL, 'v', Keys.ENTER)

    # Motivo y lugar de visita
    Select(Elemento(XPATH[3])).select_by_visible_text(MOTIVO[col])      
    Select(Elemento(XPATH[4])).select_by_visible_text(LUGAR[col])

    # Firma
    Select(Elemento(XPATH[5])).select_by_visible_text("Si") 
    Select(Elemento(XPATH[6])).select_by_value(CUIDADOR[col]) 
    time.sleep(1) #TODO: MEJORAR ESTA ESPERA
    Select(Elemento(XPATH[7])).select_by_visible_text("Si") 
    
    # Guarda el encabezado
    Elemento(GUARDAR['Encabezado']).click()
    wait.until(EC.alert_is_present()).accept() 

def servir(*parametros):
    for i in range(0, len(parametros), 2):
        servicio, donante = parametros[i:i+2]
        try:
            if float(servicio) < 2:
                dominio = 'Salud'
            elif float(servicio) > 5 and float(servicio) < 6:
                dominio = 'Fortalecimiento'
        except ValueError:
            break
        if not Elemento(SERVICIOS[servicio]).is_displayed():
            time.sleep(0.5)
            Elemento(DOMINIO[dominio]).click()
        WebDriverWait(driver,10).until(EC.visibility_of(Elemento(SERVICIOS[servicio])))
        Select(Elemento(SERVICIOS[str(servicio)])).select_by_index(1)
        if donante != 'N/A':
            Select(Elemento(DONANTE[str(servicio)])).select_by_index(donante) 
    Elemento(GUARDAR[dominio]).click()
    wait.until(EC.alert_is_present()).accept() # Espera

              
def beneficiario(col,fin): # Hace un recorrido entre los beneficiarios y le va marcando su servicio 
    indice = 1
    miembros = '//*[@id="MainContent_cbohhMember"]'
    cantidad = len(Elemento(miembros).find_elements('tag name','option'))-1
    while indice <= cantidad: 
        dominio = DOMINIO['Salud']
        servicio = SERVICIOS['1.4']
        Elemento(dominio).click()
        WebDriverWait(driver,10).until(EC.visibility_of(Elemento(servicio)))
        Select(Elemento(miembros)).select_by_index(indice)
        try:
            WebDriverWait(driver,10).until(EC.invisibility_of_element(Elemento(servicio)))  
        except UnexpectedAlertPresentException:
            print("Beneficiario tiene 21 años")   
        else:
            edad = driver.find_element('xpath','//*[@id="MainContent_txtAge"]').get_attribute("value")
            escuela = driver.find_element('xpath','//*[@id="MainContent_cboEnrolledInSchool"]')
            actividad = driver.find_element('xpath','//*[@id="MainContent_cboEnrolledEconomicActivity"]')
            flag = Elemento(miembros).get_attribute('value') in ben_salidos    
            if not flag: # Quité la comparación de la bandera con "False"       
                if int(edad) > 17 and int(edad) < 21:
                    Select(escuela).select_by_index(1)
                    Select(actividad).select_by_index(2)
                else:
                    Select(escuela).select_by_index(3)
                    Select(actividad).select_by_index(3)
                servir('1.4',6,'5.9',9,'N/A','N/A','N/A','N/A')
            else:
                print('Beneficiario salido')  
                Elemento(dominio).click()           
        indice += 1
    print('Servicio ' + str(col) + ' de ' + str(fin) + ' digitado')

# Pulir los tipos de datos de las listas de los datos a digitar, cambiar esos mismos datos en las funciones 
# que trabajan con ellos.

# Eliminar el diccionario de donantes y anexar cada elemento del mismo como una lista al lado de cada servicio
# correspondiente en dicho diccionario.