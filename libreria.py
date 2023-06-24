
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

"""

Librerias que no se estan usando de momento en este archivo

import pandas as pd
import pyperclip as ctrl
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
from datetime import datetime
""" 

class Mis:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
        self.wait = WebDriverWait(self.driver,10)
        self.driver.get("https://pactbrmis.org/Account/Login.aspx")
        self.login()
    
    def login(self): # Iniciar sesion
        self.driver.find_element('xpath','//*[@id="txtUsername"]').send_keys("jenielwtf@gmail.com")
        self.driver.find_element('xpath','//*[@id="txtPassword"]').send_keys("1qazxsw2")
        self.driver.find_element('xpath','//*[@id="btnLogin"]').click()   

    def acceder(self,enlace):
        self.driver.get(enlace)
        
    def elemento(self, ruta):
        elemento = self.driver.find_element('xpath',ruta)
        return(elemento)

    def seleccionar(self,ruta,valor='',por='index'):
        seleccionar = Select(self.elemento(ruta))
        if por == 'index':
            seleccionar.select_by_index(valor)
        elif por == 'valor':
            seleccionar.select_by_value(valor)
        elif por == 'texto':
            seleccionar.select_by_visible_text(valor)
        return(seleccionar)
    
    def extraer_cantidad(self, ruta):
        cantidad = len(self.elemento(ruta).find_elements('tag name', 'tr')) - 1
        return cantidad

    def cerrar(self):
        self.driver.close()

    def esperar_alerta(self):
        self.wait.until(EC.alert_is_present()).accept()

class Graduate(Mis): 
    
    def set_fecha(self, fecha):
        self.elemento('//*[@id="MainContent_txtDateAssessed"]').send_keys(fecha, Keys.ENTER)

    def select_hogar(self, hogar):
        self.elemento('//*[@id="select2-MainContent_ddlHHUniqueID-container"]').click()
        self.elemento('/html/body/span/span/span[1]/input').send_keys(hogar, Keys.ENTER)

    def abrir_formulario(self):
        self.acceder('https://pactbrmis.org/DataEntry/graduation_benchmark_assessment.aspx')
