# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL
# ============================================================
# Este programa permite registrar y consultar expedientes
# de los usuarios de SEDAPAL - San Juan de Lurigancho.
#
# ============================================================


# ------------------------------------------------------------
# LISTA PRINCIPAL
# ------------------------------------------------------------
# Esta lista almacenará todos los expedientes registrados.
# Por ahora no utilizamos una base de datos.

expedientes = []


# ------------------------------------------------------------
# FUNCIÓN PARA VALIDAR EL DNI
# ------------------------------------------------------------
def validar_dni(dni):

    # Verificamos que el DNI tenga exactamente 8 caracteres
    if len(dni) != 8:
        return False

    # Verificamos que todos los caracteres sean números
    for caracter in dni:
        if caracter < "0" or caracter > "9":
            return False

    return True


# ------------------------------------------------------------
# FUNCIÓN PARA GENERAR EL CÓDIGO DEL EXPEDIENTE
# ------------------------------------------------------------
def generar_codigo():

    # La cantidad de expedientes nos sirve para generar
    # un código diferente para cada registro.

    numero = len(expedientes) + 1

    if numero < 10:
        codigo = "SED-000" + str(numero)
    elif numero < 100:
        codigo = "SED-00" + str(numero)
    else:
        codigo = "SED-0" + str(numero)

    return codigo


# ------------------------------------------------------------
# FUNCIÓN PARA REGISTRAR UN EXPEDIENTE
# ------------------------------------------------------------
def registrar_expediente():

    print("\n==========================================")
    print("       REGISTRO DE EXPEDIENTE")
    print("==========================================")

    # Generamos automáticamente el código
    codigo = generar_codigo()

    print("Código del expediente:", codigo)

    # ----------------------------------------
    # INGRESO DEL DNI
    # ----------------------------------------

    dni = input("Ingrese el DNI del ciudadano: ")

    # Repetimos mientras el DNI sea incorrecto
    while validar_dni(dni) == False:

        print("Error: el DNI debe tener exactamente 8 números.")
        dni = input("Ingrese nuevamente el DNI: ")

    # ----------------------------------------
    # INGRESO DEL NOMBRE
    # ----------------------------------------

    nombre = input("Ingrese el nombre completo: ")

    # Verificamos que no esté vacío
    while nombre == "":
        print("El nombre no puede estar vacío.")
        nombre = input("Ingrese el nombre completo: ")

    # ----------------------------------------
    # TIPO DE TRÁMITE
    # ----------------------------------------

    print("\nSeleccione el tipo de trámite:")
    print("1. Reclamo")
    print("2. Queja")
    print("3. Solicitud")
    print("4. Consulta")

    opcion = input("Ingrese una opción: ")

    while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4":
        print("Opción incorrecta.")
        opcion = input("Ingrese una opción: ")

    if opcion == "1":
        tipo = "Reclamo"
    elif opcion == "2":
        tipo = "Queja"
    elif opcion == "3":
        tipo = "Solicitud"
    else:
        tipo = "Consulta"

    # ----------------------------------------
    # DESCRIPCIÓN
    # ----------------------------------------

    descripcion = input("Ingrese la descripción del trámite: ")

    while descripcion == "":
        print("La descripción no puede estar vacía.")
        descripcion = input("Ingrese la descripción del trámite: ")

    # ----------------------------------------
    # FECHA
    # ----------------------------------------

    fecha = input("Ingrese la fecha (DD/MM/AAAA): ")

    # ----------------------------------------
    # ESTADO INICIAL
    # ----------------------------------------

    estado = "Pendiente"

    # ----------------------------------------
    # CREACIÓN DEL EXPEDIENTE
    # ----------------------------------------
    # Utilizamos una lista para guardar los datos
    # de un solo expediente.

    expediente = [
        codigo,
        dni,
        nombre,
        tipo,
        descripcion,
        "SJL",
        fecha,
        estado
    ]

    # Agregamos el expediente a la lista principal
    expedientes.append(expediente)

    print("\n==========================================")
    print("Expediente registrado correctamente.")
    print("Código:", codigo)
    print("Estado:", estado)
    print("==========================================")


# ------------------------------------------------------------
# FUNCIÓN PARA MOSTRAR TODOS LOS EXPEDIENTES
# ------------------------------------------------------------
def mostrar_expedientes():

    print("\n==========================================")
    print("          LISTA DE EXPEDIENTES")
    print("==========================================")

    # Verificamos si la lista está vacía
    if len(expedientes) == 0:

        print("No existen expedientes registrados.")

    else:

        # Recorremos todos los expedientes
        for expediente in expedientes:

            print("------------------------------------------")
            print("Código:", expediente[0])
            print("DNI:", expediente[1])
            print("Ciudadano:", expediente[2])
            print("Tipo:", expediente[3])
            print("Descripción:", expediente[4])
            print("Sede:", expediente[5])
            print("Fecha:", expediente[6])
            print("Estado:", expediente[7])

        print("------------------------------------------")


# ------------------------------------------------------------
# FUNCIÓN PARA BUSCAR UN EXPEDIENTE
# ------------------------------------------------------------
def buscar_expediente():

    print("\n==========================================")
    print("        BUSCAR EXPEDIENTE")
    print("==========================================")

    codigo_buscar = input("Ingrese el código del expediente: ")

    encontrado = False

    # Recorremos la lista buscando el código
    for expediente in expedientes:

        if expediente[0] == codigo_buscar:

            print("\nExpediente encontrado:")
            print("------------------------------------------")
            print("Código:", expediente[0])
            print("DNI:", expediente[1])
            print("Ciudadano:", expediente[2])
            print("Tipo:", expediente[3])
            print("Descripción:", expediente[4])
            print("Sede:", expediente[5])
            print("Fecha:", expediente[6])
            print("Estado:", expediente[7])
            print("------------------------------------------")

            encontrado = True

    # Si después de recorrer la lista no encontramos
    # el expediente, mostramos un mensaje.
    if encontrado == False:
        print("No se encontró el expediente.")


# ------------------------------------------------------------
# FUNCIÓN PARA ACTUALIZAR EL ESTADO
# ------------------------------------------------------------
def actualizar_estado():

    print("\n==========================================")
    print("       ACTUALIZAR ESTADO")
    print("==========================================")

    codigo_buscar = input("Ingrese el código del expediente: ")

    encontrado = False

    # Buscamos el expediente
    for expediente in expedientes:

        if expediente[0] == codigo_buscar:

            encontrado = True

            print("\nExpediente encontrado.")
            print("Estado actual:", expediente[7])

            print("\nSeleccione el nuevo estado:")
            print("1. Pendiente")
            print("2. En proceso")
            print("3. Atendido")

            opcion = input("Ingrese una opción: ")

            while opcion != "1" and opcion != "2" and opcion != "3":
                print("Opción incorrecta.")
                opcion = input("Ingrese una opción: ")

            if opcion == "1":
                expediente[7] = "Pendiente"

            elif opcion == "2":
                expediente[7] = "En proceso"

            else:
                expediente[7] = "Atendido"

            print("\nEstado actualizado correctamente.")
            print("Nuevo estado:", expediente[7])

    if encontrado == False:
        print("No se encontró el expediente.")


# ------------------------------------------------------------
# FUNCIÓN PARA ORDENAR LOS EXPEDIENTES
# ------------------------------------------------------------
def ordenar_expedientes():

    print("\n==========================================")
    print("       ORDENAR EXPEDIENTES")
    print("==========================================")

    if len(expedientes) == 0:

        print("No existen expedientes para ordenar.")

    else:

        # Utilizamos el método de ordenamiento de Python
        # para ordenar los códigos de menor a mayor.

        expedientes.sort()

        print("Los expedientes fueron ordenados correctamente.")

        mostrar_expedientes()


# ------------------------------------------------------------
# FUNCIÓN PARA GUARDAR LOS EXPEDIENTES EN UN ARCHIVO
# ------------------------------------------------------------
def guardar_archivo():

    print("\n==========================================")
    print("       GUARDAR EXPEDIENTES")
    print("==========================================")

    # Verificamos que existan expedientes
    if len(expedientes) == 0:

        print("No existen expedientes para guardar.")

    else:

        # Abrimos un archivo de texto.
        # La letra "w" significa escribir.

        archivo = open("expedientes_sedapal.txt", "w")

        # Recorremos todos los expedientes
        for expediente in expedientes:

            archivo.write("====================================\n")
            archivo.write("Código: " + expediente[0] + "\n")
            archivo.write("DNI: " + expediente[1] + "\n")
            archivo.write("Ciudadano: " + expediente[2] + "\n")
            archivo.write("Tipo: " + expediente[3] + "\n")
            archivo.write("Descripción: " + expediente[4] + "\n")
            archivo.write("Sede: " + expediente[5] + "\n")
            archivo.write("Fecha: " + expediente[6] + "\n")
            archivo.write("Estado: " + expediente[7] + "\n")

        # Cerramos el archivo
        archivo.close()

        print("Los expedientes fueron guardados correctamente.")
        print("Archivo: expedientes_sedapal.txt")


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL
# ------------------------------------------------------------
def menu():

    opcion = ""

    # El menú se repetirá mientras el usuario
    # no seleccione la opción de salir.

    while opcion != "7":

        print("\n")
        print("==========================================")
        print("      SEDAPAL - MESA DE PARTES DIGITAL")
        print("           SEDE SAN JUAN DE LURIGANCHO")
        print("==========================================")
        print("1. Registrar expediente")
        print("2. Mostrar expedientes")
        print("3. Buscar expediente")
        print("4. Actualizar estado")
        print("5. Ordenar expedientes")
        print("6. Guardar expedientes en archivo")
        print("7. Salir")
        print("==========================================")

        opcion = input("Seleccione una opción: ")

        # ----------------------------------------
        # OPCIÓN 1
        # ----------------------------------------

        if opcion == "1":

            registrar_expediente()

        # ----------------------------------------
        # OPCIÓN 2
        # ----------------------------------------

        elif opcion == "2":

            mostrar_expedientes()

        # ----------------------------------------
        # OPCIÓN 3
        # ----------------------------------------

        elif opcion == "3":

            buscar_expediente()

        # ----------------------------------------
        # OPCIÓN 4
        # ----------------------------------------

        elif opcion == "4":

            actualizar_estado()

        # ----------------------------------------
        # OPCIÓN 5
        # ----------------------------------------

        elif opcion == "5":

            ordenar_expedientes()

        # ----------------------------------------
        # OPCIÓN 6
        # ----------------------------------------

        elif opcion == "6":

            guardar_archivo()

        # ----------------------------------------
        # OPCIÓN 7
        # ----------------------------------------

        elif opcion == "7":

            print("\nGracias por utilizar el sistema.")
            print("SEDAPAL - Mesa de Partes Digital")

        # ----------------------------------------
        # OPCIÓN INCORRECTA
        # ----------------------------------------

        else:

            print("\nOpción incorrecta. Intente nuevamente.")


# ------------------------------------------------------------
# INICIO DEL PROGRAMA
# ------------------------------------------------------------

menu()