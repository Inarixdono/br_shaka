"""
    Shaka
    Services form
    Inarixdono
"""

from libreria import Mis, DataFrameWrapper
from pandas import read_csv
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from functions import lista
from math import floor
from database import Database

df = read_csv(
    r"rsc\Servir.csv",
    delimiter=";",
    index_col="ID",
    dtype={
        "general_service": str,
        "general_donor": str,
        "beneficiaries_served": str,
        "individual_service": str,
        "individual_donor": str,
    },
)

xpath = DataFrameWrapper(read_csv(r"paths\ard006.csv", delimiter=";", index_col=0).T)
bd = Database()


class Service(Mis):
    """
    This class represents a service that can be performed on a group of beneficiaries.
    It contains methods for selecting and serving services, traversing members, and saving service data.
    """

    def __return_service(self, service: str):
        """
        Returns the service path, dominium path, and save path for a given service.
        Service xpaths are stored on the database.

        Args:
            service (str): The service to be returned.

        Returns:
            tuple: A tuple containing the service path, dominium path, and save path.
        """

        int_service: int = floor(float(service))
        dominium = f'//*[@id="MainContent_mainPanal"]/a[{int_service + 2}]'

        match int_service:
            case 1:
                save = xpath.save_prevention
            case 2:
                save = xpath.save_treatment
            case 3:
                save = xpath.save_support
            case 4:
                save = xpath.save_education
            case 5:
                save = xpath.save_protection
            case 6:
                save = xpath.save_main

        return bd.service_path(service), dominium, save

    def serve(self, services: tuple, donors: tuple, save=True):
        """
        Serves the given services for a member.

        Args:
            services (tuple): A tuple containing the services to be served.
            donors (tuple): A tuple containing the donors for each service.
            save (bool, optional): Whether or not to save the service data. Defaults to True.
        """

        for service, donor in zip(services, donors):
            service_path, dominium_path, save_path = self.__return_service(service)

            if not self.element(service_path).is_displayed():
                self.element(dominium_path).click()
            self.wait.until(EC.visibility_of(self.element(service_path)))
            self.select(service_path, 1)

            if donor != "0":
                donor_path = self.add_sufix(service_path, "donor_id")
                donor_element = self.element(donor_path)
                self.wait.until(EC.visibility_of(donor_element))
                self.select(donor_path, donor)

        if save:
            # TODO: SE ESTÁ PRESENTANDO UNA EXCEPCIÓN EN EL GUARDADO DEL DOMINIO DE SALUD
            #       HACER PRUEBAS Y CORREGIR.
            self.element(save_path).click()
            self.wait_for_alert()

    def header(self, row: int):
        """
        Sets the header data for the service form.

        Args:
            row (int): The row number of the group in the dataframe.
        """

        self.get(xpath.service_link)

        # Home and visit date
        self.select_household(xpath.home_container, df.home[row])
        self.fecha_visita = self.send_date(xpath.visit_date, df.date[row])

        # Reason and place
        # self.select(xpath.visit_reason, df.reason[row])
        self.select(xpath.visit_place, df.place[row])

        # Sign
        self.select(xpath.case_plan, 1)
        caregiver_select = self.select(xpath.caregiver_list, by="").options
        for caregiver in caregiver_select:
            if caregiver.text.split(" ")[0][-7:] == df.caregiver[row]:
                caregiver.click()
                self.wait_for_reload(caregiver)
                break
        self.select(xpath.caregiver_sign, 1)

        # Saving header
        self.element(xpath.save_header).click()
        self.wait_for_alert()

    def traverse_members(self, row: int):
        """
        Traverses the members list and performs services based on if they recieved.

        Args:
            row (int): The row number of the group in the dataframe.
        """

        servicio_general = df.general_service.tolist()[row].split(" ")
        servicio_individual = df.individual_service.tolist()[row].split(" ")
        servir_general = servicio_general[0] != "0"
        member_list = [
            o.text for o in self.select(xpath.member_list, by="").options[1:]
        ]

        for member in member_list:
            individual = member[-2:] in df.beneficiaries_served[row].split(" ")

            if not servir_general:
                if individual:
                    selected = member
                else:
                    continue
            else:
                selected = member

            try:
                self.select(xpath.member_list, selected, True, "text")
            except UnexpectedAlertPresentException:
                print("Beneficiario tiene 21 años")
            else:
                # Comprueba si el beneficiario esta activo
                if selected not in lista("Ben", "BenSalidos"):
                    age = int(self.element(xpath.age).get_attribute("value"))
                    if age in range(17, 21):
                        self.select(xpath.school, 1)
                        self.select(xpath.economic_activity, 2)
                    else:
                        self.select(xpath.school, 3)
                        self.select(xpath.economic_activity, 3)

                    if str(servicio_individual[0]) != "0" and individual:
                        self.serve(
                            servicio_individual,
                            df.individual_donor.tolist()[row].split(" "),
                            not servir_general,
                        )

                    if servir_general:
                        self.serve(
                            servicio_general, df.general_donor.tolist()[row].split(" ")
                        )
                else:
                    print("Beneficiario salido")

    def save_service(self, row: int):
        """
        Saves the service data for the given row into the database.

        Args:
            row (int): The row number of the group in the dataframe.

        Returns:
            None
        """

        columns = [i for i in range(11) if i not in [0, 1, 4, 5]]
        bd.insert_service(
            '{}, "{}", {}, {}, "{}", "{}", "{}", "{}", "{}"'.format(
                bd.return_id_home(df.home[row]),
                self.fecha_visita,
                *df.iloc[row, columns],
            )
        )


def main():
    sesion = Service()
    served_families = df.home

    for i in range(0, len(served_families)):
        if served_families[i] not in lista("Hogar", "FamSalidas"):
            sesion.header(i)
            sesion.traverse_members(i)
            print(f"Servicio {i + 1} de {len(served_families)} digitado")
        elif input("Familia salida, desea continuar?") == "s":
            sesion.traverse_members(i)
        else:
            print("Familia salida, no servida.")
        #sesion.save_service(i)

    sesion.almacen.close_connection()
    sesion.close()

# main()
