"""
    Shaka
    Module for the Management Information System
    Inarixdono
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import date


class Driver:
    """
    Class for interacting with browser.
    """

    def __init__(self):
        self.today = date.today()
        self.driver = webdriver.Chrome(service=Service("driver\chromedriver.exe"))
        self.wait = WebDriverWait(self.driver, 10)

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
