import json
import os

# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL v 0.1.4
# ============================================================
# Este programa permite registrar y consultar expedientes
# de los usuarios de SEDAPAL - San Juan de Lurigancho.
# Version de proyecto Ver 0.1.4
# ============================================================

# ------------------------------------------------------------
# LISTA PRINCIPAL DE EXPEDIENTES
# ------------------------------------------------------------
# Esta lista almacenará todos los expedientes registrados, Cada expediente será una lista con sus datos.
# Por ahora no utilizamos una base de datos.
expedientes = []

# ------------------------------------------------------------
# BASE DE DATOS LOCAL PARA SIMULAR UNA CONSULTA A RENIEC
# Los registros se almacenan en base_dni_sedapal.json.
# Son datos de demostracion; no es una conexion oficial con RENIEC.
# ------------------------------------------------------------
BASE_DNI_ARCHIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base_dni_sedapal.json")

# Datos iniciales: se escriben en JSON solamente cuando el archivo no existe.
DATOS_DNI_INICIALES = [{'dni': '60549429', 'nombres': 'Jhanmer', 'apellidos': 'Meza', 'fecha_emision': '15/03/2020', 'numero_verificador': '1'}, {'dni': '11111111', 'nombres': 'Ana', 'apellidos': 'Torres', 'fecha_emision': '10/05/2019', 'numero_verificador': '2'}, {'dni': '22222222', 'nombres': 'Carlos', 'apellidos': 'Ramirez', 'fecha_emision': '21/07/2021', 'numero_verificador': '3'}, {'dni': '33333333', 'nombres': 'Maria', 'apellidos': 'Flores', 'fecha_emision': '02/02/2018', 'numero_verificador': '4'}, {'dni': '44444444', 'nombres': 'Luis', 'apellidos': 'Mendoza', 'fecha_emision': '12/06/2022', 'numero_verificador': '5'}, {'dni': '55555555', 'nombres': 'Rosa', 'apellidos': 'Castillo', 'fecha_emision': '18/09/2020', 'numero_verificador': '6'}, {'dni': '66666666', 'nombres': 'Pedro', 'apellidos': 'Vargas', 'fecha_emision': '05/01/2017', 'numero_verificador': '7'}, {'dni': '77777777', 'nombres': 'Lucia', 'apellidos': 'Herrera', 'fecha_emision': '14/04/2021', 'numero_verificador': '8'}, {'dni': '88888888', 'nombres': 'Jose', 'apellidos': 'Rojas', 'fecha_emision': '23/08/2019', 'numero_verificador': '9'}, {'dni': '99999999', 'nombres': 'Carmen', 'apellidos': 'Diaz', 'fecha_emision': '30/11/2022', 'numero_verificador': '0'}, {'dni': '10101010', 'nombres': 'Miguel', 'apellidos': 'Soto', 'fecha_emision': '11/12/2018', 'numero_verificador': '1'}, {'dni': '12121212', 'nombres': 'Elena', 'apellidos': 'Cruz', 'fecha_emision': '09/02/2020', 'numero_verificador': '2'}, {'dni': '13131313', 'nombres': 'Jorge', 'apellidos': 'Ramos', 'fecha_emision': '17/05/2021', 'numero_verificador': '3'}, {'dni': '14141414', 'nombres': 'Patricia', 'apellidos': 'Leon', 'fecha_emision': '26/10/2019', 'numero_verificador': '4'}, {'dni': '15151515', 'nombres': 'Diego', 'apellidos': 'Silva', 'fecha_emision': '08/03/2022', 'numero_verificador': '5'}, {'dni': '16161616', 'nombres': 'Andrea', 'apellidos': 'Ruiz', 'fecha_emision': '19/07/2018', 'numero_verificador': '6'}, {'dni': '17171717', 'nombres': 'Marco', 'apellidos': 'Vega', 'fecha_emision': '04/04/2020', 'numero_verificador': '7'}, {'dni': '18181818', 'nombres': 'Sofia', 'apellidos': 'Castro', 'fecha_emision': '22/01/2021', 'numero_verificador': '8'}, {'dni': '19191919', 'nombres': 'Daniel', 'apellidos': 'Paredes', 'fecha_emision': '13/06/2019', 'numero_verificador': '9'}, {'dni': '20202020', 'nombres': 'Valeria', 'apellidos': 'Reyes', 'fecha_emision': '27/09/2022', 'numero_verificador': '0'}, {'dni': '21212121', 'nombres': 'Fernando', 'apellidos': 'Luna', 'fecha_emision': '06/02/2018', 'numero_verificador': '1'}, {'dni': '23232323', 'nombres': 'Gabriela', 'apellidos': 'Rios', 'fecha_emision': '16/08/2020', 'numero_verificador': '2'}, {'dni': '24242424', 'nombres': 'Alberto', 'apellidos': 'Salas', 'fecha_emision': '25/12/2021', 'numero_verificador': '3'}, {'dni': '25252525', 'nombres': 'Claudia', 'apellidos': 'Peña', 'fecha_emision': '07/05/2019', 'numero_verificador': '4'}, {'dni': '26262626', 'nombres': 'Ricardo', 'apellidos': 'Flores', 'fecha_emision': '20/10/2022', 'numero_verificador': '5'}, {'dni': '27272727', 'nombres': 'Monica', 'apellidos': 'Campos', 'fecha_emision': '03/03/2018', 'numero_verificador': '6'}, {'dni': '28282828', 'nombres': 'Eduardo', 'apellidos': 'Chavez', 'fecha_emision': '24/06/2020', 'numero_verificador': '7'}, {'dni': '29292929', 'nombres': 'Paola', 'apellidos': 'Medina', 'fecha_emision': '01/09/2021', 'numero_verificador': '8'}, {'dni': '30303030', 'nombres': 'Oscar', 'apellidos': 'Navarro', 'fecha_emision': '29/04/2019', 'numero_verificador': '9'}, {'dni': '31313131', 'nombres': 'Teresa', 'apellidos': 'Aguilar', 'fecha_emision': '12/12/2022', 'numero_verificador': '0'}]


def guardar_base_dni(datos):
    """Guarda la lista de registros DNI en un archivo JSON."""
    with open(BASE_DNI_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_base_dni():
    """Carga los DNI desde JSON; crea el archivo con datos de prueba si no existe."""
    if not os.path.exists(BASE_DNI_ARCHIVO):
        guardar_base_dni(DATOS_DNI_INICIALES)
        print("Se creo la base de datos local de DNI:", BASE_DNI_ARCHIVO)
        return DATOS_DNI_INICIALES.copy()

    try:
        with open(BASE_DNI_ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido principal del JSON debe ser una lista.")

        campos_obligatorios = [
            "dni", "nombres", "apellidos", "fecha_emision", "numero_verificador"
        ]

        for registro in datos:
            if not isinstance(registro, dict):
                raise ValueError("Cada registro del JSON debe ser un objeto.")
            for campo in campos_obligatorios:
                if campo not in registro:
                    raise ValueError("Falta el campo obligatorio: " + campo)

        return datos

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print("ERROR al leer la base de datos DNI:", error)
        print("Revise el archivo base_dni_sedapal.json antes de continuar.")
        return []