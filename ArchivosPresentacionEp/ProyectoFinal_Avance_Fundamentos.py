# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL v 0.1.2
# ============================================================
# Este programa permite registrar y consultar expedientes
# de los usuarios de SEDAPAL - San Juan de Lurigancho.
# Version de proyecto Ver 0.1.2
# ============================================================

# ------------------------------------------------------------
# LISTA PRINCIPAL DE EXPEDIENTES
# ------------------------------------------------------------
# Esta lista almacenará todos los expedientes registrados, Cada expediente será una lista con sus datos.
# Por ahora no utilizamos una base de datos.
from builtins import len


expedientes = []


# ============================================================
# CONFIGURACION: LIMITE DE EXPEDIENTES POR USUARIO
# ============================================================
LIMITE_EXPEDIENTES_PERSONA_NATURAL = 5     # personas naturales
LIMITE_EXPEDIENTES_ADMINISTRADOR   = 50    # administradores

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

reniec_digitos = [
    "9", "7", "8", "9", "0",
    "1", "1", "2", "3", "4",
    "0", "4", "1", "9", "6",
    "3", "1", "8", "5", "3",
    "1", "5", "2", "0", "7",
    "4", "1", "9", "7", "4"
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

#Agregamos una nueva estructura donde se almacenaran los usuarios nuevos
usuarios = [
    ["60549429", "Jhanmer", "Meza", "", "", "admin123", 2, 0],
    ["12345678", "Carlos", "Ramirez", "", "", "admin456", 2, 0]
]
# ============================================================
# FUNCION PARA VALIDAR TEXTO CON LETRAS Y ESPACIOS
# ============================================================

def texto_valido(texto):
        texto_limpio = texto.strip()
    
        if texto_limpio == "":          # Si el usuario no escribió nada, no es válido
         return False
        
    # Definimos nuestra lista de caracteres aprobados
        permitidas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "
    
        for letra in texto:
            if letra not in permitidas:
                return False  # Si encuentra un número o símbolo, frena y dice: "No es válido"
            
        return True  # Si el ciclo termina y todo estuvo bien, dice: "Sí es válido"

# ============================================================
# FUNCIÓN PARA VALIDAR EL DNI
# ============================================================
def validar_dni(dni):

    # Verificamos que el DNI tenga exactamente 8 caracteres
    if len(dni) != 8:
        return False

    # Verificamos que todos los caracteres sean números
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
# FUNCION PARA VALIDAR CORREO ELECTRONICO
# ============================================================
def validar_correo(email):
    
    email_limpio = email.strip().lower()        #quita espacios + minusculas
    caracteres_prohibidos = " ,()[]{}!¡¿?/*;:<>=#$"     # --- FILTRO DE CARACTERES PROHIBIDOS ---
    
    for caracter in email_limpio:
        if caracter in caracteres_prohibidos:
            return False # Si encuentra un carácter prohibido, el correo es inválido

    if "@" in email_limpio:
        partes = email_limpio.split("@")        # corta en 2 partes (usuario + @ + dominio) ["juan.perez", "gmail.com"]
        usuario = partes[0]                     # pedimos q guarde el 1er elemento [0]
        dominio = partes[1]                     # pedimos q guarde el 2do elemento [1]

        
        if usuario != "" and dominio == "gmail.com":       # el DOMINIO tenga un punto (para el .com, .net, etc.) y que el dominio sea exactamente gmail.com
            
            return True
        
    return False


# ============================================================
# FUNCION PARA VALIDAR TELEFONO
# ============================================================
def validar_telefono(telefono):
    telefono = telefono.strip()

    # Evitar campos vacios.
    if telefono == "":
        return False

    # Verificar que solamente tenga numeros.
    for numero in telefono:
        if numero not in "0123456789":
            return False

    longitud = len(telefono)
    primer_digito = telefono[0]

    # Celular peruano: empieza con 9 y tiene 9 digitos.
    if primer_digito == "9" and longitud == 9:
        return True

    # Telefono fijo de Lima y Callao: empieza con 1 y tiene 7 digitos.
    elif primer_digito == "1" and longitud == 7:
        return True

    # Telefono fijo de otras regiones: empieza entre 2 y 8 y tiene 6 digitos.
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
        print("Correo electronico incorrecto.")
        correo = input("Ingrese nuevamente su correo: ").strip()

    return correo


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

    # Evitamos crear dos cuentas con el mismo DNI.
    for i in range(len(usuarios_dni)):
        if usuarios_dni[i] == dni:
            print("Este DNI ya tiene una cuenta en el sistema.")
            return

    # Verificamos el digito solamente al crear un usuario.
    if verificar_digito_verificador(dni) == False:
        print("No se puede completar el registro.")
        return

    # Buscamos el DNI en nuestra lista simulada.
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

    # Guardamos los datos en la misma posicion de cada lista.
    usuarios_dni.append(dni)
    usuarios_nombres.append(nombre)
    usuarios_apellidos.append(apellidos)
    usuarios_telefono.append(telefono)
    usuarios_correo.append(correo)
    usuarios_claves.append(clave)
    usuarios_perfiles.append(1)

    # Agregar los nuevos usuario a la nueva estructura creada
    usuarios.append([dni, nombre, apellidos, telefono, correo, clave, 1, 0])

    print("\nUsuario registrado correctamente.")
    print("Tu perfil es: Persona natural.")
    print("Ya puedes iniciar sesion.")


# ============================================================
# FUNCION PARA INICIAR SESION
# Aca validamos las credenciales del usuario en el inicio de sesion
# ============================================================
def iniciar_sesion():
    print("\n--- INICIAR SESION ---")

    dni = input("Ingrese su DNI: ").strip()
    
    if validar_dni(dni) == False:
        print("DNI incorrecto. Debe tener exactamente 8 numeros.")
        return -1
    
    # Verificamos el digito solamente al iniciar sesion.
    if verificar_digito_verificador(dni) == False:
      return -1

    clave = input("Ingrese su contraseña: ")

    for i in range(len(usuarios)):

        if usuarios[i][0] == dni:

            if usuarios[i][5] == clave:

                print("\nBienvenido:", usuarios[i][1], usuarios[i][2])

                return i

            else:
                print("\nContraseña incorrecta.")
                return -1

    print("\nUsuario no encontrado.")
    return -1

# ------------------------------------------------------------
# FUNCIÓN PARA REGISTRAR UN EXPEDIENTE
# ------------------------------------------------------------
def registrar_expediente(posicion_usuario):
    print("\n========================================")
    print("          REGISTRO DE EXPEDIENTE")
    print("========================================")

    # Verificamos el limite antes de continuar
    if not puede_registrar_expediente(posicion_usuario):
        return

    codigo = generar_codigo()
    print("Codigo del expediente:", codigo)

    # PERFIL PERSONA NATURAL: recuperar automaticamente los datos
    # guardados cuando se creo la cuenta. No se solicitan nuevamente.
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

# PERFIL ADMINISTRADOR: se conserva el registro manual original.
    else:
        dni = input("Ingrese el DNI del ciudadano: ").strip()
        while validar_dni(dni) == False:
            print("Error: el DNI debe tener exactamente 8 numeros.")
            dni = input("Ingrese nuevamente el DNI: ").strip()

        nombre, apellidos = consultar_reniec(dni)

        while nombre == "":
            print("DNI no encontrado en la lista simulada.")
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
    if usuarios[posicion_usuario][6] == 1:
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


# ------------------------------------------------------------
# FUNCIÓN PARA MOSTRAR TODOS LOS EXPEDIENTES
# ------------------------------------------------------------
def mostrar_expedientes(posicion_usuario):
    print("\n========================================")
    print("             EXPEDIENTES")
    print("========================================")

    encontrados = 0

    for expediente in expedientes:
       if usuarios[posicion_usuario][6] == 2 or expediente[1] == usuarios[posicion_usuario][0]:
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

# ------------------------------------------------------------
# FUNCIÓN PARA BUSCAR UN EXPEDIENTE
# ------------------------------------------------------------
def buscar_expediente(posicion_usuario):

    print("\n==========================================")
    print("        BUSCAR EXPEDIENTE")
    print("==========================================")
    codigo_buscar = input("Ingrese el código del expediente: ").strip()
    encontrado = False

    for expediente in expedientes:
        if expediente[0] == codigo_buscar:
            # La persona natural solo puede consultar sus propios expedientes.
            if usuarios[posicion_usuario][6] == 1 and expediente[1] != usuarios[posicion_usuario][0]:
                continue

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
            print("Prioridad:", expediente[11])
            encontrado = True

    # Si después de recorrer la lista no encontramos
    # el expediente, mostramos un mensaje.
    if encontrado == False:
        print("No se encontro el expediente o no tienes permiso para verlo.")


# ------------------------------------------------------------
# FUNCIÓN PARA ACTUALIZAR EL ESTADO (SOLO ADMINISTRADOR)
# ------------------------------------------------------------
def actualizar_estado():

    print("\n==========================================")
    print("       ACTUALIZAR ESTADO")
    print("==========================================")
    codigo_buscar = input("Ingrese el código del expediente: ").strip()

    encontrado = False

    # Buscamos el expediente
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

            print("\nEstado actualizado correctamente.")
            print("Código:", expediente[0])
            print("Nuevo estado:", expediente[10])

    if encontrado == False:
        print("No se encontró el expediente.")


# ============================================================
# FUNCION PARA ORDENAR POR PRIORIDAD CON CICLOS FOR
# Alta primero, luego Media y finalmente Baja.
# ============================================================
def ordenar_expedientes():

    print("\n==========================================")
    print("       ORDENAR EXPEDIENTES")
    print("==========================================")

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


# ------------------------------------------------------------
# FUNCIÓN PARA GUARDAR LOS EXPEDIENTES EN UN ARCHIVO DE TEXTO
# ------------------------------------------------------------
def guardar_archivo():

    print("\n==========================================")
    print("       GUARDAR EXPEDIENTES")
    print("==========================================")

    # Verificamos que existan expedientes
    if len(expedientes) == 0:
        print("No existen expedientes para guardar.")
        return
        # Abrimos un archivo de texto.
        # La letra "w" significa escribir.
    archivo = open("expedientes_sedapal.txt", "w", encoding="utf-8")
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
        archivo.write("Prioridad: " + expediente[11] + "\n")

        # Cerramos el archivo
    archivo.close()

    print("Los expedientes fueron guardados correctamente.")
    print("Archivo: expedientes_sedapal.txt")


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
# VERIFICACION DEL DNI CON DIGITO VERIFICADOR
# ============================================================
def verificar_digito_verificador(dni):
    # Si el DNI esta en nuestra lista simulada, comprobamos su digito.
    if dni in reniec_dni:
        posicion = reniec_dni.index(dni)
        digito = input("Ingrese digito verificador: ").strip()

        if digito == reniec_digitos[posicion]:
            print("DNI verificado correctamente.")
            return True
        else:
            print("Digito verificador incorrecto.")
            return False

    # Si no esta en la lista simulada, se deja continuar.
    return True


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================
menu_inicial()