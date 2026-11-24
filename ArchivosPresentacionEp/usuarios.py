
# USUARIOS.PY -  Gestionar cuentas, RENIEC simulada y funciones de seguridad.

# =======================================
# BUSCAR REGISTRO DNI
# =======================================

def buscar_registro_dni(dni):
    """Busca y devuelve el registro completo de un DNI."""
    for registro in base_dni:
        if registro["dni"] == dni:
            return registro
    return None


# ============================================================
# FUNCIONES DE RENIEC SIMULACION
# ============================================================

# =======================================
# CONSULTAR RENIEC
# =======================================

def consultar_reniec(dni):
    registro = buscar_registro_dni(dni)
    if registro is not None:
        return registro["nombres"], registro["apellidos"]
    return "", ""

# =======================================
# VERIFICAR DIGITO VERIFICADOR DNI
# =======================================

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

# =======================================
# REGISTRAR DNI SIMULACION
# =======================================

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


# =======================================
# REGISTRO DE USUARIOS
# =======================================
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

# =======================================
# INICIAR SESION DE USUARIOS
# =======================================

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

# =======================================
# ACTUALIZAR DATOS DE USUARIOS
# =======================================

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

        usuario[5] = nueva

    try:
        guardar_usuarios_json()
        print("\nDatos actualizados y guardados correctamente.")
    except OSError as error:
        print("Advertencia: los datos cambiaron en memoria, pero no se guardaron en JSON:", error)

    esperar_continuar()

# ============================================================
# RECUPERACION DE CONTRASEÑA (RELACION DE BASES DE DATOS)
# ============================================================
def buscar_posicion_usuario(dni):
    """Devuelve la posicion del usuario en la lista, o -1 si no existe."""
    for i in range(len(usuarios)):
        if usuarios[i][0] == dni:
            return i
    return -1

# =======================================
# RECUPERAR CONTRASEÑAS
# =======================================

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

