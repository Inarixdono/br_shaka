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
    """
    Class for interacting with the Management Information System.
    """

    def __init__(self):
        """
        Initializes the class and logs in to the MIS.
        """
        self.today = date.today()
        self.driver = webdriver.Chrome(service=Service("driver\chromedriver.exe"))
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://pactbrmis.org/Account/Login.aspx")
        self.__login()

    def __login(self):
        """
        Logs in to the MIS using the credentials from the credentials module.
        """
        self.element('//*[@id="txtUsername"]').send_keys(USER)
        self.element('//*[@id="txtPassword"]').send_keys(PASS)
        self.element('//*[@id="btnLogin"]').click()

    def get(self, link: str):
        """
        Navigates to the specified link.

        Args:
            link (str): The link to navigate to.
        """
        self.driver.get(link)

    def element(self, path: str):
        """
        Finds the element specified by the given xpath.

        Args:
            path (str): The xpath of the element to find.

        Returns:
            The element specified by the given xpath.
        """
        return self.driver.find_element("xpath", path)

    def select_household(self, path: str, home_code: str):
        """
        Selects the household with the given code.

        Args:
            path (str): The xpath of the household dropdown.
            home_code (str): The code of the household to select.
        """
        ref = self.element(path)
        code_input = "/html/body/span/span/span[1]/input"
        self.element(path).click()
        self.element(code_input).send_keys(home_code, Keys.ENTER)
        self.wait_for_reload(ref)

    def send_date(self, path: str, date_input: str, allows_entry=False):
        """
        Enters the given date into the specified input field.

        Args:
            path (str): The xpath of the input field.
            date_input (str): The date to enter in the format "dd/mm/yyyy".
            allows_entry (bool): Whether to allow manual entry of the date.

        Returns:
            The entered date in ISO format.
        """
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
        """
        Adds the given suffix to the given value.

        Args:
            value (str): The value to add the suffix to.
            sufix (str): The suffix to add.

        Returns:
            The value with the suffix added.
        """
        return value[:-2] + f"_{sufix}" + value[-2:]

    def send_keys(self, path: str, value: str):
        """
        Enters the given value into the specified input field.

        Args:
            path (str): The xpath of the input field.
            value (str): The value to enter.
        """
        self.element(path).send_keys(value)

    def send_other(self, path: str, other_path: str, value: str):
        """
        Enters the given value into the specified input field after clicking on another element.

        Args:
            path (str): The xpath of the element to click.
            other_path (str): The xpath of the input field.
            value (str): The value to enter.
        """
        self.element(path).click()
        self.wait_for_reload(self.element(path))
        self.element(other_path).send_keys(value)

    def select(self, path: str, value="", wait=False, by="index"):
        """
        Selects an option from the specified dropdown.

        Args:
            path (str): The xpath of the dropdown.
            value (str): The value to select.
            wait (bool): Whether to wait for the page to reload after selecting the option.
            by (str): The method to use for selecting the option ("index", "valor", or "text").

        Returns:
            The Select object for the specified dropdown.
        """
        ref = self.element(path)
        select = Select(ref)

        match by:
            case "index":
                select.select_by_index(value)
            case "valor":
                select.select_by_value(value)
            case "text":
                select.select_by_visible_text(value)
            case "":
                return select
            case _:
                print("Invalid selection method")

        if wait:
            self.wait_for_reload(ref)

    def close(self):
        """
        Closes the webdriver.
        """
        self.driver.close()

    def wait_for_reload(self, reference: element):
        """
        Waits for the specified element to reload.

        Args:
            reference (element): The element to wait for.
        """
        self.wait.until(EC.staleness_of(reference))

    def wait_for_alert(self):
        """
        Waits for an alert to appear and accepts it.
        """
        self.wait.until(EC.alert_is_present()).accept()


class DataFrameWrapper:
    """
    Wrapper class for a pandas DataFrame.
    """

    def __init__(self, df):
        """
        Initializes the wrapper with the given DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame to wrap.
        """
        self.df = df

    def __getattr__(self, name):
        """
        Gets the value of the specified column from the wrapped DataFrame.

        Args:
            name (str): The name of the column to get.

        Returns:
            The value of the specified column.
        """
        if name in self.df.columns:
            return self.df.iloc[0][name]
        else:
            raise AttributeError(f"'DataFrameWrapper' object has no attribute '{name}'")
