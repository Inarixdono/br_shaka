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

def lista(columna, nombre = 'Servir', index='ID'):
    lista = pd.read_csv('Archivos\\'+ nombre +'.csv',delimiter=';', index_col= index, dtype= str)[columna].tolist()
    return(lista)

XPATH = lista('xPath','XPATH')
HOGAR = lista('Hogar')
driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
wait = WebDriverWait(driver,10)

def login(): # Iniciar sesion
    driver.get("https://pactbrmis.org/Account/Login.aspx")
    driver.find_element('xpath','//*[@id="txtUsername"]').send_keys("jenielwtf@gmail.com")
    driver.find_element('xpath','//*[@id="txtPassword"]').send_keys("1qazxsw2")
    driver.find_element('xpath','//*[@id="btnLogin"]').click()   

SERVICIOS = {'1.9':['//*[@id="MainContent_cboyn_art_retention"]'],
             '1.4':['//*[@id="MainContent_cboOtherWashMaterialDistribution"]','//*[@id="MainContent_cboOtherWashMaterialDistribution_dnr"]'],
             '5.9':['//*[@id="MainContent_cboFoodDeliveryservice"]','//*[@id="MainContent_cboFoodDeliveryservice_dnr"]'],
             '1.2':['//*[@id="MainContent_cboyn_wash"]']}

DOMINIO = {'Salud':'//*[@id="MainContent_mainPanal"]/a[3]',
           'Fortalecimiento':'//*[@id="MainContent_mainPanal"]/a[7]'}

GUARDAR = {'Salud':'//*[@id="MainContent_btnsaveHealth"]',
           'Fortalecimiento':'//*[@id="MainContent_btnsave"]',
           'Encabezado':'//*[@id="MainContent_btnsaveMain"]'}

def Elemento(ruta):
    Elemento = driver.find_element('xpath',ruta)
    return(Elemento)

def Seleccionar(ruta,valor='',por='index'):
    Seleccionar = Select(Elemento(ruta))
    if por == 'index':
        Seleccionar.select_by_index(valor)
    elif por == 'valor':
        Seleccionar.select_by_value(valor)
    elif por == 'texto':
        Seleccionar.select_by_visible_text(valor)
    return(Seleccionar)

def encabezado(fila): 

    # Entra al formulario de entrada de servicios
    driver.get("https://pactbrmis.org/DataEntry/service_delivery.aspx?tokenID=&action=") 

    # Selecciona el hogar y asigna la fecha
    Elemento(XPATH[0]).click() 
    Elemento(XPATH[1]).send_keys(HOGAR[fila], Keys.ENTER)
    set_fecha = datetime.strptime(lista('FechaVisita')[fila], '%d/%m/%Y')
    fecha = set_fecha.strftime('%d/%m/%Y')
    ctrl.copy(fecha)
    Elemento(XPATH[2]).send_keys(Keys.CONTROL, 'v', Keys.ENTER)

    # Motivo y lugar de visita
    Select(Elemento(XPATH[3])).select_by_visible_text(lista('MotivoVisita')[fila])      
    Select(Elemento(XPATH[4])).select_by_visible_text(lista('EntregaEn')[fila])

    # Firma
    Select(Elemento(XPATH[5])).select_by_visible_text("Si") 
    Select(Elemento(XPATH[6])).select_by_value(lista('Idcare')[fila]) 
    time.sleep(1) #TODO: MEJORAR ESTA ESPERA
    Select(Elemento(XPATH[7])).select_by_visible_text("Si") 
    
    # Guarda el encabezado
    Elemento(GUARDAR['Encabezado']).click()
    wait.until(EC.alert_is_present()).accept() 

def servir(servicios, donantes, guardar = True):
    for i in range(len(servicios)):
        try:
            if 1 < float(servicios[i]) < 2:
                dominio = 'Salud'
            elif 5 < float(servicios[i]) < 6:
                dominio = 'Fortalecimiento'
        except ValueError:
            break
        if not Elemento(SERVICIOS[servicios[i]][0]).is_displayed():
            time.sleep(0.5)
            Elemento(DOMINIO[dominio]).click()
        wait.until(EC.visibility_of(Elemento(SERVICIOS[servicios[i]][0])))
        Seleccionar(SERVICIOS[servicios[i]][0],1)
        if donantes[i] != '0':
            Seleccionar(SERVICIOS[servicios[i]][1],donantes[i])
    if guardar:
        Elemento(GUARDAR[dominio]).click()
        wait.until(EC.alert_is_present()).accept() # Espera

def beneficiario(fila): # Hace un recorrido entre los beneficiarios y le va marcando su servicio 

    servicio_general = lista('S_GENERAL')[fila].split(' ')
    donante_general = lista('D_GENERAL')[fila].split(' ')
    servido_individual = lista('B_SERVIDO')[fila].split(' ')
    servicio_individual = lista('SERVBEN')[fila].split(' ')
    donante_individual = lista('D_BENSERV')[fila].split(' ')

    for indice in range(1, len(Seleccionar(XPATH[8],por='').options)): 
        Elemento(DOMINIO['Salud']).click()
        wait.until(EC.visibility_of(Elemento(SERVICIOS['1.4'][0])))
        Seleccionar(XPATH[8],indice)
        try:
            wait.until(EC.invisibility_of_element(Elemento(SERVICIOS['1.4'][0])))  
        except UnexpectedAlertPresentException:
            print("Beneficiario tiene 21 años")       
        else:
                    # Comprueba si el beneficiario esta activo
            if not Elemento(XPATH[8]).get_attribute('value') in lista('ID','BenSalidos','Ben'): 
                    
                    # Comprueba la edad del beneficiario
                if int(Elemento(XPATH[9]).get_attribute('value')) in range(17, 21): 
                    Seleccionar(XPATH[10],1)
                    Seleccionar(XPATH[11],2)
                else:
                    Seleccionar(XPATH[10],3)
                    Seleccionar(XPATH[11],3)

                    # Comprueba si el hogar recibe algun servicio individua   
                if str(servicio_individual[0]) != '0':
                    if Elemento(XPATH[8]).text.splitlines()[indice][-2:] in servido_individual:
                        servir(servicio_individual,donante_individual, servicio_general[0] == '0')
                
                if str(servicio_general[0]) != '0': servir(servicio_general, donante_general)
                
            else:
                print('Beneficiario salido')  
                Elemento(DOMINIO['Salud']).click()           


# Solo esta funcionando adecuadamente cuando el hogar cuenta con un servicio general o el servicio individula
# es aplicado al primer beneficiario