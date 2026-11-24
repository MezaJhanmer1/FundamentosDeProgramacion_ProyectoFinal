
# Manejar el almacenamiento en disco y mantener las listas en memoria.

# =======================================
# CARGAR EXPEDIENTES
# =======================================

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


# =======================================
# GUARDAR EXPEDIENTES
# =======================================

def guardar_expedientes_json():
    """Guarda todos los expedientes en el archivo JSON."""
    with open(EXPEDIENTES_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(expedientes, archivo, ensure_ascii=False, indent=4)


# Cargamos los expedientes guardados al iniciar el programa.
expedientes = cargar_expedientes()

# =======================================
# CARGAR BASE DNI
# =======================================

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

# =======================================
# GUARDAR BASE DNI
# =======================================

def guardar_base_dni(datos):
    """Guarda los registros de DNI en el archivo JSON."""
    with open(BASE_DNI_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

# =======================================
# CARGAR USUARIOS
# =======================================

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

# =======================================
# GUARDAR USUARIOS
# =======================================

def guardar_usuarios_json():
    """Guarda todos los usuarios en el archivo JSON."""
    with open(USUARIOS_ARCHIVO, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, ensure_ascii=False, indent=4)

# =======================================
# GUARDAR ARCHIVC EXPEDIENTES
# =======================================


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
