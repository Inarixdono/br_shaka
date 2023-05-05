import Elementos as od
import pyperclip as ctrl 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
from datetime import datetime

col = 0
driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
wait = WebDriverWait(driver,4)

def login(): # Iniciar sesion
    driver.get("https://pactbrmis.org/Account/Login.aspx")
    driver.find_element('xpath','//*[@id="txtUsername"]').send_keys("jenielwtf@gmail.com")
    driver.find_element('xpath','//*[@id="txtPassword"]').send_keys("1qazxsw2")
    driver.find_element('xpath','//*[@id="btnLogin"]').click()   
    
def firma(): #Firma y plan de caso
    Select(driver.find_element('xpath',od.XPATH.iloc[5,1])).select_by_visible_text("Si")
    firma = driver.find_element('xpath',od.XPATH.iloc[6,1])
    Select(firma).select_by_value(od.Servir.iloc[col,5])
    time.sleep(1)
    Select(driver.find_element('xpath',od.XPATH.iloc[7,1])).select_by_visible_text("Si")
    
def visita(): # Motivo y lugar de visita
    if od.Servir.iloc[col,2] == "Visita regular":  # Motivo de la Visita
        Select(driver.find_element('xpath',od.XPATH.iloc[3,1])).select_by_value("1") 
    elif od.Servir.iloc[col,2] == "Seguimiento":
        Select(driver.find_element('xpath',od.XPATH.iloc[3,1])).select_by_value("2")
    elif od.Servir.iloc[col,2] == "Monitoreo":
        Select(driver.find_element('xpath',od.XPATH.iloc[3,1])).select_by_value("3")
            
    if od.Servir.iloc[col,3] == "SAI":  # Lugar del servicio
        Select(driver.find_element('xpath',od.XPATH.iloc[4,1])).select_by_value("1")
    elif od.Servir.iloc[col,3] == "HOGAR":
        Select(driver.find_element('xpath',od.XPATH.iloc[4,1])).select_by_value("2")
        
def beneficiario(): # Hace un recorrido entre los beneficiarios y le va marcando su servicio 
    indice = 1
    miembros = driver.find_element('xpath','//*[@id="MainContent_cbohhMember"]')
    cantidad = len(miembros.find_elements('tag name','option'))-1
    while indice <= cantidad: 
        miembros = driver.find_element('xpath','//*[@id="MainContent_cbohhMember"]')
        dominio = driver.find_element('xpath','//*[@id="MainContent_mainPanal"]/a[3]')  
        servicio = driver.find_element('xpath','//*[@id="MainContent_cboOtherWashMaterialDistribution"]') 
        dominio.click()
        WebDriverWait(driver,10).until(EC.visibility_of(servicio))
        Select(miembros).select_by_index(indice)
        try:
            WebDriverWait(driver,10).until(EC.invisibility_of_element(servicio))  
        except UnexpectedAlertPresentException:
            print("Beneficiario tiene 21 años")
        else:
            miembros = driver.find_element('xpath','//*[@id="MainContent_cbohhMember"]')
            dominio = driver.find_element('xpath','//*[@id="MainContent_mainPanal"]/a[3]')  
            servicio = driver.find_element('xpath','//*[@id="MainContent_cboOtherWashMaterialDistribution"]') 
            edad = driver.find_element('xpath','//*[@id="MainContent_txtAge"]').get_attribute("value")
            escuela = driver.find_element('xpath','//*[@id="MainContent_cboEnrolledInSchool"]')
            actividad = driver.find_element('xpath','//*[@id="MainContent_cboEnrolledEconomicActivity"]')
            flag = miembros.get_attribute('value') in od.ben_salidos    
            if flag == False:       
                if int(edad) > 17 and int(edad) < 21:
                    Select(escuela).select_by_index(1)
                    Select(actividad).select_by_index(2)
                else:
                    Select(escuela).select_by_index(3)
                    Select(actividad).select_by_index(3)
                dominio.click() # Aquí empieza a servir
                WebDriverWait(driver,10).until(EC.visibility_of(servicio))
                Select(servicio).select_by_index(1)
                Select(driver.find_element('xpath','//*[@id="MainContent_cboOtherWashMaterialDistribution_dnr"]')).select_by_index(6)
                driver.find_element('xpath','//*[@id="MainContent_btnsaveHealth"]').click() # Guarda el servicio
                wait.until(EC.alert_is_present()).accept() # Espera
            else:
                print('Beneficiario salido')          
        indice += 1
    print('Servicio digitado')