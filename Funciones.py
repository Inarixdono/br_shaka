import Elementos as od
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

driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
wait = WebDriverWait(driver,10)

def login(): # Iniciar sesion
    driver.get("https://pactbrmis.org/Account/Login.aspx")
    driver.find_element('xpath','//*[@id="txtUsername"]').send_keys("jenielwtf@gmail.com")
    driver.find_element('xpath','//*[@id="txtPassword"]').send_keys("1qazxsw2")
    driver.find_element('xpath','//*[@id="btnLogin"]').click()   

def encabezado(col): 

    # Entra al formulario de entrada de servicios
    driver.get("https://pactbrmis.org/DataEntry/service_delivery.aspx?tokenID=&action=") 

    # Selecciona el hogar y asigna la fecha
    driver.find_element('xpath',od.XPATH.iloc[0,1]).click() 
    driver.find_element('xpath', od.XPATH.iloc[1,1]).send_keys(od.HOGAR[col], Keys.ENTER)
    set_fecha = datetime.strptime(od.FECHA[col], '%d/%m/%Y')
    fecha = set_fecha.strftime('%d/%m/%Y')
    ctrl.copy(fecha)
    driver.find_element('xpath',od.XPATH.iloc[2,1]).send_keys(Keys.CONTROL, 'v', Keys.ENTER)

    # Motivo y lugar de visita
    Select(driver.find_element('xpath',od.XPATH.iloc[3,1])).select_by_visible_text(od.MOTIVO[col])      
    Select(driver.find_element('xpath',od.XPATH.iloc[4,1])).select_by_visible_text(od.LUGAR[col])

    # Firma
    Select(driver.find_element('xpath',od.XPATH.iloc[5,1])).select_by_visible_text("Si") 
    Select(driver.find_element('xpath',od.XPATH.iloc[6,1])).select_by_value(od.CUIDADOR[col]) 
    time.sleep(1) #TODO: MEJORAR ESTA ESPERA
    Select(driver.find_element('xpath',od.XPATH.iloc[7,1])).select_by_visible_text("Si") 
    
    # Guarda el encabezado
    driver.find_element('xpath','//*[@id="MainContent_btnsaveMain"]').click()
    wait.until(EC.alert_is_present()).accept() 

def servir(servicio, dnrcode = 'N/A', serv2 = 'N/A', dnr2 = 'N/A'):

    if servicio == '1.40' or servicio == '1.9':
        dominio = 'Salud'
    elif servicio == '5.9':
        dominio = 'Fortalecimiento'

    driver.find_element('xpath', od.dominio[dominio]).click()
    WebDriverWait(driver,10).until(EC.visibility_of(driver.find_element('xpath',od.servicios[servicio])))
    Select(driver.find_element('xpath',od.servicios[servicio])).select_by_index(1)
    if dnrcode != 'N/A':
        Select(driver.find_element('xpath',od.donante[servicio])).select_by_index(dnrcode)
    
    if dnr2 != 'N/A':
        servicio = serv2
        dnrcode = dnr2
        servir(servicio, dnrcode)

    driver.find_element('xpath',od.guardar[dominio])
    
        
       
def beneficiario(): # Hace un recorrido entre los beneficiarios y le va marcando su servicio 
    indice = 1
    miembros = driver.find_element('xpath','//*[@id="MainContent_cbohhMember"]')
    cantidad = len(miembros.find_elements('tag name','option'))-1
    while indice <= cantidad: 
        miembros = driver.find_element('xpath','//*[@id="MainContent_cbohhMember"]')
        dominio = driver.find_element('xpath',od.dominio['Salud'])  
        servicio = driver.find_element('xpath',od.servicios['1.40']) 
        dominio.click()
        WebDriverWait(driver,10).until(EC.visibility_of(servicio))
        Select(miembros).select_by_index(indice)
        try:
            WebDriverWait(driver,10).until(EC.invisibility_of_element(servicio))  
        except UnexpectedAlertPresentException:
            print("Beneficiario tiene 21 años")
            dominio = driver.find_element('xpath',od.dominio['Salud'])
            dominio.click()      
        else:
            miembros = driver.find_element('xpath','//*[@id="MainContent_cbohhMember"]')
            dominio = driver.find_element('xpath',od.dominio['Salud'])  
            servicio = driver.find_element('xpath',od.servicios['1.40']) 
            edad = driver.find_element('xpath','//*[@id="MainContent_txtAge"]').get_attribute("value")
            escuela = driver.find_element('xpath','//*[@id="MainContent_cboEnrolledInSchool"]')
            actividad = driver.find_element('xpath','//*[@id="MainContent_cboEnrolledEconomicActivity"]')
            flag = miembros.get_attribute('value') in od.ben_salidos    
            if not flag: # Quité la comparación de la bandera con "False"       
                if int(edad) > 17 and int(edad) < 21:
                    Select(escuela).select_by_index(1)
                    Select(actividad).select_by_index(2)
                else:
                    Select(escuela).select_by_index(3)
                    Select(actividad).select_by_index(3)
                servir('1.40', 6,'5.9',9)
                wait.until(EC.alert_is_present()).accept() # Espera
            else:
                print('Beneficiario salido')  
                dominio = driver.find_element('xpath',od.dominio['Salud'])
                dominio.click()           
        indice += 1
    print('Servicio digitado')

    # Probar la funcion beneficiarios repetidas veces con familias que tengan beneficiarios salidos
    # y mayores de 18 años para capturar errores.