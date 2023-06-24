# Funciones externas a las clases del MIS

from datetime import datetime

class Herramienta:

    def format_fecha(fecha, from_csv = False):
        if not from_csv:
            if len(fecha) <= 5:
                fecha = datetime.strptime(fecha + '/23', '%d/%m/%y').strftime('%d/%m/%Y')
            else:
                fecha = datetime.strptime(fecha, '%d/%m/%y').strftime('%d/%m/%Y')
            return fecha
        else:
            fecha = datetime.strptime(fecha, '%d/%m/%Y').strftime('%d/%m/%Y')
            return fecha
