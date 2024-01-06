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
        self.__has_tracing = False
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
        self.__has_tracing = False

    def step_into(self, path: str):
        """
        Gets into the given path, clicks a button and wait for reload.

        Args:
            path (str): The path to step into.
        """
        btn = self.element(path)
        btn.click()
        self.wait_for_reload(btn)

    def get_appointment(self):
        """
        Gets the appointment for the patient currently selected.
        """
        appointment = "No tiene seguimiento"
        
        try:
            self.step_into(xpath.btn_tracing)
            appointment = self.element(xpath.appointment).text
        except Exception:
            print("El paciente no tiene seguimiento")
        else:
            self.__has_tracing = True
        return appointment

    def get_amount(self):
        """
        Gets the amount of medicine the patient currently selected has in their last tracing.
        """
        amount = 0
    
        if self.__has_tracing:
            self.step_into(xpath.btn_medicine)
            amount = self.element(xpath.amount).text

        return amount
    
    def get_cv(self):
        """
        Gets the viral charge of the patient currently selected.
        """
        cv_date = "00/00/0000"
        cv_result = "0"

        if self.__has_tracing:
            self.step_into(xpath.btn_return)
            self.step_into(xpath.btn_changes)
            cv_date = self.element(xpath.txt_date_cv).get_attribute("value")
            cv_result = self.element(xpath.txt_cv).get_attribute("value")

        return cv_date, cv_result
    
    def main(self):
        
        df = read_csv(r"rsc\Pacientes VIH.csv", delimiter=";", index_col=0)
        columnas = ["Nombre", "Código", "Record", "FAPPS", "Cita", "Cantidad", "Fecha CV", "Resultado CV", "Comentario", "Gestor"]
        cita = []
        cantidad = []
        fecha_cv = []
        resultado_cv = []
        
        for paciente in df.fapps:
            self.search_patient(paciente)
            cita.append(self.get_appointment())
            cantidad.append(self.get_amount())
            fecha, resultado = self.get_cv()
            fecha_cv.append(fecha)
            resultado_cv.append(resultado)

        df.cita = cita
        df.cantidad = cantidad
        df.fecha_cv = fecha_cv
        df.resultado_cv = resultado_cv
        df.columns =  columnas
        df.to_excel(r"rsc\Pacientes VIH.xlsx")

        #TODO: Mandar fechas de manera que Excel las reconozca como fechas.
        #TODO: Eficientar manera en que se mandan los datos al dataframe.
        #TODO: Agregar manejo de datos faltantes para la base de datos y excel.