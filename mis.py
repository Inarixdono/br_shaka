"""
    Shaka
    Module for the Management Information System
    Inarixdono
"""

from driver import Driver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pyperclip as ctrl
from credentials import MIS_USER, MIS_PASS


class MIS(Driver):
    """
    Class for interacting with the Management Information System.
    """

    def __init__(self):
        """
        Initializes the class and logs in to the MIS.
        """
        super.__init__()
        self.driver.get("https://pactbrmis.org/Account/Login.aspx")
        self.__login()

    def __login(self):
        """
        Logs in to the MIS using the credentials from the credentials module.
        """
        self.element('//*[@id="txtUsername"]').send_keys(MIS_USER)
        self.element('//*[@id="txtPassword"]').send_keys(MIS_PASS)
        self.element('//*[@id="btnLogin"]').click()

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