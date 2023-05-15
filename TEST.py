import Funciones as do
do.login()

while do.col < 4:
    do.encabezado
    do.beneficiario
    do.col += 1

do.driver.quit()