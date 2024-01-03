"""
    Shaka
    Module for webscraping on FAPPS.
    Inarixdono
"""

from driver import Driver, DataFrameWrapper
from pandas import read_csv
from credentials import FAPPS_USER, FAPPS_PASS


xpath = DataFrameWrapper(read_csv(r"paths\fapps.csv", delimiter=";", index_col=0).T)


class FAPPS(Driver):
    """
    Class for interacting with FAPPS.
    """

    def __init__(self):
        super().__init__()
        self.driver.get(xpath.form)
        self.__login()

    def __login(self):
        """
        Logs in to FAPPS using the credentials from the credentials module.
        """
        self.send_keys(xpath.txt_user, FAPPS_USER)
        self.send_keys(xpath.txt_pass, FAPPS_PASS)
        self.element(xpath.btn_login).click()

    def search_patient(self, patient_id: str):
        """
        Searches for a patient with the given ID.

        Args:
            patient_id (str): The ID of the patient to search for.
        """
        self.get(xpath.form)
        txt_id = self.element(xpath.txt_id)
        txt_id.send_keys(patient_id)
        self.element(xpath.btn_submit).click()
        self.wait_for_reload(txt_id)

    def get_appointment(self):
        """
        Gets the appointment for the patient currently selected.
        """
        btn_tracing = self.element(xpath.btn_tracing)
        btn_tracing.click()
        self.wait_for_reload(btn_tracing)
        return self.element(xpath.appointment).text
    
    def get_amount(self):
        """
        Gets the amount of medicine the patient currently selected has in their last tracing.
        """
        btn_medicine = self.element(xpath.btn_medicine)
        btn_medicine.click()
        self.wait_for_reload(btn_medicine)
        return self.element(xpath.amount).text

