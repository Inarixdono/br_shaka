import pandas as pd
import pyperclip as ctrl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime


'''
driver = webdriver.Chrome(service=Service('driver\chromedriver.exe'))
wait = WebDriverWait(driver,10)

def lista(columna,nombre,index):
    lista = pd.read_csv('Archivos\\'+ nombre +'.csv',delimiter=';', index_col= index, dtype= str)[columna].tolist()
    return(lista)

def login(): # Iniciar sesion
    driver.get("https://pactbrmis.org/Account/Login.aspx")
    driver.find_element('xpath','//*[@id="txtUsername"]').send_keys("jenielwtf@gmail.com")
    driver.find_element('xpath','//*[@id="txtPassword"]').send_keys("1qazxsw2")
    driver.find_element('xpath','//*[@id="btnLogin"]').click()   

def Elemento(ruta):
    Elemento = driver.find_element('xpath',ruta)
    return(Elemento)

def Seleccionar(ruta,valor,por):
    Seleccionar = Select(Elemento(ruta))
    if por == 'index':
        Seleccionar.select_by_index(valor)
    elif por == 'valor':
        Seleccionar.select_by_value(valor)
    elif por == 'texto':
        Seleccionar.select_by_visible_text(valor)
    return(Seleccionar)

'''