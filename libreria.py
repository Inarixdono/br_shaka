"""
    Shaka
    Module for the Management Information System
    Inarixdono
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime, date
import pyperclip as ctrl
from credentials import USER, PASS


class Mis:

    
    def __init__(self):
        self.today = date.today()
        self.driver = webdriver.Chrome(service=Service("driver\chromedriver.exe"))
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://pactbrmis.org/Account/Login.aspx")
        self.__login()

    def __login(self):  # Iniciar sesion
        self.element('//*[@id="txtUsername"]').send_keys(USER)
        self.element('//*[@id="txtPassword"]').send_keys(PASS)
        self.element('//*[@id="btnLogin"]').click()

    def get(self, link: str):
        self.driver.get(link)

    def element(self, path: str):
        return self.driver.find_element("xpath", path)

    def select_household(self, path: str, home_code: str):
        ref = self.element(path)
        code_input = "/html/body/span/span/span[1]/input"
        self.element(path).click()
        self.element(code_input).send_keys(home_code, Keys.ENTER)
        self.wait_for_reload(ref)

    def send_date(self, path: str, date_input: str, allows_entry=False):
        match len(date_input):
            case 2:
                date_output = datetime.strptime(
                    f"{date_input}/{self.today.month}/{self.today.year}", "%d/%m/%Y"
                )
            case 5:
                date_output = datetime.strptime(
                    f"{date_input}/{self.today.year}", "%d/%m/%Y"
                )
            case 10:
                date_output = datetime.strptime(date_input, "%d/%m/%Y")
            case _:
                raise ValueError

        mis_format = date_output.strftime("%d/%m/%Y")

        if allows_entry:
            self.element(path).send_keys(mis_format, Keys.ENTER)
        else:
            ctrl.copy(mis_format)
            self.element(path).send_keys(Keys.CONTROL, "v", Keys.ENTER)

        return date_output.isoformat().split("T")[0]

    def add_sufix(self, value: str, sufix: str):
        return value[:-2] + f"_{sufix}" + value[-2:]

    def send_keys(self, path: str, value: str):
        self.element(path).send_keys(value)

    def send_other(self, path: str, other_path: str, value: str):
        self.element(path).click()
        self.wait_for_reload(self.element(path))
        self.element(other_path).send_keys(value)

    def select(self, path: str, value= "", wait= False, by= "index"):
        ref = self.element(path)
        seleccionar = Select(ref)

        match by:
            case "index":
                seleccionar.select_by_index(value)
            case "valor":
                seleccionar.select_by_value(value)
            case "text":
                seleccionar.select_by_visible_text(value)
            case "":
                return seleccionar
            case _:
                print("Invalid selection method")

        if wait:
            self.wait_for_reload(ref)

    def close(self):
        self.driver.close()

    def wait_for_reload(self, reference: element):
        self.wait.until(EC.staleness_of(reference))

    def wait_for_alert(self):
        self.wait.until(EC.alert_is_present()).accept()


class DataFrameWrapper:
    def __init__(self, df):
        self.df = df

    def __getattr__(self, name):
        if name in self.df.columns:
            return self.df.iloc[0][name]
        else:
            raise AttributeError(f"'DataFrameWrapper' object has no attribute '{name}'")