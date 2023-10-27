"""
Shaka
Formularios de registro
Inarixdono
"""

from libreria import Mis, DataFrameWrapper
from selenium.webdriver.common.keys import Keys
from pandas import read_csv
from database import HIVPatient, Database, HomeMember

xpath_01 = DataFrameWrapper(read_csv(r"paths\ard001.csv", delimiter=";", index_col=0).T)


class Identification(Mis):
    def __header(
        self,
        navigator: str,
        date: str,
        user: str,
        record: str,
        fapps: str,
        gender: int,
        age: int,
    ):
        self.index_member = HIVPatient(user, gender, age, record, fapps, True)

        self.get(xpath_01.identification_link)
        self.select(xpath_01.ngo, 1, True)  # Ong
        self.select(xpath_01.sai, 1, True)  # Sai
        self.send_keys(xpath_01.navigator, navigator)  # Navegador
        self.send_date(xpath_01.identification_date, date, True)  # Fecha
        self.send_keys(
            xpath_01.index_name,
            self.index_member.name[0],
            " ",
            self.index_member.surname[0],
        )  # Usuario
        self.send_keys(xpath_01.record, record)  # Record
        self.send_keys(xpath_01.fapps, fapps)  # ID Fapps
        self.select(xpath_01.index_gender, gender, True)  # Sexo

    def __step_1(self, place: int, has_children=True, enrolled=False):
        self.select(xpath_01.question_1, place, True)  # P1
        self.send_keys(
            xpath_01.question_2, Keys.UP * (self.index_member.age - 14)
        )  # P2
        self.select(xpath_01.question_3, 1, True)
        self.select(xpath_01.question_4, 1, True)

        for i in range(3):
            p4b = self.element(f'//*[@id="MainContent_lstHaitianDescentCategory_{i}"]')
            p4b.click()
            self.wait_for_reload(p4b)

        if self.index_member.age > 17:
            underaged = False
            self.select(xpath_01.question_5, 2, True)
        else:
            underaged = True
            self.select(xpath_01.question_5, 1, True)
            r = input("Seleccione la categoria: ")
            self.select(xpath_01.question_5b, r, True)
            has_children = False

        if not underaged:
            if has_children:
                self.select(xpath_01.question_6, 1, True)
            else:
                self.select(xpath_01.question_6, 2, True)

        if not enrolled:
            self.select(xpath_01.question_9, 2, True)
        else:
            self.select(xpath_01.question_9, 1, True)

    def __step_2(self, consent=True):
        if consent:
            self.select(xpath_01.question_10, 1, True)
            self.index_member.home_code = self.element(xpath_01.homecode).get_attribute(
                "value"
            )
        else:
            self.select(xpath_01.question_10, 2, True)
            r = input("Razon por la que no quiere entrar al proyecto: ")
            self.element(f'//*[@id="MainContent_lstnonConsentReason_{r}"]')
            if r == "3":
                r = input("Otra razón, especifique: ")
                self.send_other(xpath_01.question_11, xpath_01.question_11b, r)

        # TODO: AGREGAR BOTON DE GUARDAR

    def main_test():
        sesion = Identification()
        sesion.__header("asdad", "05/07/2023", "Horacio vaque", "585", "25565", 1, 24)
        sesion.__step_1(1)
        sesion.__step_2()
        sesion.close()


xpath_03 = DataFrameWrapper(read_csv(r"paths\ard003.csv", delimiter=";", index_col=0).T)


class Register(Identification):
    def __init__(
        self, new=True, home="", name="", gender=0, age=0, record="", fapps=""
    ):
        self.acceso = Database()
        if not new:
            self.index_member = HIVPatient(name, gender, age, record, fapps)
            self.index_member.home_code = home
        super().__init__()

    def header(self, gestor, community, verification_date):
        address = self.acceso.return_comunidad(community)
        self.verification_date = verification_date
        self.get(xpath_03.register_link)
        self.select_household(xpath_03.home_container, self.index_member.home_code)
        self.select(xpath_03.sai, 4, True)  # Sai
        self.select(xpath_03.supervisor, 1)  # Supervisor
        self.select(xpath_03.promoter, gestor)  # Gestor

        self.select_household(xpath_03.province, address[3])  # Provincia
        self.select_household(xpath_03.municipality, address[2])  # Municipio
        self.select(xpath_03.district, address[1], True, "texto")  # Distrito
        self.select(xpath_03.community, address[0], True, "texto")  # Comunidad

        self.send_keys(
            xpath_03.index_name,
            (self.index_member.name[0], " ", self.index_member.surname[0]),
        )  # Usuario
        self.send_date(
            xpath_03.verification_date, self.verification_date
        )  # Fecha de verificacion

    def contact_mode(self, r: tuple):
        self.select(xpath_03.question_1, str(r[0]), True, "texto")
        self.select(xpath_03.question_2, str(r[1]), True, "texto")
        self.select(xpath_03.question_3, r[2], True)

        match r[2]:
            case 1:
                self.select(xpath_03.question_4, r[3], True)
            case 2:
                self.select(xpath_03.question_5, r[3], True)

    def step_1(
        self, principal_caregiver: bool, location: int, proxima_cita, pcg_name=""
    ):
        self.send_keys(xpath_03.question_6, Keys.UP * (self.index_member.age - 14))
        self.select(xpath_03.question_7, 1, True)
        self.select(xpath_03.question_8, 1, True)

        for i in range(3):  # P8b
            p8b = self.element(f'//*[@id="MainContent_lstHaitianDescentCategory_{i}"]')
            p8b.click()
            self.wait_for_reload(p8b)

        if self.index_member.age > 17:  # P9
            underaged = False
            self.select(xpath_03.question_9, 2, True)
        else:
            underaged = True
            self.select(xpath_03.question_9, 1, True)
            r = input("Seleccione la categoria: ")
            self.select(xpath_03.question_9b, r, True)

        if not underaged:  # P10
            self.select(xpath_03.question_10, 1, True)

        if principal_caregiver:  # P13
            self.principal_caregiver = self.index_member
            self.select(xpath_03.question_13, 1, True)

        else:  # P14
            self.secondary_caregiver = self.index_member
            self.principal_caregiver = HomeMember(pcg_name, 0, 0)
            self.select(xpath_03.question_13, 2)
            self.send_keys(
                xpath_03.question_14a,
                (
                    self.principal_caregiver.name[0],
                    " ",
                    self.principal_caregiver.surname[0],
                ),
            )
            self.select(xpath_03.question_14b, 1)

        self.select(xpath_03.question_15, 1, True)  # P15
        self.select(xpath_03.question_15a, location, True)
        self.send_date(xpath_03.question_15b, self.verification_date)
        # TODO: BOTON DE GUARDAR

        self.send_date(xpath_03.roster_date, self.verification_date)
        self.send_date(xpath_03.next_visit, proxima_cita)
        # TODO: BOTON DE GUARDAR


respuestas = [0, 1, 2, 1]
prueba = Register(False, "PU/GRE/CG/0004", "Junina Petite Home", 2, 25, "859", "85695")
prueba.header(1, "Muñoz", "03/08/2023")
prueba.contact_mode(respuestas)
prueba.step_1(True)
prueba.close()