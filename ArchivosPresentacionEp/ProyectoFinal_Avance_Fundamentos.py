from builtins import print
import json
import os

# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL v 0.1.5
# ============================================================
# Esta version incorpora JSON para DNI simulados y expedientes.
# No existe conexion oficial con RENIEC.
# ============================================================

# ------------------------------------------------------------
# ARCHIVO JSON PARA GUARDAR LOS EXPEDIENTES
# Es independiente del JSON de DNI.
# ------------------------------------------------------------
EXPEDIENTES_ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SEDAPAL_expedientes.json"
)


def cargar_expedientes():
    """Carga los expedientes guardados; si no existe el archivo, inicia vacio."""
    if not os.path.exists(EXPEDIENTES_ARCHIVO):
        return []

    try:
        with open(EXPEDIENTES_ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido principal debe ser una lista.")

        for expediente in datos:
            if not isinstance(expediente, list) or len(expediente) != 12:
                raise ValueError("Cada expediente debe tener exactamente 12 campos.")
            if not all(isinstance(campo, str) for campo in expediente):
                raise ValueError("Todos los campos del expediente deben ser texto.")

        return datos

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print("ERROR al cargar SEDAPAL_expedientes.json:", error)
        print("No se cargaron expedientes. Revise el archivo antes de continuar.")
        return []


def guardar_expedientes_json():
    """Guarda todos los expedientes en el archivo JSON."""
    with open(EXPEDIENTES_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(expedientes, archivo, ensure_ascii=False, indent=4)


# Cargamos los expedientes guardados al iniciar el programa.
expedientes = cargar_expedientes()

# ============================================================
# CONFIGURACION: LIMITES DE EXPEDIENTES POR USUARIO
# ============================================================
LIMITE_EXPEDIENTES_PERSONA_NATURAL = 5
LIMITE_EXPEDIENTES_ADMINISTRADOR = 50

# ------------------------------------------------------------
# ARCHIVO JSON PARA SIMULAR UNA CONSULTA A RENIEC
# Los registros DNI se mantienen en SEDAPAL_base_DNI.json.
# Los expedientes se guardan por separado en SEDAPAL_expedientes.json.
# ------------------------------------------------------------
BASE_DNI_ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SEDAPAL_base_DNI.json"
)


def guardar_base_dni(datos):
    """Guarda los registros de DNI en el archivo JSON."""
    with open(BASE_DNI_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)


def cargar_base_dni():
    """Lee los registros desde JSON. Si no existe, crea uno vacio."""
    if not os.path.exists(BASE_DNI_ARCHIVO):
        guardar_base_dni([])
        print("Se creo un JSON vacio:", BASE_DNI_ARCHIVO)
        print("Coloque los registros de prueba en ese archivo o agreguelos desde el administrador.")
        return []

    try:
        with open(BASE_DNI_ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido principal del JSON debe ser una lista.")

        campos_obligatorios = [
            "dni", "nombres", "apellidos", "numero_verificador"
        ]
        dni_vistos = set()

        for registro in datos:
            if not isinstance(registro, dict):
                raise ValueError("Cada registro debe ser un objeto JSON.")

            for campo in campos_obligatorios:
                if campo not in registro:
                    raise ValueError("Falta el campo obligatorio: " + campo)
                if not isinstance(registro[campo], str):
                    raise ValueError("El campo debe ser texto: " + campo)
                registro[campo] = registro[campo].strip()

            registro.setdefault("fecha_emision", "")
            if not isinstance(registro["fecha_emision"], str):
                raise ValueError("El campo fecha_emision debe ser texto.")
            registro["fecha_emision"] = registro["fecha_emision"].strip()

            if len(registro["dni"]) != 8 or not registro["dni"].isdigit():
                raise ValueError("Se encontro un DNI con formato incorrecto.")

            if len(registro["numero_verificador"]) != 1 or not registro["numero_verificador"].isdigit():
                raise ValueError("Se encontro un numero verificador incorrecto.")

            if registro["dni"] in dni_vistos:
                raise ValueError("Hay un DNI duplicado en el archivo JSON.")
            dni_vistos.add(registro["dni"])

        return datos

    except (json.JSONDecodeError, OSError, ValueError) as error:
        print("ERROR al cargar la base de datos DNI:", error)
        print("Revise el archivo SEDAPAL_base_DNI.json antes de continuar.")
        return []


# Los datos de RENIEC simulada se cargan exclusivamente desde JSON.
base_dni = cargar_base_dni()


def buscar_registro_dni(dni):
    """Busca y devuelve el registro completo de un DNI."""
    for registro in base_dni:
        if registro["dni"] == dni:
            return registro
    return None

# ------------------------------------------------------------
# LISTAS PARA LOS USUARIOS DEL SISTEMA (LISTAS PARALELAS)
# Perfil 1 = Persona natural
# Perfil 2 = Administrador
# ------------------------------------------------------------
usuarios_dni = ["60549429", "12345678"]
usuarios_nombres = ["Jhanmer", "Carlos"]
usuarios_apellidos = ["Meza", "Ramirez"]
usuarios_telefono = ["", ""]
usuarios_correo = ["", ""]
usuarios_claves = ["admin123", "admin456"]
usuarios_perfiles = [2, 2]

# Estructura de usuarios: DNI, nombres, apellidos, telefono,
# correo, clave, perfil y contador reservado.
usuarios = [
    ["60549429", "Jhanmer", "Meza", "", "", "admin123", 2, 0],
    ["12345678", "Carlos", "Ramirez", "", "", "admin456", 2, 0]
]

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

    dia_texto, mes_texto, anio_texto = partes

    if len(dia_texto) != 2 or len(mes_texto) != 2 or len(anio_texto) != 4:
        return False

    if not (dia_texto.isdigit() and mes_texto.isdigit() and anio_texto.isdigit()):
        return False

    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)

    if anio < 2026 or anio > 2100:
        return False

    if mes < 1 or mes > 12:
        return False

    if mes in [4, 6, 9, 11]:
        maximo_dias = 30
    elif mes == 2:
        if anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0):
            maximo_dias = 29
        else:
            maximo_dias = 28
    else:
        maximo_dias = 31

    return 1 <= dia <= maximo_dias


# Para fecha de emision del DNI se permiten años anteriores a 2026.
def validar_fecha_emision(fecha):
    partes = fecha.split("/")

    if len(partes) != 3:
        return False

    dia_texto, mes_texto, anio_texto = partes
    if len(dia_texto) != 2 or len(mes_texto) != 2 or len(anio_texto) != 4:
        return False
    if not (dia_texto.isdigit() and mes_texto.isdigit() and anio_texto.isdigit()):
        return False

    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)

    if anio < 1900 or anio > 2100 or mes < 1 or mes > 12:
        return False

    if mes in [4, 6, 9, 11]:
        maximo_dias = 30
    elif mes == 2:
        maximo_dias = 29 if (anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)) else 28
    else:
        maximo_dias = 31

    return 1 <= dia <= maximo_dias


# ============================================================
# FUNCION PARA VALIDAR CORREO ELECTRONICO
# Se conserva la regla del proyecto: solo gmail.com.
# ============================================================
def validar_correo(email):
    email_limpio = email.strip().lower()
    caracteres_prohibidos = " ,()[]{}!¡¿?/*;:<>=#$"

    for caracter in email_limpio:
        if caracter in caracteres_prohibidos:
            return False

    if email_limpio.count("@") != 1:
        return False

    partes = email_limpio.split("@")
    usuario = partes[0]
    dominio = partes[1]

    return usuario != "" and dominio == "gmail.com"


# ============================================================
# FUNCION PARA VALIDAR TELEFONO
# ============================================================
def validar_telefono(telefono):
    telefono = telefono.strip()

    if telefono == "":
        return False

    for numero in telefono:
        if numero not in "0123456789":
            return False

    longitud = len(telefono)
    primer_digito = telefono[0]

    if primer_digito == "9" and longitud == 9:
        return True
    elif primer_digito == "1" and longitud == 7:
        return True
    elif primer_digito in "2345678" and longitud == 6:
        return True

    return False


# ============================================================
# FUNCION PARA SOLICITAR UN TELEFONO VALIDO
# ============================================================
def solicitar_telefono():
    telefono = input("Ingrese su telefono/celular: ").strip()

    while validar_telefono(telefono) == False:
        print("Telefono incorrecto. Verifique la cantidad de digitos.")
        telefono = input("Ingrese nuevamente su telefono: ").strip()

    return telefono


# ============================================================
# FUNCION PARA SOLICITAR UN CORREO VALIDO
# ============================================================
def solicitar_correo():
    correo = input("Ingrese su correo electronico: ").strip()

    while validar_correo(correo) == False:
        print("Correo electronico incorrecto. Use una cuenta @gmail.com.")
        correo = input("Ingrese nuevamente su correo: ").strip()

    return correo


# ============================================================
# FUNCION PARA SIMULAR LA CONSULTA A RENIEC DESDE JSON
# ============================================================
def consultar_reniec(dni):
    registro = buscar_registro_dni(dni)

    if registro is not None:
        return registro["nombres"], registro["apellidos"]

    return "", ""


# ============================================================
# VERIFICACION DEL DNI CON NUMERO VERIFICADOR DEL JSON
# ============================================================
def verificar_digito_verificador(dni, permitir_no_registrado=False):
    registro = buscar_registro_dni(dni)

    if registro is None:
        if permitir_no_registrado:
            return True
        print("DNI no encontrado en la base de datos simulada.")
        return False

    digito = input("Ingrese digito verificador: ").strip()

    if digito == registro["numero_verificador"]:
        print("DNI verificado correctamente.")
        return True

    print("Digito verificador incorrecto.")
    return False


# ============================================================
# FUNCION PARA AGREGAR UN NUEVO DNI AL ARCHIVO JSON
# Esta opcion se habilita desde el menu del administrador.
# Los datos son de demostracion, no se verifican con RENIEC.
# ============================================================
def registrar_dni_simulado():
    print("\n========================================")
    print("       AGREGAR DNI A BASE JSON")
    print("========================================")

    dni = input("Ingrese el DNI: ").strip()

    while validar_dni(dni) == False:
        print("El DNI debe tener exactamente 8 numeros.")
        dni = input("Ingrese el DNI nuevamente: ").strip()

    if buscar_registro_dni(dni) is not None:
        print("Este DNI ya existe en la base JSON.")
        return

    nombres = input("Ingrese los nombres: ").strip()
    while texto_valido(nombres) == False:
        print("Ingrese nombres validos, utilizando solo letras y espacios.")
        nombres = input("Ingrese los nombres: ").strip()

    apellidos = input("Ingrese los apellidos: ").strip()
    while texto_valido(apellidos) == False:
        print("Ingrese apellidos validos, utilizando solo letras y espacios.")
        apellidos = input("Ingrese los apellidos: ").strip()

    fecha_emision = input("Ingrese fecha de emision (DD/MM/AAAA) o Enter para omitir: ").strip()
    while fecha_emision != "" and validar_fecha_emision(fecha_emision) == False:
        print("Fecha incorrecta. Use DD/MM/AAAA y una fecha valida desde 1900.")
        fecha_emision = input("Ingrese fecha de emision o Enter para omitir: ").strip()

    digito = input("Ingrese el numero verificador (1 digito): ").strip()
    while len(digito) != 1 or digito not in "0123456789":
        print("El numero verificador debe ser un solo digito.")
        digito = input("Ingrese nuevamente el numero verificador: ").strip()

    nuevo_registro = {
        "dni": dni,
        "nombres": nombres,
        "apellidos": apellidos,
        "fecha_emision": fecha_emision,
        "numero_verificador": digito
    }

    nuevos_datos = base_dni + [nuevo_registro]

    try:
        guardar_base_dni(nuevos_datos)
    except OSError as error:
        print("No se pudo guardar el registro en JSON:", error)
        return

    base_dni.append(nuevo_registro)

    print("\nDNI agregado y guardado correctamente.")
    print("Nombre:", nombres, apellidos)
    print("Archivo: SEDAPAL_base_DNI.json")


# ============================================================
# FUNCION PARA GENERAR CODIGO DE EXPEDIENTE
# ============================================================
def generar_codigo():
    numero = len(expedientes) + 1

    if numero < 10:
        codigo = "SED-000" + str(numero)
    elif numero < 100:
        codigo = "SED-00" + str(numero)
    else:
        codigo = "SED-0" + str(numero)

    return codigo


# ============================================================
# FUNCIONES PARA CONTROLAR EL LIMITE DE EXPEDIENTES
# ============================================================
def contar_expedientes_usuario(dni):
    contador = 0

    for expediente in expedientes:
        if expediente[1] == dni:
            contador += 1

    return contador


def obtener_limite_usuario(posicion_usuario):
    if usuarios_perfiles[posicion_usuario] == 2:
        return LIMITE_EXPEDIENTES_ADMINISTRADOR

    return LIMITE_EXPEDIENTES_PERSONA_NATURAL


def puede_registrar_expediente(posicion_usuario):
    dni_usuario = usuarios_dni[posicion_usuario]
    limite = obtener_limite_usuario(posicion_usuario)
    actuales = contar_expedientes_usuario(dni_usuario)

    if actuales >= limite:
        print("\n========================================")
        print("        LIMITE ALCANZADO")
        print("========================================")
        print("Ya registraste", actuales, "de", limite, "expedientes permitidos.")
        print("No puedes registrar mas expedientes por ahora.")
        return False

    print("Expedientes registrados:", actuales, "/", limite)
    return True


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

    if dni in usuarios_dni:
        print("Este DNI ya tiene una cuenta en el sistema.")
        return

    # El DNI debe existir en el JSON antes de crear una cuenta.
    nombre, apellidos = consultar_reniec(dni)

    if nombre == "":
        print("DNI no encontrado en SEDAPAL_base_DNI.json.")
        print("Solicite al administrador que agregue el registro de prueba.")
        print("No se puede completar el registro.")
        return

    # Verificamos el numero registrado en el JSON.
    if verificar_digito_verificador(dni) == False:
        print("No se puede completar el registro.")
        return

    print("Nombre encontrado:", nombre)
    print("Apellidos encontrados:", apellidos)

    telefono = solicitar_telefono()
    correo = solicitar_correo()

    clave = input("Cree su contraseña: ")
    while clave == "":
        print("La contraseña no puede estar vacia.")
        clave = input("Cree su contraseña: ")

    # Guardamos los datos en las listas paralelas.
    usuarios_dni.append(dni)
    usuarios_nombres.append(nombre)
    usuarios_apellidos.append(apellidos)
    usuarios_telefono.append(telefono)
    usuarios_correo.append(correo)
    usuarios_claves.append(clave)
    usuarios_perfiles.append(1)

    # Guardamos tambien el usuario en la estructura principal.
    usuarios.append([dni, nombre, apellidos, telefono, correo, clave, 1, 0])

    print("\nUsuario registrado correctamente.")
    print("Tu perfil es: Persona natural.")
    print("Ya puedes iniciar sesion.")


# ============================================================
# FUNCION PARA INICIAR SESION
# ============================================================
def iniciar_sesion():
    print("\n========================================")
    print("              INICIAR SESION")
    print("========================================")

    dni = input("Ingrese su DNI: ").strip()

    if validar_dni(dni) == False:
        print("DNI incorrecto. Debe tener exactamente 8 numeros.")
        return -1

    # Primero comprobamos que exista una cuenta en el sistema.
    posicion = -1
    for i in range(len(usuarios)):
        if usuarios[i][0] == dni:
            posicion = i
            break

    if posicion == -1:
        print("Usuario no encontrado.")
        return -1

    # Si el DNI existe en el JSON, se solicita el digito verificador.
    # La cuenta administrativa 12345678 no esta en el JSON inicial.
    if buscar_registro_dni(dni) is not None:
        if verificar_digito_verificador(dni) == False:
            return -1

        # Verifica si el usuario tiene el perfil de Persona Natural (1).
    if usuarios[posicion][6] == 1:

        # Inicializa el contador de intentos en cero.
        intentos = 0

        # Permite ingresar la contraseña mientras no supere los 3 intentos.
        while intentos < 3:

            # Solicita la contraseña al usuario.
            clave = input("Ingrese su contraseña: ")

            # Comprueba si la contraseña ingresada es correcta.
            if usuarios[posicion][5] == clave:

                # Muestra el mensaje de bienvenida y el perfil del usuario.
                print("\nBienvenido:", usuarios[posicion][1], usuarios[posicion][2])
                print("Perfil: Persona natural")

                # Devuelve la posición del usuario y finaliza el inicio de sesión.
                return posicion

            # Aumenta en uno el contador cuando la contraseña es incorrecta.
            intentos += 1

            # Si todavía quedan intentos, informa cuántos están disponibles.
            if intentos < 3:
                print("Contraseña incorrecta. Intentos restantes:", 3 - intentos)

        # Informa que se agotaron los tres intentos permitidos.
        print("\nMuchos intentos. Vuelve a intentar.")

        # Finaliza el inicio de sesión sin permitir el acceso.
        return -1

    # Si el usuario es administrador (perfil 2), solicita su contraseña.
    # Mantiene la validación original de un solo intento.
    clave = input("Ingrese su contraseña: ")

    # Comprueba si la contraseña del administrador es correcta.
    if usuarios[posicion][5] == clave:

        # Muestra el mensaje de bienvenida y el perfil de administrador.
        print("\nBienvenido:", usuarios[posicion][1], usuarios[posicion][2])
        print("Perfil: Administrador")

        # Devuelve la posición del administrador y permite continuar.
        return posicion

    # Si la contraseña es incorrecta, muestra un mensaje de error.
    print("\nContraseña incorrecta.")

    # Finaliza el inicio de sesión sin permitir el acceso.
    return -1


# ------------------------------------------------------------
# FUNCION PARA REGISTRAR UN EXPEDIENTE
# ------------------------------------------------------------
def registrar_expediente(posicion_usuario):
    print("\n========================================")
    print("          REGISTRO DE EXPEDIENTE")
    print("========================================")

    if not puede_registrar_expediente(posicion_usuario):
        return

    codigo = generar_codigo()
    print("Codigo del expediente:", codigo)

    # PERSONA NATURAL: se recuperan los datos de su cuenta.
    if usuarios[posicion_usuario][6] == 1:
        dni = usuarios[posicion_usuario][0]
        nombre = usuarios[posicion_usuario][1]
        apellidos = usuarios[posicion_usuario][2]
        telefono = usuarios[posicion_usuario][3]
        correo = usuarios[posicion_usuario][4]

        print("\nDatos recuperados de tu cuenta:")
        print("DNI:", dni)
        print("Nombre:", nombre)
        print("Apellidos:", apellidos)
        print("Telefono:", telefono)
        print("Correo:", correo)

    # ADMINISTRADOR: registra los datos del ciudadano manualmente.
    else:
        dni = input("Ingrese el DNI del ciudadano: ").strip()

        while validar_dni(dni) == False:
            print("Error: el DNI debe tener exactamente 8 numeros.")
            dni = input("Ingrese nuevamente el DNI: ").strip()

        nombre, apellidos = consultar_reniec(dni)

        while nombre == "":
            print("DNI no encontrado en la base JSON simulada.")
            dni = input("Ingrese otro DNI: ").strip()

            while validar_dni(dni) == False:
                print("Error: el DNI debe tener exactamente 8 numeros.")
                dni = input("Ingrese nuevamente el DNI: ").strip()

            nombre, apellidos = consultar_reniec(dni)

        print("Nombre encontrado:", nombre)
        print("Apellidos encontrados:", apellidos)

        telefono = solicitar_telefono()
        correo = solicitar_correo()

    print("\nSeleccione el tipo de tramite:")
    print("1. Queja y reclamo")
    print("2. Solicitud")
    print("3. Consulta")
    opcion = input("Ingrese una opcion: ").strip()

    while opcion not in ["1", "2", "3"]:
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
        print("Fecha incorrecta. Use DD/MM/AAAA y una fecha valida.")
        fecha = input("Ingrese la fecha (DD/MM/AAAA): ").strip()

    print("\nSeleccione la prioridad:")
    print("1. Alta")
    print("2. Media")
    print("3. Baja")

    if usuarios[posicion_usuario][6] == 1:
        prioridad = "Media"
        print("Tu expediente se registrara con prioridad Media.")
    else:
        opcion_prioridad = input("Ingrese una opcion: ").strip()

        while opcion_prioridad not in ["1", "2", "3"]:
            print("Opcion incorrecta.")
            opcion_prioridad = input("Ingrese una opcion: ").strip()

        if opcion_prioridad == "1":
            prioridad = "Alta"
        elif opcion_prioridad == "2":
            prioridad = "Media"
        else:
            prioridad = "Baja"

    estado = "Pendiente"

    expediente = [
        codigo, dni, nombre, apellidos, telefono, correo,
        tipo, descripcion, "SJL", fecha, estado, prioridad
    ]

    expedientes.append(expediente)

    try:
        guardar_expedientes_json()
    except OSError as error:
        print("Advertencia: el expediente quedo en memoria, pero no se pudo guardar en JSON:", error)
    else:
        print("Expediente guardado en SEDAPAL_expedientes.json.")

    print("\nExpediente registrado correctamente.")
    print("Codigo:", codigo)
    print("Prioridad:", prioridad)
    print("Estado:", estado)


# ============================================================
# PAUSA PARA LEER LOS RESULTADOS ANTES DE VOLVER AL MENU
# ============================================================
def esperar_continuar():
    input("\nPresione ENTER para volver al menu...")


# ------------------------------------------------------------
# FUNCION PARA MOSTRAR EXPEDIENTES
# ------------------------------------------------------------
def mostrar_expedientes(posicion_usuario, estado=None):
    print("\n========================================")
    print("             EXPEDIENTES")
    print("========================================")

    encontrados = 0
    es_administrador = usuarios[posicion_usuario][6] == 2
    dni_usuario = usuarios[posicion_usuario][0]

    for expediente in expedientes:
        es_propietario = expediente[1].strip() == dni_usuario
        estado_expediente = expediente[10].strip().lower()

        if (es_administrador or es_propietario) and (
            estado is None
            or (estado == "activo" and estado_expediente in ["pendiente", "en proceso"])
            or  estado == "historial"
        ): 
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
            encontrados += 1

    if encontrados == 0:
        print("No hay expedientes para mostrar.")
    else:
        print("\nTotal de expedientes encontrados:", encontrados)

    # Espera para que el administrador pueda leer los resultados.
    esperar_continuar()


# ------------------------------------------------------------
# FUNCION PARA BUSCAR UN EXPEDIENTE
# ------------------------------------------------------------
def buscar_expediente(posicion_usuario):
    print("\n==========================================")
    print("        BUSCAR EXPEDIENTE")
    print("==========================================")
    print("1. Buscar por DNI")
    print("2. Buscar por codigo")

    opcion = input("Seleccione una opcion: ").strip()
    while opcion not in ["1", "2"]:
        print("Opcion incorrecta.")
        opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
        dato_buscar = input("Ingrese el DNI: ").strip()
        if validar_dni(dato_buscar) == False:
            print("El DNI debe tener exactamente 8 numeros.")
            esperar_continuar()
            return
    else:
        dato_buscar = input("Ingrese el codigo del expediente: ").strip()

    encontrado = False
    es_administrador = usuarios[posicion_usuario][6] == 2
    dni_usuario = usuarios[posicion_usuario][0]

    for expediente in expedientes:
        if opcion == "1":
            coincide = expediente[1] == dato_buscar
        else:
            coincide = expediente[0] == dato_buscar

        if coincide:
            # La persona natural solo puede consultar sus propios expedientes.
            if not es_administrador and expediente[1] != dni_usuario:
                continue

            print("\nExpediente encontrado:")
            print("------------------------------------------")
            print("Codigo:", expediente[0])
            print("DNI:", expediente[1])
            print("Ciudadano:", expediente[2], expediente[3])
            print("Telefono/Celular:", expediente[4])
            print("Correo electronico:", expediente[5])
            print("Tipo:", expediente[6])
            print("Descripcion:", expediente[7])
            print("Sede:", expediente[8])
            print("Fecha:", expediente[9])
            print("Estado:", expediente[10])
            print("Prioridad:", expediente[11])
            encontrado = True

    if encontrado == False:
        print("No se encontro el expediente o no tienes permiso para verlo.")
    else:
        print("\nBusqueda finalizada.")

    # Espera para que el usuario pueda leer el resultado.
    esperar_continuar()


# ------------------------------------------------------------
# FUNCION PARA ACTUALIZAR EL ESTADO (SOLO ADMINISTRADOR)
# ------------------------------------------------------------
def actualizar_estado():
    print("\n==========================================")
    print("       ACTUALIZAR ESTADO")
    print("==========================================")
    codigo_buscar = input("Ingrese el codigo del expediente: ").strip()

    for expediente in expedientes:
        if expediente[0] == codigo_buscar:
            print("Estado actual:", expediente[10])
            print("1. Pendiente")
            print("2. En proceso")
            print("3. Atendido")

            opcion = input("Seleccione el nuevo estado: ").strip()
            while opcion not in ["1", "2", "3"]:
                print("Opcion incorrecta.")
                opcion = input("Seleccione el nuevo estado: ").strip()

            if opcion == "1":
                expediente[10] = "Pendiente"
            elif opcion == "2":
                expediente[10] = "En proceso"
            else:
                expediente[10] = "Atendido"

            try:
                guardar_expedientes_json()
            except OSError as error:
                print("Advertencia: no se pudo guardar el nuevo estado en JSON:", error)

            print("\nEstado actualizado correctamente.")
            print("Codigo:", expediente[0])
            print("Nuevo estado:", expediente[10])
            return

    print("No se encontro el expediente.")


# ============================================================
# FUNCION PARA ORDENAR POR PRIORIDAD
# Alta primero, luego Media y finalmente Baja.
# ============================================================
def ordenar_expedientes():
    print("\n==========================================")
    print("       ORDENAR EXPEDIENTES")
    print("==========================================")

    if len(expedientes) == 0:
        print("No existen expedientes para ordenar.")
        return

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

    try:
        guardar_expedientes_json()
    except OSError as error:
        print("Advertencia: no se pudo guardar el orden en JSON:", error)

    print("Expedientes ordenados por prioridad.")
    print("Orden: Alta, Media y Baja.")


# ------------------------------------------------------------
# FUNCION PARA GUARDAR EXPEDIENTES EN ARCHIVO DE TEXTO
# ------------------------------------------------------------
def guardar_archivo():
    print("\n==========================================")
    print("       GUARDAR EXPEDIENTES")
    print("==========================================")

    if len(expedientes) == 0:
        print("No existen expedientes para guardar.")
        return

    try:
        guardar_expedientes_json()
        archivo_txt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expedientes_sedapal.txt")
        with open(archivo_txt, "w", encoding="utf-8") as archivo:
            for expediente in expedientes:
                archivo.write("====================================\n")
                archivo.write("Codigo: " + expediente[0] + "\n")
                archivo.write("DNI: " + expediente[1] + "\n")
                archivo.write("Ciudadano: " + expediente[2] + " " + expediente[3] + "\n")
                archivo.write("Telefono/Celular: " + expediente[4] + "\n")
                archivo.write("Correo electronico: " + expediente[5] + "\n")
                archivo.write("Tipo: " + expediente[6] + "\n")
                archivo.write("Descripcion: " + expediente[7] + "\n")
                archivo.write("Sede: " + expediente[8] + "\n")
                archivo.write("Fecha: " + expediente[9] + "\n")
                archivo.write("Estado: " + expediente[10] + "\n")
                archivo.write("Prioridad: " + expediente[11] + "\n")

    except OSError as error:
        print("No se pudieron guardar los expedientes:", error)
        return

    print("Los expedientes fueron guardados correctamente.")
    print("Archivo: expedientes_sedapal.txt")
    print("Copia permanente: SEDAPAL_expedientes.json")


# ============================================================
# MENU PARA PERSONA NATURAL
# ============================================================
def menu_persona_natural(posicion_usuario):
    opcion = ""

    while opcion != "4":
        print("\n========================================")
        print("       MENU - PERSONA NATURAL")
        print("========================================")

        usados = contar_expedientes_usuario(usuarios_dni[posicion_usuario])
        disponibles = LIMITE_EXPEDIENTES_PERSONA_NATURAL - usados
        if disponibles < 0:
            disponibles = 0

        print("Expedientes disponibles:", disponibles, "/", LIMITE_EXPEDIENTES_PERSONA_NATURAL)
        print("1. Registrar/enviar documento")
        print("2. Ver mis expedientes activos")
        print("3. Historial de expedientes")
        print("4. Cerrar sesion")

        opcion = input("Seleccione una opcion: ").strip()

        # Ejecutamos la opcion seleccionada.
        if opcion == "1":
            registrar_expediente(posicion_usuario)

        elif opcion == "2":
            # Muestra expedientes pendientes y en proceso.
            mostrar_expedientes(posicion_usuario, "activo")

        elif opcion == "3":
            # Muestra todos los expedientes registrados del usuario.
            mostrar_expedientes(posicion_usuario, "historial")

        elif opcion == "4":
            print("Sesion cerrada.")

        else:
            print("Opcion incorrecta.")


# ============================================================
# MENU PARA ADMINISTRADOR
# ============================================================
def menu_administrador(posicion_usuario):
    opcion = ""

    while opcion != "8":
        print("\n========================================")
        print("         MENU - ADMINISTRADOR")
        print("========================================")
        print("1. Registrar expediente")
        print("2. Mostrar todos los expedientes")
        print("3. Buscar expediente")
        print("4. Actualizar estado")
        print("5. Ordenar por prioridad")
        print("6. Guardar expedientes en archivo")
        print("7. Agregar DNI a base JSON")
        print("8. Cerrar sesion")

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
            registrar_dni_simulado()
        elif opcion == "8":
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
                if usuarios[posicion][6] == 2:
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
# Esta llamada debe quedar al final, despues de definir funciones.
# ============================================================
if __name__ == "__main__":
    menu_inicial()
