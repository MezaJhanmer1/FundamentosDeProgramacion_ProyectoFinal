# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL
# Proyecto educativo: listas, funciones, ciclos y archivos
#Version de proyecto Ver 1.2
# ============================================================

# ------------------------------------------------------------
# LISTA PRINCIPAL DE EXPEDIENTES
# Cada expediente será una lista con sus datos.
# ------------------------------------------------------------
expedientes = []

# ------------------------------------------------------------
# LISTAS PARA SIMULAR UNA CONSULTA A RENIEC
# Estos son datos de prueba, no una consulta oficial.
# ------------------------------------------------------------
reniec_dni = [
    "60549429", "11111111", "22222222", "33333333", "44444444",
    "55555555", "66666666", "77777777", "88888888", "99999999",
    "10101010", "12121212", "13131313", "14141414", "15151515",
    "16161616", "17171717", "18181818", "19191919", "20202020",
    "21212121", "23232323", "24242424", "25252525", "26262626",
    "27272727", "28282828", "29292929", "30303030", "31313131"
]

reniec_nombres = [
    "Jhanmer", "Ana", "Carlos", "Maria", "Luis", "Rosa", "Pedro",
    "Lucia", "Jose", "Carmen", "Miguel", "Elena", "Jorge", "Patricia",
    "Diego", "Andrea", "Marco", "Sofia", "Daniel", "Valeria", "Fernando",
    "Gabriela", "Alberto", "Claudia", "Ricardo", "Monica", "Eduardo",
    "Paola", "Oscar", "Teresa"
]

reniec_apellidos = [
    "Meza", "Torres", "Ramirez", "Flores", "Mendoza", "Castillo", "Vargas",
    "Herrera", "Rojas", "Diaz", "Soto", "Cruz", "Ramos", "Leon", "Silva",
    "Ruiz", "Vega", "Castro", "Paredes", "Reyes", "Luna", "Rios", "Salas",
    "Peña", "Flores", "Campos", "Chavez", "Medina", "Navarro", "Aguilar"
]

# ------------------------------------------------------------
# LISTAS PARA LOS USUARIOS DEL SISTEMA (LISTAS PARALELAS)
# Perfil 1 = Persona natural
# Perfil 2 = Administrador
# Las dos cuentas iniciales son de demostración.
# ------------------------------------------------------------
usuarios_dni = ["60549429", "12345678"]
usuarios_nombres = ["Jhanmer", "Carlos"]
usuarios_apellidos = ["Meza", "Ramirez"]
usuarios_telefono = ["", ""]
usuarios_correo = ["", ""]
usuarios_claves = ["admin123", "admin456"]
usuarios_perfiles = [2, 2]

# ============================================================
# FUNCION PARA VALIDAR TEXTO CON LETRAS Y ESPACIOS
# ============================================================
def texto_valido(texto):
    texto_limpio = texto.strip()

    if texto_limpio == "":
        return False

    permitidas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "

    for letra in texto_limpio:
        if letra not in permitidas:
            return False

    return True


# ============================================================
# FUNCION PARA VALIDAR EL DNI
# ============================================================
def validar_dni(dni):
    if len(dni) != 8:
        return False

    for caracter in dni:
        if caracter < "0" or caracter > "9":
            return False

    return True


# ============================================================
# FUNCION PARA VALIDAR LA FECHA DD/MM/AAAA
# ============================================================
def validar_fecha(fecha):
    partes = fecha.split("/")

    if len(partes) != 3:
        return False

    dia_texto = partes[0]
    mes_texto = partes[1]
    anio_texto = partes[2]

    if len(dia_texto) != 2 or len(mes_texto) != 2 or len(anio_texto) != 4:
        return False

    for caracter in dia_texto:
        if caracter < "0" or caracter > "9":
            return False

    for caracter in mes_texto:
        if caracter < "0" or caracter > "9":
            return False

    for caracter in anio_texto:
        if caracter < "0" or caracter > "9":
            return False

    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)

    if anio < 2026 or anio > 2100:
        return False

    if mes < 1 or mes > 12:
        return False

    # Comprobamos cuantos dias tiene el mes.
    if mes == 4 or mes == 6 or mes == 9 or mes == 11:
        maximo_dias = 30
    elif mes == 2:
        # Regla sencilla para reconocer años bisiestos.
        if anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0):
            maximo_dias = 29
        else:
            maximo_dias = 28
    else:
        maximo_dias = 31

    if dia < 1 or dia > maximo_dias:
        return False

    return True


# ============================================================
# FUNCION PARA VALIDAR TELEFONO
# ============================================================
def validar_telefono(telefono):
    telefono = telefono.strip()

    if len(telefono) == 0:
        return False

    for caracter in telefono:
        if caracter < "0" or caracter > "9":
            return False

    longitud = len(telefono)
    primer_digito = telefono[0]

    if primer_digito == "9" and longitud == 9:
        return True

    if primer_digito in ["2", "3", "4", "5", "6", "7", "8"]:
        if longitud == 6 or longitud == 7:
            return True

    return False


# ============================================================
# FUNCION PARA VALIDAR CORREO
# ============================================================
def validar_correo(correo):
    correo = correo.strip()

    if correo.count("@") != 1:
        return False

    partes = correo.split("@")
    usuario = partes[0]
    dominio = partes[1]

    if usuario == "" or dominio == "":
        return False

    if "." not in dominio:
        return False

    if dominio.startswith(".") or dominio.endswith("."):
        return False

    if " " in correo:
        return False

    return True


# ============================================================
# FUNCION PARA SIMULAR LA CONSULTA A RENIEC
# Devuelve nombre y apellido si encuentra el DNI.
# ============================================================
def consultar_reniec(dni):
    for i in range(len(reniec_dni)):
        if reniec_dni[i] == dni:
            return reniec_nombres[i], reniec_apellidos[i]

    return "", ""


# ============================================================
# FUNCION PARA GENERAR CODIGO DE EXPEDIENTE
# ============================================================
def generar_codigo():
    numero = len(expedientes) + 1

    if numero < 10:
        codigo = "SED-000" + str(numero)
    elif numero < 100:
        codigo = "SED-00" + str(numero)
    elif numero < 1000:
        codigo = "SED-0" + str(numero)
    else:
        codigo = "SED-" + str(numero)

    return codigo


# ============================================================
# FUNCION PARA REGISTRAR UN USUARIO NUEVO
# Los usuarios nuevos siempre son personas naturales.
# ============================================================
def registrar_usuario():
    print("\n========================================")
    print("          CREAR NUEVO USUARIO")
    print("========================================")

    dni = input("Ingrese su DNI: ").strip()

    while validar_dni(dni) == False:
        print("El DNI debe tener exactamente 8 numeros.")
        dni = input("Ingrese su DNI nuevamente: ").strip()

    # Evitamos crear dos cuentas con el mismo DNI.
    for i in range(len(usuarios_dni)):
        if usuarios_dni[i] == dni:
            print("Este DNI ya tiene una cuenta en el sistema.")
            return

    # Buscamos el DNI en nuestra lista simulada.
    nombre, apellidos = consultar_reniec(dni)

    if nombre == "":
        print("DNI no encontrado en la lista simulada.")
        print("No se puede completar el registro.")
        return

    print("Nombre encontrado:", nombre)
    print("Apellidos encontrados:", apellidos)

    telefono = input("Ingrese su telefono/celular: ").strip()
    while validar_telefono(telefono) == False:
        print("Telefono incorrecto. Revise la cantidad de digitos.")
        telefono = input("Ingrese su telefono/celular nuevamente: ").strip()

    correo = input("Ingrese su correo: ").strip()
    while validar_correo(correo) == False:
        print("Correo incorrecto.")
        correo = input("Ingrese su correo nuevamente: ").strip()

    clave = input("Cree su contraseña: ")
    while clave == "":
        print("La contraseña no puede estar vacia.")
        clave = input("Cree su contraseña: ")

    # Guardamos los datos en la misma posicion de cada lista.
    usuarios_dni.append(dni)
    usuarios_nombres.append(nombre)
    usuarios_apellidos.append(apellidos)
    usuarios_telefono.append(telefono)
    usuarios_correo.append(correo)
    usuarios_claves.append(clave)
    usuarios_perfiles.append(1)

    print("\nUsuario registrado correctamente.")
    print("Tu perfil es: Persona natural.")
    print("Ya puedes iniciar sesion.")


# ============================================================
# FUNCION PARA INICIAR SESION
# Devuelve la posicion del usuario o -1 si falla.
# ============================================================
def iniciar_sesion():
    print("\n========================================")
    print("              INICIAR SESION")
    print("========================================")

    dni = input("Ingrese su usuario (DNI): ").strip()
    clave = input("Ingrese su contraseña: ")

    for i in range(len(usuarios_dni)):
        if usuarios_dni[i] == dni:
            if usuarios_claves[i] == clave:
                print("\nBienvenido:", usuarios_nombres[i], usuarios_apellidos[i])
                if usuarios_perfiles[i] == 2:
                    print("Perfil: Administrador")
                else:
                    print("Perfil: Persona natural")
                return i
            else:
                print("Contraseña incorrecta.")
                return -1

    print("Usuario no registrado.")
    return -1


# ============================================================
# FUNCION PARA REGISTRAR UN EXPEDIENTE
# El DNI completa nombre y apellidos desde la lista simulada.
# ============================================================
def registrar_expediente(posicion_usuario):
    print("\n========================================")
    print("          REGISTRO DE EXPEDIENTE")
    print("========================================")

    codigo = generar_codigo()
    print("Codigo del expediente:", codigo)

    dni = input("Ingrese el DNI del ciudadano: ").strip()
    while validar_dni(dni) == False:
        print("Error: el DNI debe tener exactamente 8 numeros.")
        dni = input("Ingrese nuevamente el DNI: ").strip()

    # La persona natural solo puede registrar con su propio DNI.
    if usuarios_perfiles[posicion_usuario] == 1 and dni != usuarios_dni[posicion_usuario]:
        print("Por seguridad, solo puedes registrar expedientes con tu propio DNI.")
        return

    nombre, apellidos = consultar_reniec(dni)

    while nombre == "":
        print("DNI no encontrado en la lista simulada.")
        dni = input("Ingrese otro DNI: ").strip()

        while validar_dni(dni) == False:
            print("Error: el DNI debe tener exactamente 8 numeros.")
            dni = input("Ingrese nuevamente el DNI: ").strip()

        if usuarios_perfiles[posicion_usuario] == 1 and dni != usuarios_dni[posicion_usuario]:
            print("Solo puedes registrar expedientes con tu propio DNI.")
            return

        nombre, apellidos = consultar_reniec(dni)

    print("Nombre encontrado:", nombre)
    print("Apellidos encontrados:", apellidos)

    telefono = input("Ingrese el telefono/celular de contacto: ").strip()
    while validar_telefono(telefono) == False:
        print("Telefono incorrecto. Ingrese un numero valido.")
        telefono = input("Ingrese el telefono/celular nuevamente: ").strip()

    correo = input("Ingrese el correo electronico de contacto: ").strip()
    while validar_correo(correo) == False:
        print("Correo electronico incorrecto.")
        correo = input("Ingrese el correo nuevamente: ").strip()

    print("\nSeleccione el tipo de tramite:")
    print("1. Queja y reclamo")
    print("2. Solicitud")
    print("3. Consulta")
    opcion = input("Ingrese una opcion: ").strip()

    while opcion != "1" and opcion != "2" and opcion != "3":
        print("Opcion incorrecta.")
        opcion = input("Ingrese una opcion: ").strip()

    if opcion == "1":
        tipo = "Queja y reclamo"
    elif opcion == "2":
        tipo = "Solicitud"
    else:
        tipo = "Consulta"

    descripcion = input("Ingrese la descripcion del tramite: ").strip()
    while descripcion == "":
        print("La descripcion no puede estar vacia.")
        descripcion = input("Ingrese la descripcion del tramite: ").strip()

    fecha = input("Ingrese la fecha (DD/MM/AAAA): ").strip()
    while validar_fecha(fecha) == False:
        print("Fecha incorrecta. Use el formato DD/MM/AAAA y una fecha valida.")
        fecha = input("Ingrese la fecha (DD/MM/AAAA): ").strip()

    print("\nSeleccione la prioridad:")
    print("1. Alta")
    print("2. Media")
    print("3. Baja")

    # Las personas naturales no eligen prioridad alta por su cuenta.
    if usuarios_perfiles[posicion_usuario] == 1:
        prioridad = "Media"
        print("Tu expediente se registrara con prioridad Media.")
    else:
        opcion_prioridad = input("Ingrese una opcion: ").strip()
        while opcion_prioridad != "1" and opcion_prioridad != "2" and opcion_prioridad != "3":
            print("Opcion incorrecta.")
            opcion_prioridad = input("Ingrese una opcion: ").strip()

        if opcion_prioridad == "1":
            prioridad = "Alta"
        elif opcion_prioridad == "2":
            prioridad = "Media"
        else:
            prioridad = "Baja"

    estado = "Pendiente"

    # Cada expediente es una lista. Los datos mantienen sus posiciones.
    expediente = [
        codigo, dni, nombre, apellidos, telefono, correo,
        tipo, descripcion, "SJL", fecha, estado, prioridad
    ]

    expedientes.append(expediente)

    print("\nExpediente registrado correctamente.")
    print("Codigo:", codigo)
    print("Prioridad:", prioridad)
    print("Estado:", estado)


# ============================================================
# FUNCION PARA MOSTRAR EXPEDIENTES
# Una persona natural solo ve los expedientes de su DNI.
# ============================================================
def mostrar_expedientes(posicion_usuario):
    print("\n========================================")
    print("             EXPEDIENTES")
    print("========================================")

    encontrados = 0

    for expediente in expedientes:
        if usuarios_perfiles[posicion_usuario] == 2 or expediente[1] == usuarios_dni[posicion_usuario]:
            print("----------------------------------------")
            print("Codigo:", expediente[0])
            print("DNI:", expediente[1])
            print("Ciudadano:", expediente[2], expediente[3])
            print("Telefono:", expediente[4])
            print("Correo:", expediente[5])
            print("Tipo:", expediente[6])
            print("Descripcion:", expediente[7])
            print("Sede:", expediente[8])
            print("Fecha:", expediente[9])
            print("Estado:", expediente[10])
            print("Prioridad:", expediente[11])
            encontrados = encontrados + 1

    if encontrados == 0:
        print("No hay expedientes para mostrar.")


# ============================================================
# FUNCION PARA BUSCAR EXPEDIENTE
# ============================================================
def buscar_expediente(posicion_usuario):
    codigo_buscar = input("Ingrese el codigo del expediente: ").strip()
    encontrado = False

    for expediente in expedientes:
        if expediente[0] == codigo_buscar:
            # La persona natural solo puede consultar sus propios expedientes.
            if usuarios_perfiles[posicion_usuario] == 1 and expediente[1] != usuarios_dni[posicion_usuario]:
                continue

            print("\nExpediente encontrado:")
            print("Codigo:", expediente[0])
            print("DNI:", expediente[1])
            print("Ciudadano:", expediente[2], expediente[3])
            print("Tipo:", expediente[6])
            print("Descripcion:", expediente[7])
            print("Fecha:", expediente[9])
            print("Estado:", expediente[10])
            print("Prioridad:", expediente[11])
            encontrado = True

    if encontrado == False:
        print("No se encontro el expediente o no tienes permiso para verlo.")


# ============================================================
# FUNCION PARA ACTUALIZAR ESTADO (SOLO ADMINISTRADOR)
# ============================================================
def actualizar_estado():
    codigo_buscar = input("Ingrese el codigo del expediente: ").strip()
    encontrado = False

    for expediente in expedientes:
        if expediente[0] == codigo_buscar:
            encontrado = True
            print("Estado actual:", expediente[10])
            print("1. Pendiente")
            print("2. En proceso")
            print("3. Atendido")
            opcion = input("Seleccione el nuevo estado: ").strip()

            while opcion != "1" and opcion != "2" and opcion != "3":
                print("Opcion incorrecta.")
                opcion = input("Seleccione el nuevo estado: ").strip()

            if opcion == "1":
                expediente[10] = "Pendiente"
            elif opcion == "2":
                expediente[10] = "En proceso"
            else:
                expediente[10] = "Atendido"

            print("Estado actualizado:", expediente[10])

    if encontrado == False:
        print("No se encontro el expediente.")


# ============================================================
# FUNCION PARA ORDENAR POR PRIORIDAD CON CICLOS FOR
# Alta primero, luego Media y finalmente Baja.
# ============================================================
def ordenar_expedientes():
    if len(expedientes) == 0:
        print("No existen expedientes para ordenar.")
        return

    # Asignamos un numero a cada prioridad para compararlas.
    for i in range(len(expedientes)):
        for j in range(i + 1, len(expedientes)):
            prioridad_i = expedientes[i][11]
            prioridad_j = expedientes[j][11]

            if prioridad_i == "Alta":
                numero_i = 1
            elif prioridad_i == "Media":
                numero_i = 2
            else:
                numero_i = 3

            if prioridad_j == "Alta":
                numero_j = 1
            elif prioridad_j == "Media":
                numero_j = 2
            else:
                numero_j = 3

            if numero_i > numero_j:
                temporal = expedientes[i]
                expedientes[i] = expedientes[j]
                expedientes[j] = temporal

    print("Expedientes ordenados por prioridad.")
    print("Orden: Alta, Media y Baja.")


# ============================================================
# FUNCION PARA GUARDAR EXPEDIENTES EN UN ARCHIVO DE TEXTO
# ============================================================
def guardar_archivo():
    archivo = open("expedientes_sedapal.txt", "w", encoding="utf-8")

    for expediente in expedientes:
        archivo.write("========================================\n")
        archivo.write("Codigo: " + expediente[0] + "\n")
        archivo.write("DNI: " + expediente[1] + "\n")
        archivo.write("Ciudadano: " + expediente[2] + " " + expediente[3] + "\n")
        archivo.write("Telefono: " + expediente[4] + "\n")
        archivo.write("Correo: " + expediente[5] + "\n")
        archivo.write("Tipo: " + expediente[6] + "\n")
        archivo.write("Descripcion: " + expediente[7] + "\n")
        archivo.write("Sede: " + expediente[8] + "\n")
        archivo.write("Fecha: " + expediente[9] + "\n")
        archivo.write("Estado: " + expediente[10] + "\n")
        archivo.write("Prioridad: " + expediente[11] + "\n")

    archivo.close()
    print("Expedientes guardados en expedientes_sedapal.txt")


# ============================================================
# MENU PARA PERSONA NATURAL
# ============================================================
def menu_persona_natural(posicion_usuario):
    opcion = ""

    while opcion != "4":
        print("\n========================================")
        print("       MENU - PERSONA NATURAL")
        print("========================================")
        print("1. Registrar/enviar documento")
        print("2. Ver mis expedientes")
        print("3. Buscar mi expediente por codigo")
        print("4. Cerrar sesion")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            registrar_expediente(posicion_usuario)
        elif opcion == "2":
            mostrar_expedientes(posicion_usuario)
        elif opcion == "3":
            buscar_expediente(posicion_usuario)
        elif opcion == "4":
            print("Sesion cerrada.")
        else:
            print("Opcion incorrecta.")


# ============================================================
# MENU PARA ADMINISTRADOR
# ============================================================
def menu_administrador(posicion_usuario):
    opcion = ""

    while opcion != "7":
        print("\n========================================")
        print("         MENU - ADMINISTRADOR")
        print("========================================")
        print("1. Registrar expediente")
        print("2. Mostrar todos los expedientes")
        print("3. Buscar expediente")
        print("4. Actualizar estado")
        print("5. Ordenar por prioridad")
        print("6. Guardar expedientes en archivo")
        print("7. Cerrar sesion")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            registrar_expediente(posicion_usuario)
        elif opcion == "2":
            mostrar_expedientes(posicion_usuario)
        elif opcion == "3":
            buscar_expediente(posicion_usuario)
        elif opcion == "4":
            actualizar_estado()
        elif opcion == "5":
            ordenar_expedientes()
        elif opcion == "6":
            guardar_archivo()
        elif opcion == "7":
            print("Sesion cerrada.")
        else:
            print("Opcion incorrecta.")


# ============================================================
# MENU INICIAL DEL SISTEMA
# ============================================================
def menu_inicial():
    opcion = ""

    while opcion != "3":
        print("\n========================================")
        print("    SEDAPAL - MESA DE PARTES DIGITAL")
        print("       SEDE SAN JUAN DE LURIGANCHO")
        print("========================================")
        print("1. Iniciar sesion")
        print("2. Crear nuevo usuario")
        print("3. Salir")

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            posicion = iniciar_sesion()

            if posicion != -1:
                if usuarios_perfiles[posicion] == 2:
                    menu_administrador(posicion)
                else:
                    menu_persona_natural(posicion)

        elif opcion == "2":
            registrar_usuario()

        elif opcion == "3":
            print("Gracias por utilizar el sistema.")

        else:
            print("Opcion incorrecta. Intente nuevamente.")


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================
menu_inicial()
