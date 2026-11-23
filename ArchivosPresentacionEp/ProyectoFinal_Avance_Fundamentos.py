from builtins import print, range
import json
import os
from datetime import datetime

# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL v 0.1.7
# ============================================================
# Esta version incorpora JSON para DNI, expedientes y usuarios.
# Ademas, relaciona la base de usuarios con la de DNI al 
# momento de recuperar contraseña (doble factor).
# ============================================================

# ------------------------------------------------------------
# ARCHIVO JSON PARA GUARDAR LOS EXPEDIENTES
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
            # Compatibilidad con expedientes de 12 campos agregando el campo 13 (respuesta_cita).
            if isinstance(expediente, list) and len(expediente) == 12:
                expediente.append("")

            if not isinstance(expediente, list) or len(expediente) != 13:
                raise ValueError("Cada expediente debe tener exactamente 13 campos.")
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
LIMITE_CONSULTAS_PERSONA_NATURAL = 3

# ------------------------------------------------------------
# ARCHIVO JSON PARA SIMULAR UNA CONSULTA A RENIEC
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
        return []

    try:
        with open(BASE_DNI_ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido principal del JSON debe ser una lista.")

        campos_obligatorios = ["dni", "nombres", "apellidos", "numero_verificador"]
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
        return []

base_dni = cargar_base_dni()

def buscar_registro_dni(dni):
    """Busca y devuelve el registro completo de un DNI."""
    for registro in base_dni:
        if registro["dni"] == dni:
            return registro
    return None

# ============================================================
# ARCHIVO JSON PARA GUARDAR LOS USUARIOS DEL SISTEMA
# Estructura: [dni, nombres, apellidos, telefono, correo, clave, perfil, consultas]
# ============================================================
USUARIOS_ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SEDAPAL_usuarios.json"
)

def guardar_usuarios_json():
    """Guarda todos los usuarios en el archivo JSON."""
    with open(USUARIOS_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, ensure_ascii=False, indent=4)

def cargar_usuarios():
    """Carga los usuarios desde JSON. Si no existe, lo crea con los admins por defecto."""
    if not os.path.exists(USUARIOS_ARCHIVO):
        usuarios_iniciales = [
            ["60549429", "Jhanmer", "Meza", "", "", "admin123", 2, 0],
            ["12345678", "Carlos", "Ramirez", "", "", "admin456", 2, 0]
        ]
        with open(USUARIOS_ARCHIVO, "w", encoding="utf-8") as archivo:
            json.dump(usuarios_iniciales, archivo, ensure_ascii=False, indent=4)
        print("Se creo un JSON de usuarios:", USUARIOS_ARCHIVO)
        return usuarios_iniciales

    try:
        with open(USUARIOS_ARCHIVO, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        if not isinstance(datos, list):
            raise ValueError("El contenido principal debe ser una lista.")

        dni_vistos = set()
        for usuario in datos:
            if not isinstance(usuario, list) or len(usuario) != 8:
                raise ValueError("Cada usuario debe tener exactamente 8 campos.")
            for indice in range(6):
                if not isinstance(usuario[indice], str):
                    raise ValueError("Los campos de texto del usuario deben ser cadenas.")
            if not isinstance(usuario[6], int) or not isinstance(usuario[7], int):
                raise ValueError("Los campos perfil y consultas deben ser enteros.")
            if usuario[6] not in (1, 2):
                raise ValueError("El perfil debe ser 1 (persona natural) o 2 (administrador).")
            if len(usuario[0]) != 8 or not usuario[0].isdigit():
                raise ValueError("Se encontro un DNI de usuario con formato incorrecto.")
            if usuario[0] in dni_vistos:
                raise ValueError("Hay un DNI de usuario duplicado en el archivo JSON.")
            dni_vistos.add(usuario[0])

        return datos
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print("ERROR al cargar SEDAPAL_usuarios.json:", error)
        return []

usuarios = cargar_usuarios()

# ============================================================
# FUNCIONES DE VALIDACION
# ============================================================
def texto_valido(texto):
    texto_limpio = texto.strip()
    if texto_limpio == "": return False
    permitidas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "
    for letra in texto_limpio:
        if letra not in permitidas: return False
    return True

def validar_dni(dni):
    if len(dni) != 8: return False
    for caracter in dni:
        if caracter < "0" or caracter > "9": return False
    return True

def validar_fecha(fecha):
    partes = fecha.split("/")
    if len(partes) != 3: return False
    dia_texto, mes_texto, anio_texto = partes
    if len(dia_texto) != 2 or len(mes_texto) != 2 or len(anio_texto) != 4: return False
    if not (dia_texto.isdigit() and mes_texto.isdigit() and anio_texto.isdigit()): return False
    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)
    if anio < 2026 or anio > 2100: return False
    if mes < 1 or mes > 12: return False
    if mes in [4, 6, 9, 11]: maximo_dias = 30
    elif mes == 2:
        maximo_dias = 29 if (anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)) else 28
    else: maximo_dias = 31
    return 1 <= dia <= maximo_dias

def validar_fecha_emision(fecha):
    partes = fecha.split("/")
    if len(partes) != 3: return False
    dia_texto, mes_texto, anio_texto = partes
    if len(dia_texto) != 2 or len(mes_texto) != 2 or len(anio_texto) != 4: return False
    if not (dia_texto.isdigit() and mes_texto.isdigit() and anio_texto.isdigit()): return False
    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)
    if anio < 1900 or anio > 2100 or mes < 1 or mes > 12: return False
    if mes in [4, 6, 9, 11]: maximo_dias = 30
    elif mes == 2:
        maximo_dias = 29 if (anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)) else 28
    else: maximo_dias = 31
    return 1 <= dia <= maximo_dias

def dias_desde(fecha_texto):
    try:
        fecha = datetime.strptime(fecha_texto, "%d/%m/%Y")
        return (datetime.now() - fecha).days
    except (ValueError, TypeError): return None

def extraer_fecha_cita(respuesta_cita):
    if not respuesta_cita or not respuesta_cita.startswith("Fecha: "): return None
    resto = respuesta_cita[len("Fecha: "):]
    fecha = resto.split("|")[0].strip()
    return fecha if fecha != "" else None

def validar_correo(email):
    email_limpio = email.strip().lower()
    caracteres_prohibidos = " ,()[]{}!¡¿?/*;:<>=#$"
    for caracter in email_limpio:
        if caracter in caracteres_prohibidos: return False
    if email_limpio.count("@") != 1: return False
    partes = email_limpio.split("@")
    usuario = partes[0]
    dominio = partes[1]
    return usuario != "" and dominio == "gmail.com"

def validar_telefono(telefono):
    telefono = telefono.strip()
    if telefono == "": return False
    for numero in telefono:
        if numero not in "0123456789": return False
    longitud = len(telefono)
    primer_digito = telefono[0]
    if primer_digito == "9" and longitud == 9: return True
    elif primer_digito == "1" and longitud == 7: return True
    elif primer_digito in "2345678" and longitud == 6: return True
    return False

def solicitar_telefono():
    telefono = input("Ingrese su telefono/celular: ").strip()
    while validar_telefono(telefono) == False:
        print("Telefono incorrecto. Verifique la cantidad de digitos.")
        telefono = input("Ingrese nuevamente su telefono: ").strip()
    return telefono

def solicitar_correo():
    correo = input("Ingrese su correo electronico: ").strip()
    while validar_correo(correo) == False:
        print("Correo electronico incorrecto. Use una cuenta @gmail.com.")
        correo = input("Ingrese nuevamente su correo: ").strip()
    return correo

# ============================================================
# FUNCIONES DE RENIEC SIMULADA
# ============================================================
def consultar_reniec(dni):
    registro = buscar_registro_dni(dni)
    if registro is not None:
        return registro["nombres"], registro["apellidos"]
    return "", ""

def verificar_digito_verificador(dni, permitir_no_registrado=False):
    registro = buscar_registro_dni(dni)
    if registro is None:
        if permitir_no_registrado: return True
        print("DNI no encontrado en la base de datos simulada.")
        return False
    digito = input("Ingrese digito verificador: ").strip()
    if digito == registro["numero_verificador"]:
        print("DNI verificado correctamente.")
        return True
    print("Digito verificador incorrecto.")
    return False

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
        "dni": dni, "nombres": nombres, "apellidos": apellidos,
        "fecha_emision": fecha_emision, "numero_verificador": digito
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

# ============================================================
# FUNCIONES DE EXPEDIENTES Y LIMITES
# ============================================================
def generar_codigo():
    max_numero = 0
    for expediente in expedientes:
        codigo = expediente[0]
        if codigo.startswith("SED-"):
            parte = codigo[4:]
            if parte.isdigit():
                numero = int(parte)
                if numero > max_numero: max_numero = numero
    return "SED-" + str(max_numero + 1).zfill(4)

def contar_expedientes_usuario(dni):
    contador = 0
    for expediente in expedientes:
        if expediente[1] == dni and expediente[10] != "Anulado":
            contador += 1
    return contador

def obtener_limite_usuario(posicion_usuario):
    if usuarios[posicion_usuario][6] == 2:
        return LIMITE_EXPEDIENTES_ADMINISTRADOR
    return LIMITE_EXPEDIENTES_PERSONA_NATURAL

def puede_registrar_expediente(posicion_usuario):
    dni_usuario = usuarios[posicion_usuario][0]
    limite = obtener_limite_usuario(posicion_usuario)
    actuales = contar_expedientes_usuario(dni_usuario)
    if actuales >= limite:
        print("\n========================================")
        print("        LIMITE ALCANZADO")
        print("========================================")
        print("Ya registraste", actuales, "de", limite, "expedientes permitidos.")
        return False
    print("Expedientes registrados:", actuales, "/", limite)
    return True

# ============================================================
# REGISTRO E INICIO DE SESION DE USUARIOS
# ============================================================
def registrar_usuario():
    print("\n========================================")
    print("          CREAR NUEVO USUARIO")
    print("========================================")
    dni = input("Ingrese su DNI: ").strip()
    while validar_dni(dni) == False:
        print("El DNI debe tener exactamente 8 numeros.")
        dni = input("Ingrese su DNI nuevamente: ").strip()

    for i in range(len(usuarios)):
        if usuarios[i][0] == dni:
            print("Este DNI ya tiene una cuenta en el sistema.")
            return

    nombre, apellidos = consultar_reniec(dni)
    if nombre == "":
        print("DNI no encontrado en la lista simulada.")
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

    usuarios.append([dni, nombre, apellidos, telefono, correo, clave, 1, 0])
    try:
        guardar_usuarios_json()
    except OSError as error:
        print("Advertencia: el usuario quedo en memoria, pero no se pudo guardar en JSON:", error)

    print("\nUsuario registrado correctamente.")
    print("Tu perfil es: Persona natural.")
    print("Ya puedes iniciar sesion.")

def iniciar_sesion():
    print("\n========================================")
    print("              INICIAR SESION")
    print("========================================")
    dni = input("Ingrese su DNI: ").strip()

    if validar_dni(dni) == False:
        print("DNI incorrecto. Debe tener exactamente 8 numeros.")
        return -1

    posicion = -1
    for i in range(len(usuarios)):
        if usuarios[i][0] == dni:
            posicion = i
            break

    if posicion == -1:
        print("Usuario no encontrado.")
        return -1

    if buscar_registro_dni(dni) is not None:
        if verificar_digito_verificador(dni) == False:
            return -1

    if usuarios[posicion][6] == 1:
        intentos = 0
        while intentos < 3:
            clave = input("Ingrese su contraseña: ")
            if usuarios[posicion][5] == clave:
                print("\nBienvenido:", usuarios[posicion][1], usuarios[posicion][2])
                print("Perfil: Persona natural")
                return posicion
            intentos += 1
            if intentos < 3:
                print("Contraseña incorrecta. Intentos restantes:", 3 - intentos)
        print("\nMuchos intentos. Vuelve a intentar.")
        return -1

    clave = input("Ingrese su contraseña: ")
    if usuarios[posicion][5] == clave:
        print("\nBienvenido:", usuarios[posicion][1], usuarios[posicion][2])
        print("Perfil: Administrador")
        return posicion

    print("\nContraseña incorrecta.")
    return -1

# ============================================================
# REGISTRO DE EXPEDIENTES Y CONSULTAS
# ============================================================
def registrar_expediente(posicion_usuario):
    print("\n========================================")
    print("          REGISTRO DE EXPEDIENTE")
    print("========================================")
    if not puede_registrar_expediente(posicion_usuario):
        return

    codigo = generar_codigo()
    print("Codigo del expediente:", codigo)

    if usuarios[posicion_usuario][6] == 1:
        dni = usuarios[posicion_usuario][0]
        nombre = usuarios[posicion_usuario][1]
        apellidos = usuarios[posicion_usuario][2]
        telefono = usuarios[posicion_usuario][3]
        correo = usuarios[posicion_usuario][4]
        print("\nDatos recuperados de tu cuenta:")
        print("DNI:", dni, "| Nombre:", nombre, apellidos)
        print("Telefono:", telefono, "| Correo:", correo)
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

        print("Nombre encontrado:", nombre, apellidos)
        telefono = solicitar_telefono()
        correo = solicitar_correo()

    print("\nSeleccione el tipo de tramite:")
    print("1. Queja y reclamo\n2. Solicitud\n3. Consulta")
    opcion = input("Ingrese una opcion: ").strip()
    while opcion not in ["1", "2", "3"]:
        opcion = input("Opcion incorrecta. Ingrese una opcion: ").strip()
    
    tipo = "Queja y reclamo" if opcion == "1" else ("Solicitud" if opcion == "2" else "Consulta")

    descripcion = input("Ingrese la descripcion del tramite: ").strip()
    while descripcion == "":
        descripcion = input("La descripcion no puede estar vacia. Ingrese la descripcion: ").strip()

    fecha = input("Ingrese la fecha (DD/MM/AAAA): ").strip()
    while validar_fecha(fecha) == False:
        print("Fecha incorrecta. Use DD/MM/AAAA y una fecha valida.")
        fecha = input("Ingrese la fecha (DD/MM/AAAA): ").strip()

    if usuarios[posicion_usuario][6] == 1:
        prioridad = "Media"
        print("\nTu expediente se registrara con prioridad Media.")
    else:
        print("\nSeleccione la prioridad:\n1. Alta\n2. Media\n3. Baja")
        opcion_prioridad = input("Ingrese una opcion: ").strip()
        while opcion_prioridad not in ["1", "2", "3"]:
            opcion_prioridad = input("Opcion incorrecta. Ingrese una opcion: ").strip()
        prioridad = "Alta" if opcion_prioridad == "1" else ("Media" if opcion_prioridad == "2" else "Baja")

    expediente = [
        codigo, dni, nombre, apellidos, telefono, correo,
        tipo, descripcion, "SJL", fecha, "Pendiente", prioridad, ""
    ]
    expedientes.append(expediente)

    try:
        guardar_expedientes_json()
        print("Expediente guardado en SEDAPAL_expedientes.json.")
    except OSError as error:
        print("Advertencia: el expediente quedo en memoria, no se pudo guardar en JSON:", error)

    print("\nExpediente registrado correctamente.")
    print("Codigo:", codigo, "| Prioridad:", prioridad, "| Estado: Pendiente")

def esperar_continuar():
    input("\nPresione ENTER para volver al menu...")

def puede_consultar(posicion_usuario):
    if usuarios[posicion_usuario][6] == 2: return True
    consultas = usuarios[posicion_usuario][7]
    if consultas >= LIMITE_CONSULTAS_PERSONA_NATURAL:
        print("\n========================================")
        print("       LIMITE DE CONSULTAS ALCANZADO")
        print("========================================")
        print("Ya utilizaste tus 3 consultas permitidas.")
        esperar_continuar()
        return False
    usuarios[posicion_usuario][7] += 1
    try:
        guardar_usuarios_json()
    except OSError:
        pass
    print("Consultas disponibles:", LIMITE_CONSULTAS_PERSONA_NATURAL - usuarios[posicion_usuario][7])
    return True

def mostrar_expedientes(posicion_usuario, estado=None):
    if puede_consultar(posicion_usuario) == False: return
    print("\n========================================\n             EXPEDIENTES\n========================================")
    encontrados = 0
    es_administrador = usuarios[posicion_usuario][6] == 2
    dni_usuario = usuarios[posicion_usuario][0]

    for expediente in expedientes:
        es_propietario = expediente[1].strip() == dni_usuario
        estado_expediente = expediente[10].strip().lower()

        if (es_administrador or es_propietario) and (
            estado is None or (estado == "activo" and estado_expediente in ["pendiente", "en proceso"]) or estado == "historial"
        ):
            print("----------------------------------------")
            print("Codigo:", expediente[0], "| DNI:", expediente[1])
            print("Ciudadano:", expediente[2], expediente[3])
            print("Telefono:", expediente[4], "| Correo:", expediente[5])
            print("Tipo:", expediente[6], "| Prioridad:", expediente[11])
            print("Descripcion:", expediente[7])
            print("Sede:", expediente[8], "| Fecha:", expediente[9])
            print("Estado:", expediente[10])
            print("Respuesta de cita:", expediente[12] if expediente[12] != "" else "Sin cita programada")
            encontrados += 1

    if encontrados == 0:
        print("No hay expedientes para mostrar.")
    else:
        print("\nTotal de expedientes encontrados:", encontrados)
    esperar_continuar()

def generar_reporte_estadistico():
    print("\n==========================================")
    print("       REPORTE ESTADISTICO")
    print("==========================================")
    if len(expedientes) == 0:
        print("No existen expedientes para generar el reporte.")
        esperar_continuar()
        return

    pendientes = en_proceso = atendidos = anulados = 0
    prioridad_alta = prioridad_media = prioridad_baja = 0
    quejas = solicitudes = consultas = 0

    for expediente in expedientes:
        if expediente[10] == "Pendiente": pendientes += 1
        elif expediente[10] == "En proceso": en_proceso += 1
        elif expediente[10] == "Atendido": atendidos += 1
        elif expediente[10] == "Anulado": anulados += 1

        if expediente[11] == "Alta": prioridad_alta += 1
        elif expediente[11] == "Media": prioridad_media += 1
        elif expediente[11] == "Baja": prioridad_baja += 1

        if expediente[6] == "Queja y reclamo": quejas += 1
        elif expediente[6] == "Solicitud": solicitudes += 1
        elif expediente[6] == "Consulta": consultas += 1

    print("\nTOTAL DE EXPEDIENTES:", len(expedientes))
    print("\n--- POR ESTADO ---")
    print("Pendientes:", pendientes, "| En proceso:", en_proceso, "| Atendidos:", atendidos, "| Anulados:", anulados)
    print("\n--- POR PRIORIDAD ---")
    print("Alta:", prioridad_alta, "| Media:", prioridad_media, "| Baja:", prioridad_baja)
    print("\n--- POR TIPO ---")
    print("Quejas:", quejas, "| Solicitudes:", solicitudes, "| Consultas:", consultas)
    print("\n==========================================")
    esperar_continuar()

def buscar_expediente(posicion_usuario):
    print("\n==========================================")
    print("        BUSCAR EXPEDIENTE")
    print("==========================================")
    print("1. Buscar por DNI\n2. Buscar por codigo")
    opcion = input("Seleccione una opcion: ").strip()
    while opcion not in ["1", "2"]:
        opcion = input("Opcion incorrecta. Seleccione una opcion: ").strip()

    if opcion == "1":
        dato_buscar = input("Ingrese el DNI: ").strip()
        if validar_dni(dato_buscar) == False:
            print("El DNI debe tener exactamente 8 numeros.")
            esperar_continuar()
            return
    else:
        dato_buscar = input("Ingrese el codigo del expediente: ").strip().upper()

    encontrado = False
    es_administrador = usuarios[posicion_usuario][6] == 2
    dni_usuario = usuarios[posicion_usuario][0]

    for expediente in expedientes:
        coincide = expediente[1] == dato_buscar if opcion == "1" else expediente[0] == dato_buscar
        if coincide:
            if not es_administrador and expediente[1] != dni_usuario:
                continue
            print("\nExpediente encontrado:")
            print("------------------------------------------")
            print("Codigo:", expediente[0], "| DNI:", expediente[1])
            print("Ciudadano:", expediente[2], expediente[3])
            print("Tipo:", expediente[6], "| Prioridad:", expediente[11])
            print("Descripcion:", expediente[7])
            print("Estado:", expediente[10])
            print("Respuesta de cita:", expediente[12] if expediente[12] != "" else "Sin cita programada")
            encontrado = True

    if encontrado == False:
        print("No se encontro el expediente o no tienes permiso para verlo.")
    esperar_continuar()

def registrar_respuesta_cita():
    print("\n==========================================")
    print("REGISTRAR RESPUESTA POR CORREO DE CITA")
    print("==========================================")
    if len(expedientes) == 0:
        print("No existen expedientes registrados en el sistema.")
        esperar_continuar()
        return

    codigo_buscar = input("Ingrese el codigo del expediente: ").strip().upper()
    expediente_encontrado = None
    for expediente in expedientes:
        if expediente[0].upper() == codigo_buscar:
            expediente_encontrado = expediente
            break

    if expediente_encontrado is None:
        print("Error: El codigo de expediente no existe.")
        esperar_continuar()
        return
    if expediente_encontrado[10] == "Anulado":
        print("No se puede registrar una cita para un expediente anulado.")
        esperar_continuar()
        return

    print("\nCiudadano:", expediente_encontrado[2], expediente_encontrado[3])
    print("Correo destino:", expediente_encontrado[5])
    
    fecha_cita = input("\nIngrese la fecha de la cita (DD/MM/AAAA): ").strip()
    while validar_fecha(fecha_cita) == False:
        fecha_cita = input("Fecha invalida. Ingrese nuevamente (DD/MM/AAAA): ").strip()

    mensaje_cita = input("Ingrese el mensaje o detalle de la cita: ").strip()
    while mensaje_cita == "":
        mensaje_cita = input("El mensaje no puede estar vacio. Ingrese detalle: ").strip()

    print("\n1. En proceso\n2. Atendido")
    opcion_estado = input("Seleccione el nuevo estado: ").strip()
    while opcion_estado not in ["1", "2"]:
        opcion_estado = input("Opcion incorrecta. Elija 1 o 2: ").strip()
    nuevo_estado = "En proceso" if opcion_estado == "1" else "Atendido"

    confirmar = input("\nEscriba S para confirmar envio por correo o N para cancelar: ").strip().upper()
    while confirmar not in ["S", "N"]:
        confirmar = input("Opcion invalida. Escriba S o N: ").strip().upper()

    if confirmar == "N":
        print("Operacion cancelada.")
        esperar_continuar()
        return

    expediente_encontrado[10] = nuevo_estado
    expediente_encontrado[12] = "Fecha: " + fecha_cita + " | Mensaje: " + mensaje_cita

    try:
        guardar_expedientes_json()
    except OSError as error:
        print("Advertencia: No se pudo guardar en JSON:", error)

    print("\n==========================================")
    print("NOTIFICACION DE CORREO ENVIADA")
    print("==========================================")
    print("Para:", expediente_encontrado[5])
    print("Fecha de cita:", fecha_cita, "| Detalle:", mensaje_cita)
    print("Registro guardado correctamente.")
    esperar_continuar()

def actualizar_estado():
    print("\n==========================================")
    print("       ACTUALIZAR ESTADO")
    print("==========================================")
    codigo_buscar = input("Ingrese el codigo del expediente: ").strip().upper()

    for expediente in expedientes:
        if expediente[0] == codigo_buscar:
            if expediente[10] == "Anulado":
                print("\nADVERTENCIA: el expediente esta anulado.")
                confirmar = input("Reactivar como Pendiente? (S/N): ").strip().upper()
                while confirmar not in ["S", "N"]:
                    confirmar = input("Escriba S o N: ").strip().upper()
                if confirmar != "S":
                    print("Operacion cancelada.")
                    return
                expediente[10] = "Pendiente"
                guardar_expedientes_json()
                print("Expediente reactivado. Nuevo estado: Pendiente.")
                return

            print("Estado actual:", expediente[10])
            print("1. Pendiente\n2. En proceso\n3. Atendido")
            opcion = input("Seleccione el nuevo estado: ").strip()
            while opcion not in ["1", "2", "3"]:
                opcion = input("Opcion incorrecta. Seleccione nuevo estado: ").strip()

            expediente[10] = "Pendiente" if opcion == "1" else ("En proceso" if opcion == "2" else "Atendido")
            try:
                guardar_expedientes_json()
            except OSError as error:
                print("Advertencia: no se pudo guardar en JSON:", error)

            print("\nEstado actualizado correctamente. Nuevo estado:", expediente[10])
            return
    print("No se encontro el expediente.")

def ordenar_expedientes():
    print("\n==========================================")
    print("       ORDENAR EXPEDIENTES")
    print("==========================================")
    if len(expedientes) == 0:
        print("No existen expedientes para ordenar.")
        return

    for i in range(len(expedientes)):
        for j in range(i + 1, len(expedientes)):
            p_i = expedientes[i][11]
            p_j = expedientes[j][11]
            n_i = 1 if p_i == "Alta" else (2 if p_i == "Media" else 3)
            n_j = 1 if p_j == "Alta" else (2 if p_j == "Media" else 3)
            if n_i > n_j:
                temporal = expedientes[i]
                expedientes[i] = expedientes[j]
                expedientes[j] = temporal

    try:
        guardar_expedientes_json()
        print("Expedientes ordenados por prioridad (Alta, Media, Baja).")
    except OSError as error:
        print("Advertencia: no se pudo guardar el orden en JSON:", error)

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
            for exp in expedientes:
                archivo.write("====================================\n")
                archivo.write("Codigo: " + exp[0] + "\nDNI: " + exp[1] + "\n")
                archivo.write("Ciudadano: " + exp[2] + " " + exp[3] + "\n")
                archivo.write("Telefono: " + exp[4] + "\nCorreo: " + exp[5] + "\n")
                archivo.write("Tipo: " + exp[6] + "\nDescripcion: " + exp[7] + "\n")
                archivo.write("Sede: " + exp[8] + "\nFecha: " + exp[9] + "\n")
                archivo.write("Estado: " + exp[10] + "\nPrioridad: " + exp[11] + "\n")
                cita_texto = exp[12] if exp[12] != "" else "Sin cita programada"
                archivo.write("Respuesta de cita: " + cita_texto + "\n")
        print("Los expedientes fueron guardados en expedientes_sedapal.txt y JSON.")
    except OSError as error:
        print("No se pudieron guardar los expedientes:", error)

def actualizar_datos_usuario(posicion_usuario):
    """Permite actualizar telefono, correo y contraseña del usuario."""
    usuario = usuarios[posicion_usuario]

    print("\n========================================")
    print("   ACTUALIZAR DATOS DE MI CUENTA")
    print("========================================")

   # Pedimos la contraseña actual.
    clave = input("Ingrese su contraseña actual: ")
   
   # Comprobamos que la contraseña sea correcta.
    if clave != usuario[5]:
           print("Contraseña incorrecta.")
           esperar_continuar()
           return
   
    # Pedimos el nuevo telefono.
    telefono = input("Nuevo telefono (ENTER para mantener el actual): ").strip()
   
    # Si escribio un telefono, revisamos que sea valido.
    if telefono != "":
        while validar_telefono(telefono) == False:
            print("Telefono incorrecto.")
            telefono = input("Ingrese nuevamente el telefono: ").strip()
        usuario[3] = telefono
   
    # Pedimos el nuevo correo.
    correo = input("Nuevo correo (ENTER para mantener el actual): ").strip()
   
    # Si escribio un correo, revisamos que sea valido.
    if correo != "":
        while validar_correo(correo) == False:
            print("Correo incorrecto. Use @gmail.com.")
            correo = input("Ingrese nuevamente el correo: ").strip()
        usuario[4] = correo
   
    # Preguntamos si desea cambiar su contraseña.
    cambiar = input("¿Desea cambiar su contraseña? (S/N): ").strip().upper()
   
    while cambiar != "S" and cambiar != "N":
        cambiar = input("Ingrese S o N: ").strip().upper()
   
    # Si responde S, solicitamos la nueva contraseña.
    if cambiar == "S":
        nueva = input("Nueva contraseña: ")
   
        while nueva == "":
            print("La contraseña no puede estar vacia.")
            nueva = input("Nueva contraseña: ")
   
        # Pedimos confirmar la contraseña.
        confirmar = input("Repita la nueva contraseña: ")
   
        while nueva != confirmar:
               print("Las contraseñas no coinciden.")
               confirmar = input("Repita la nueva contraseña: ")

# ============================================================
# MENUS DEL SISTEMA
# ============================================================

def editar_anular_expediente(posicion_usuario):
    print("\n==========================================")
    print("   EDITAR / ANULAR EXPEDIENTE PENDIENTE")
    print("==========================================")

    dni_usuario = usuarios[posicion_usuario][0]
    es_administrador = usuarios[posicion_usuario][6] == 2
    codigo_buscar = input("Ingrese el codigo del expediente: ").strip().upper()

    expediente_encontrado = None
    for expediente in expedientes:
        if expediente[0].upper() == codigo_buscar:
            if not es_administrador and expediente[1] != dni_usuario:
                print("No tienes permiso para modificar este expediente.")
                esperar_continuar()
                return
            expediente_encontrado = expediente
            break

    if expediente_encontrado is None:
        print("No se encontro el expediente.")
        esperar_continuar()
        return

    if expediente_encontrado[10] != "Pendiente":
        print("\nSolo se pueden editar o anular expedientes en estado Pendiente.")
        print("Estado actual:", expediente_encontrado[10])
        esperar_continuar()
        return

    print("\n1. Editar la descripcion")
    print("2. Anular el expediente")
    print("3. Cancelar")

    opcion = input("Seleccione una opcion: ").strip()
    while opcion not in ["1", "2", "3"]:
        opcion = input("Opcion incorrecta. Seleccione: ").strip()

    if opcion == "3":
        return

    if opcion == "2":
        confirmar = input("Escriba S para confirmar la anulacion: ").strip().upper()
        while confirmar not in ["S", "N"]:
            confirmar = input("Escriba S o N: ").strip().upper()
        if confirmar != "S":
            print("Operacion cancelada.")
            return
        expediente_encontrado[10] = "Anulado"
        guardar_expedientes_json()
        print("\nExpediente anulado correctamente.")
        esperar_continuar()
        return

    nueva_desc = input("Ingrese la nueva descripcion del tramite: ").strip()
    while nueva_desc == "":
        nueva_desc = input("La descripcion no puede estar vacia. Ingrese: ").strip()

    expediente_encontrado[7] = nueva_desc
    guardar_expedientes_json()
    print("\nDescripcion actualizada correctamente.")
    esperar_continuar()

def eliminar_expediente_no_atendido():
    print("\n==========================================")
    print("  ELIMINAR EXPEDIENTE NO ATENDIDO")
    print("  (requiere +10 dias desde la cita)")
    print("==========================================")

    if len(expedientes) == 0:
        print("No existen expedientes registrados.")
        esperar_continuar()
        return

    codigo_buscar = input("Ingrese el codigo del expediente: ").strip().upper()
    expediente_encontrado = None

    for expediente in expedientes:
        if expediente[0].upper() == codigo_buscar:
            expediente_encontrado = expediente
            break

    if expediente_encontrado is None:
        print("Error: el codigo no existe.")
        esperar_continuar()
        return

    if expediente_encontrado[10] == "Atendido":
        print("\nNo se puede eliminar: el expediente ya fue atendido.")
        esperar_continuar()
        return

    fecha_cita_str = extraer_fecha_cita(expediente_encontrado[12])
    if fecha_cita_str is None:
        print("\nNo se puede eliminar: el expediente no tiene cita programada.")
        esperar_continuar()
        return

    dias = dias_desde(fecha_cita_str)
    if dias is None:
        print("\nError: la fecha de la cita registrada no es valida.")
        esperar_continuar()
        return

    print("\nFecha de la cita:", fecha_cita_str, "| Dias transcurridos:", dias)

    if dias <= 10:
        print("\nNo se puede eliminar: aun no han pasado mas de 10 dias desde la cita.")
        esperar_continuar()
        return

    confirmar = input("Escriba S para confirmar la eliminacion permanente: ").strip().upper()
    while confirmar not in ["S", "N"]:
        confirmar = input("Escriba S o N: ").strip().upper()

    if confirmar != "S":
        print("Operacion cancelada.")
        esperar_continuar()
        return

    expedientes.remove(expediente_encontrado)
    guardar_expedientes_json()
    print("\nExpediente eliminado correctamente por inasistencia.")
    esperar_continuar()

def menu_persona_natural(posicion_usuario):
    opcion = ""
    while opcion != "6":
        print("\n========================================")
        print("       MENU - PERSONA NATURAL")
        print("========================================")
        usados = contar_expedientes_usuario(usuarios[posicion_usuario][0])
        disponibles = LIMITE_EXPEDIENTES_PERSONA_NATURAL - usados
        if disponibles < 0: disponibles = 0
        print("Expedientes disponibles:", disponibles, "/", LIMITE_EXPEDIENTES_PERSONA_NATURAL)
        print("1. Registrar/enviar documento")
        print("2. Editar o anular expediente pendiente")
        print("3. Ver mis expedientes activos")
        print("4. Historial de expedientes")
        print("5. Actualizar datos de contacto y contraseña")
        print("6. Cerrar sesion")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1": registrar_expediente(posicion_usuario)
        elif opcion == "2": editar_anular_expediente(posicion_usuario)
        elif opcion == "3": mostrar_expedientes(posicion_usuario, "activo")
        elif opcion == "4": mostrar_expedientes(posicion_usuario, "historial")
        elif opcion == "5": actualizar_datos_usuario(posicion_usuario)
        elif opcion == "6": print("Sesion cerrada.")
        else: print("Opcion incorrecta.")
        
def menu_administrador(posicion_usuario):
    opcion = ""
    while opcion != "12":
        print("\n========================================")
        print("         MENU - ADMINISTRADOR")
        print("========================================")
        print("1. Registrar expediente")
        print("2. Mostrar todos los expedientes")
        print("3. Buscar expediente")
        print("4. Actualizar estado")
        print("5. Editar o anular expediente pendiente")
        print("6. Eliminar expediente no atendido")
        print("7. Registrar respuesta por correo de cita")
        print("8. Ordenar por prioridad")
        print("9. Guardar expedientes en archivo")
        print("10. Agregar DNI a base JSON")
        print("11. Generar reporte estadistico")
        print("12. Cerrar sesion")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1": registrar_expediente(posicion_usuario)
        elif opcion == "2": mostrar_expedientes(posicion_usuario)
        elif opcion == "3": buscar_expediente(posicion_usuario)
        elif opcion == "4": actualizar_estado()
        elif opcion == "5": editar_anular_expediente(posicion_usuario)
        elif opcion == "6": eliminar_expediente_no_atendido()
        elif opcion == "7": registrar_respuesta_cita()
        elif opcion == "8": ordenar_expedientes()
        elif opcion == "9": guardar_archivo()
        elif opcion == "10": registrar_dni_simulado()
        elif opcion == "11": generar_reporte_estadistico()
        elif opcion == "12": print("Sesion cerrada.")
        else: print("Opcion incorrecta.")

# ============================================================
# RECUPERACION DE CONTRASEÑA (RELACION DE BASES DE DATOS)
# ============================================================
def buscar_posicion_usuario(dni):
    """Devuelve la posicion del usuario en la lista, o -1 si no existe."""
    for i in range(len(usuarios)):
        if usuarios[i][0] == dni:
            return i
    return -1

def recuperar_contrasena():
    print("\n========================================")
    print("       RECUPERAR CONTRASEÑA")
    print("========================================")
    
    dni = input("Ingrese su DNI: ").strip()

    if validar_dni(dni) == False:
        print("El DNI debe tener exactamente 8 numeros.")
        esperar_continuar()
        return

    # ---- Paso 1: el DNI debe existir en la base de USUARIOS ----
    posicion = buscar_posicion_usuario(dni)

    if posicion == -1:
        print("No existe una cuenta registrada con ese DNI.")
        esperar_continuar()
        return

    usuario_actual = usuarios[posicion]

    # ---- Paso 2: el DNI debe existir tambien en la base de DNI ----
    registro_dni = buscar_registro_dni(dni)

    if registro_dni is None:
        print("\nEl DNI no esta registrado en la base RENIEC simulada.")
        print("No es posible vincular la cuenta con la base de identidad.")
        print("Comuniquese con el administrador del sistema.")
        esperar_continuar()
        return

    # ---- Paso 3: integridad referencial (nombres deben coincidir) ----
    if (usuario_actual[1].strip().lower() != registro_dni["nombres"].strip().lower()
            or usuario_actual[2].strip().lower() != registro_dni["apellidos"].strip().lower()):
        print("\nLos datos de la cuenta no coinciden con la base de identidad.")
        print("Comuniquese con el administrador para regularizar su registro.")
        esperar_continuar()
        return

    print("\nDNI encontrado y vinculado con la base de identidad.")
    print("Ciudadano:", registro_dni["nombres"], registro_dni["apellidos"])

    # ---- Paso 4: Factor 1 - Digito verificador (base_DNI) ----
    digito = input("\nFactor 1 - Ingrese su digito verificador: ").strip()

    if digito != registro_dni["numero_verificador"]:
        print("Digito verificador incorrecto. No se puede continuar.")
        esperar_continuar()
        return

    print("Digito verificador correcto.")

    # ---- Paso 5: Factor 2 - Correo o telefono (base_usuarios) ----
    if usuario_actual[4].strip() != "":
        correo = input("Factor 2 - Ingrese su correo electronico registrado: ").strip().lower()
        if correo != usuario_actual[4].strip().lower():
            print("Correo electronico incorrecto. No se puede continuar.")
            esperar_continuar()
            return
        print("Correo electronico correcto.")

    elif usuario_actual[3].strip() != "":
        telefono = input("Factor 2 - Ingrese su telefono registrado: ").strip()
        if telefono != usuario_actual[3].strip():
            print("Telefono incorrecto. No se puede continuar.")
            esperar_continuar()
            return
        print("Telefono correcto.")

    else:
        print("\nSu cuenta no tiene correo ni telefono registrado.")
        print("No es posible completar la verificacion doble.")
        print("Comuniquese con el administrador del sistema.")
        esperar_continuar()
        return

    # ---- Paso 6: cambio de contraseña ----
    print("\nIdentidad verificada con doble factor.")
    print("========================================")

    nueva_clave = input("Ingrese su nueva contraseña: ")
    while nueva_clave == "":
        print("La contraseña no puede estar vacia.")
        nueva_clave = input("Ingrese su nueva contraseña: ")

    confirmar_clave = input("Confirme su nueva contraseña: ")

    if nueva_clave != confirmar_clave:
        print("Las contraseñas no coinciden. No se realizo ningun cambio.")
        esperar_continuar()
        return

    usuarios[posicion][5] = nueva_clave

    # ---- Paso 7: persistencia ----
    try:
        guardar_usuarios_json()
    except OSError as error:
        print("Advertencia: la contraseña cambio en memoria, pero no se pudo guardar en JSON:", error)
        esperar_continuar()
        return

    print("\nContraseña actualizada correctamente.")
    print("Ya puede iniciar sesion con su nueva contraseña.")
    esperar_continuar()

# ============================================================
# MENU INICIAL
# ============================================================
def menu_inicial():
    opcion = ""
    while opcion != "4":
        print("\n========================================")
        print("    SEDAPAL - MESA DE PARTES DIGITAL")
        print("       SEDE SAN JUAN DE LURIGANCHO")
        print("========================================")
        print("1. Iniciar sesion")
        print("2. Crear nuevo usuario")
        print("3. Recuperar contraseña")
        print("4. Salir")
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
            recuperar_contrasena()
        elif opcion == "4":
            print("Gracias por utilizar el sistema.")
        else:
            print("Opcion incorrecta. Intente nuevamente.")

# ============================================================
# INICIO DEL PROGRAMA
# ============================================================
if __name__ == "__main__":
    menu_inicial()