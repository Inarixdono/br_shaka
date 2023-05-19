import Funciones as do
do.login()
do.col = 2

while do.col < 6:
    do.encabezado()
    do.beneficiario()
    do.col += 1

do.driver.quit()