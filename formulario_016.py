"""
    Shaka
    Graduation form
    Inarixdono
"""

from libreria import Mis, DataFrameWrapper
from pandas import read_csv

xpath = DataFrameWrapper(read_csv(r"paths\ard016.csv", delimiter=";", index_col=0).T)


class Graduate(Mis):
    def tabla(self, n):
        return f'//*[@id="MainContent_gvBenchmark{n}"]/tbody'

    def extraer_cantidad(self, path):
        return len(self.element(path).find_elements("tag name", "tr")) - 1

    def format_preguntas(self, n):
        # Para el punto
        P = (
            f'//*[@id="MainContent_gvBenchmark8_ddlChildEnrolledInSchool_{n}"]',
            f'//*[@id="MainContent_gvBenchmark8_ddlChildAttendedSchoolRegularly_{n}"]',
            f'//*[@id="MainContent_gvBenchmark8_ddlChildProgressedToNextGrade_{n}"]',
            f'//*[@id="MainContent_gvBenchmark8_ddlPCGAnswerYesToAllBM8_{n}"]',
        )
        return P

    def encabezado(self):
        self.get(xpath.graduation_link)
        self.send_date(xpath.assessment_date, input("Fecha de evaluacion"), True)
        self.select_household(xpath.home_container, input("Codigo del hogar"))

        previously_assessed = input("Previamente evaluado?")
        self.select(xpath.previously_assessed, previously_assessed)
        if str(previously_assessed) == "1":
            self.send_date(xpath.assessed_date, input("Fecha en que fue evaluado"), True)

    def punto_1(self):
        for i in range(self.extraer_cantidad(self.tabla(1))):
            r = input("Fecha en la que se reporta estatus")
            if r == "1":
                continue
            elif r == "0":
                break
            else:
                self.send_date(
                    f'//*[@id="MainContent_gvBenchmark1_txtDateHIVStatusDocumented_{i}"]',
                    r,
                    True,
                )

    def punto_2(self):
        for i in range(self.extraer_cantidad(self.tabla(2))):
            p2a = f'//*[@id="MainContent_gvBenchmark2_ddlAttendingARTAppointments_{i}"]'
            p2b = (
                f'//*[@id="MainContent_gvBenchmark2_ddlTakingARTPillsAsPrescribed_{i}"]'
            )
            if self.element(p2a).is_enabled():
                r = input("Digitar respuestas para punto 2")
                self.select(p2a, r[0])
                self.select(p2b, r[1])

    def punto_3(self):
        beneficiarios = self.extraer_cantidad(self.tabla(3)) / 22
        if int(beneficiarios) != 0:
            for b in range(
                int(beneficiarios)
            ):  # Para repetir por la cantidad de beneficiarios
                respuestas = 0

                r = input("Pregunta 3.1")
                for i in range(
                    len(str(r))
                ):  # Para repetir en base al input a la pregunta 3.1
                    self.element(
                        f'//*[@id="MainContent_gvBenchmark3_cblWaysOfGettingHIV_{b}_{r[i]}_{b}"]'
                    ).click()
                    respuestas += 1

                r = input("Pregunta 3.2")
                for i in range(
                    len(str(r))
                ):  # Para repetir en base al input a la pregunta 3.2
                    self.element(
                        f'//*[@id="MainContent_gvBenchmark3_cblWaysOfProtectingAgainstHIV_{b}_{r[i]}_{b}"]'
                    ).click()
                    respuestas += 1

                r = input("Pregunta 3.3")
                for i in range(
                    len(str(r))
                ):  # Para repetir en base al input a la pregunta 3.3
                    self.element(
                        f'//*[@id="MainContent_gvBenchmark3_cblWhereHIVPreventionSupport_{b}_{r}_{b}"]'
                    ).click()
                    if str(r[i]) == "4":
                        self.element(
                            f'//*[@id="MainContent_gvBenchmark3_txtWhereHIVPreventionSupportOther_{b}"]'
                        ).send_keys(input("Otro"))
                    respuestas += 1

                if respuestas > 4:
                    self.select(
                        f'//*[@id="MainContent_gvBenchmark3_ddlChildAwareOfHIVRisksAndPreventionMeasures_{b}"]',
                        1,
                    )
                else:
                    self.select(
                        f'//*[@id="MainContent_gvBenchmark3_ddlChildAwareOfHIVRisksAndPreventionMeasures_{b}"]',
                        2,
                    )

    def punto_4(self):
        p4a = self.extraer_cantidad(self.tabla(4))
        p4b = self.extraer_cantidad(self.tabla("4b"))

        if p4a != 0:
            for i in range(p4a):
                self.select(
                    f'//*[@id="MainContent_gvBenchmark4_ddlChildMUACMoreThan12_5_{i}"]',
                    1,
                )
                self.select(
                    f'//*[@id="MainContent_gvBenchmark4_ddlChildFreeOfAnySignsOfBipedalEdema_{i}"]',
                    1,
                )

        if p4b != 0:
            for i in range(p4b):
                print("agregar rutas")  # TODO: AGREGAR RUTAS

    def punto_5(self):
        P = (
            '//*[@id="MainContent_ddlAbleToPayForMedicalCosts"]',
            '//*[@id="MainContent_ddlAbleToPayForMedicalCostsWithoutCashTransfer"]',
            '//*[@id="MainContent_ddlAbleToPayForMedicalCostsWithoutSellingAnything"]',
            '//*[@id="MainContent_ddlAbleToPayForSchoolSupplies"]',
            '//*[@id="MainContent_ddlAbleToPayForSchoolSuppliesWithoutFinancialAid"]',
            '//*[@id="MainContent_ddlAbleToPayForSchoolSuppliesWithoutSellingAnything"]',
        )
        # TODO: SIMPLIFICAR
        r = input("Punto 5")
        if r == "1a":
            for i in range(6):
                try:
                    self.select(P[i], 1)
                except NotImplementedError:
                    break
        elif r == "2a":
            for i in range(6):
                try:
                    self.select(P[i], 2)
                except NotImplementedError:
                    break
        else:
            for i in range(len(str(r))):
                try:
                    self.select(P[i], int(r[i]))
                except NotImplementedError:
                    break

    def p6to7(self):
        P = (
            '//*[@id="MainContent_ddlAwareOfAnyPhysicalAbuse"]',
            '//*[@id="MainContent_ddlAwareOfAnySexualAbuse"]',
            '//*[@id="MainContent_ddlChildrenUnderCareOfStableAdultCaregiver"]',
        )

        for i in range(3):
            if i < 2:
                self.select(P[i], 2)
            else:
                self.select(P[i], 1)

    def punto_8(self):
        beneficiarios = self.extraer_cantidad(self.tabla(8))
        if beneficiarios != 0:
            for b in range(beneficiarios):
                for p in range(4):
                    self.select(self.format_preguntas(b)[p], 1)
