# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL v 0.1.1
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

#Funcion para validar el formato de la fecha ingresada

def validar_fecha(fecha):
    # Separamos la fecha usando "/"
    partes = fecha.split("/")

    # La fecha debe tener:
    # dia / mes / año
    if len(partes) != 3:
        return False

    dia = partes[0]
    mes = partes[1]
    año = partes[2]

    # Verificamos la cantidad de caracteres
    if len(dia) != 2:
        return False

    if len(mes) != 2:
        return False

    if len(año) != 4:
        return False

    # Verificamos que el día tenga solo números
    for caracter in dia:

        if caracter < "0" or caracter > "9":
            return False

    # Verificamos que el mes tenga solo números
    for caracter in mes:

        if caracter < "0" or caracter > "9":
            return False

    # Verificamos que el año tenga solo números
    for caracter in año:

        if caracter < "0" or caracter > "9":
            return False

    # Convertimos los datos a números
    dia = int(dia)
    mes = int(mes)
    año = int(año)

    # Validamos los rangos
    if dia < 1 or dia > 31:
        return False

    if mes < 1 or mes > 12:
        return False

    if año < 2026 or año > 2100:
        return False

    return True

def texto_valido(texto):
        texto_limpio = texto.strip()
    
        if texto_limpio == "":          # Si el usuario no escribió nada, no es válido
         return False
        
    # Definimos nuestra lista de caracteres aprobados
        permitidas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "
    
    # Revisamos cada letra igual que en tu ejemplo
        for letra in texto:
            if letra not in permitidas:
                return False  # Si encuentra un número o símbolo, frena y dice: "No es válido"
            
        return True  # Si el ciclo termina y todo estuvo bien, dice: "Sí es válido"

def validar_correo(email):
    
    email_limpio = email.strip().lower()        #quita espacios + minusculas
    caracteres_prohibidos = " ,()[]{}!¡¿?/*;:<>=#$"     # --- FILTRO DE CARACTERES PROHIBIDOS ---
    
    for caracter in email_limpio:
        if caracter in caracteres_prohibidos:
            return False # Si encuentra un carácter prohibido, el correo es inválido

    if "@" in email_limpio:
        partes = email_limpio.split("@")        # corta en 2 partes (usuario + @ + dominio) ["juan.perez", "gmail.com"]
        dominio = partes[1]                     # pedimos q guarde el 2do elemento [1]
        
        if "." in dominio:                      # el DOMINIO tenga un punto (para el .com, .net, etc.)
            return True
        
    return False

# ----------------------------------------------------------------------
# FUNCIÓN PARA VALIDAR TELÉFONOS (FIJOS Y CELULARES EN PERÚ)
# ----------------------------------------------------------------------
def validar_telefono(telefono):
    tel_limpio = telefono.strip()       # Quitamos espacios en blanco por si el usuario los puso
    
    # REGLA 1: Solo debe contener números
    for caracter in tel_limpio:
        if caracter not in "0123456789":
            return False
        
    longitud = len(tel_limpio)
    primer_digito = tel_limpio[0]
    
    if primer_digito == "9":            # REGLA 2: Si es un celular (Empieza con 9)
        if longitud == 9:
            return True
        else:
            return False # Celular incorrecto si no tiene 9 dígitos
            
    elif primer_digito in ["2", "3", "4", "5", "6", "7", "8"]:      # REGLA 3: Si es un teléfono fijo o rural (Empieza entre 2 y 8)
        if longitud == 6 or longitud == 7:                          # Acepta 7 dígitos (Lima/Callao) o 6 dígitos (Provincias)
            return True
        else:
            return False                                # Fijo incorrecto si no tiene 6 o 7 dígitos
            
    return False                            # Si empieza con 0, 1 o cualquier otro carácter, es inválido

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
    while nombre == "" or texto_valido(nombre) == False:
        print("El nombre no puede estar vacío o estar digitado de forma incorrecta.")
        nombre = input("Ingrese el nombre completo: ")
    
    apellidos = input("Ingrese sus apellidos completos: ")
    
        # Verificamos que no esté vacío
    while apellidos == "" or texto_valido(apellidos) == False:
            print("El apellido no puede estar vacío o estar digitado de forma incorrecta.")
            apellidos = input("Ingrese los apellidos completos: ")

    # --- NUEVOS CAMPOS DE CONTACTO ---
    # Pedimos el número de teléfono
    nro_telefono = input("Ingrese el número de teléfono/celular: ")

    while nro_telefono == "" or validar_telefono(nro_telefono) == False:
            print("Error: El número ingresado no es un celular válido de 9 dígitos (inicia con 9) ")
            print("       ni un teléfono fijo válido de 6 o 7 dígitos (inicia del 2 al 8).")
            nro_telefono = input("Ingrese el número de teléfono nuevamente: ")

    # Pedimos el correo electrónico
    correo = input("Ingrese el correo electrónico del ciudadano: ")

    # Verificamos que no esté vacío
    while correo == "" or validar_correo(correo) == False:
        print("El correo electrónico no puede estar vacío o estar digitado de forma incorrecta.")
        correo = input("Ingrese el correo electrónico nuevamente: ")


    # ----------------------------------------
    # TIPO DE TRÁMITE
    # ----------------------------------------

    print("\nSeleccione el tipo de trámite:")
    print("1. Queja y Reclamos")
    print("2. Solicitud")
    print("3. Consulta")

    opcion = input("Ingrese una opción: ")
#Se modifico Las opciones de tramites
    while opcion != "1" and opcion != "2" and opcion != "3" :
        print("Opción incorrecta.")
        opcion = input("Ingrese una opción: ")

    if opcion == "1":
        tipo = "Quejas y Reclamos"
    elif opcion == "2":
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
    # Mientras la fecha sea incorrecta, la volvemos a pedir
    while validar_fecha(fecha) == False:

        print("Fecha incorrecta.")
        print("Debe utilizar el formato DD/MM/AAAA.")

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
        apellidos,
        nro_telefono,
        correo,
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
            print("Ciudadano:", expediente[2] +" "+ expediente[3])
            print("Telefono/Celular:", expediente[4])
            print("Correo electrónico:", expediente[5])
            print("Tipo:", expediente[6])
            print("Descripción:", expediente[7])
            print("Sede:", expediente[8])
            print("Fecha:", expediente[9])
            print("Estado:", expediente[10])

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
            print("Ciudadano:", expediente[2] +" "+ expediente[3])
            print("Telefono/Celular:", expediente[4])
            print("Correo electrónico:", expediente[5])
            print("Tipo:", expediente[6])
            print("Descripción:", expediente[7])
            print("Sede:", expediente[8])
            print("Fecha:", expediente[9])
            print("Estado:", expediente[10])
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
            print("Código:", expediente[0])
            print("Estado actual:", expediente[10])

            print("\nSeleccione el nuevo estado:")
            print("1. Pendiente")
            print("2. En proceso")
            print("3. Atendido")

            opcion = input("Ingrese una opción: ")

            while opcion != "1" and opcion != "2" and opcion != "3":
                print("Opción incorrecta.")
                opcion = input("Ingrese una opción: ")

            if opcion == "1":
                expediente[10] = "Pendiente"

            elif opcion == "2":
                expediente[10] = "En proceso"

            else:
                expediente[10] = "Atendido"

            print("\nEstado actualizado correctamente.")
            print("Código:", expediente[0])
            print("Nuevo estado:", expediente[10])

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
            archivo.write("Ciudadano: " + expediente[2] +" "+ expediente[3] + "\n")
            archivo.write("Telefono/Celular:" + expediente[4] + "\n")
            archivo.write("Correo electrónico:" + expediente[5] + "\n")
            archivo.write("Tipo: " + expediente[6] + "\n")
            archivo.write("Descripción: " + expediente[7] + "\n")
            archivo.write("Sede: " + expediente[8] + "\n")
            archivo.write("Fecha: " + expediente[9] + "\n")
            archivo.write("Estado: " + expediente[10] + "\n")

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