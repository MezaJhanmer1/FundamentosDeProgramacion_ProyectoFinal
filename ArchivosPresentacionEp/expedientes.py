# expedientes.py
# Módulo de gestión de expedientes

# ------------------------------------------------------------
# GENERAR_CODIGO
# GENERA EL SIGUIENTE CÓDIGO DE EXPEDIENTE ÚNICO (EJ. SED-0001).
# ------------------------------------------------------------
def generar_codigo():
    """Genera el siguiente código secuencial de expediente."""
    max_numero = 0
    for expediente in expedientes:
        codigo = expediente[0]
        if codigo.startswith("SED-"):
            parte = codigo[4:]
            if parte.isdigit():
                numero = int(parte)
                if numero > max_numero: max_numero = numero
    return "SED-" + str(max_numero + 1).zfill(4)

# ------------------------------------------------------------
# CONTAR_EXPEDIENTES_USUARIO
# CUENTA CUÁNTOS EXPEDIENTES ACTIVOS (NO ANULADOS) TIENE UN DNI.
# ------------------------------------------------------------
def contar_expedientes_usuario(dni):
    """Cuenta los expedientes de un usuario, excluyendo los anulados."""
    contador = 0
    for expediente in expedientes:
        if expediente[1] == dni and expediente[10] != "Anulado":
            contador += 1
    return contador

# ------------------------------------------------------------
# OBTENER_LIMITE_USUARIO
# RETORNA EL LÍMITE DE EXPEDIENTES SEGÚN EL PERFIL.
# ------------------------------------------------------------
def obtener_limite_usuario(posicion_usuario):
    """Devuelve el límite de expedientes permitidos según el perfil."""
    if usuarios[posicion_usuario][6] == 2:
        return LIMITE_EXPEDIENTES_ADMINISTRADOR
    return LIMITE_EXPEDIENTES_PERSONA_NATURAL

# ------------------------------------------------------------
# PUEDE_REGISTRAR_EXPEDIENTE
# VERIFICA SI EL USUARIO AÚN NO ALCANZÓ SU LÍMITE.
# ------------------------------------------------------------
def puede_registrar_expediente(posicion_usuario):
    """Valida si el usuario tiene cupo disponible para registrar un expediente."""
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
# REGISTRO DE EXPEDIENTES Y CONSULTAS
# ============================================================

# ------------------------------------------------------------
# REGISTRAR_EXPEDIENTE
# SOLICITA LOS DATOS Y GUARDA UN NUEVO TRÁMITE.
# ------------------------------------------------------------
def registrar_expediente(posicion_usuario):
    """Registra un nuevo expediente en el sistema."""
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

# ------------------------------------------------------------
# PUEDE_CONSULTAR
# CONTROLA EL LÍMITE DE CONSULTAS (3 MÁXIMO PARA PERSONAS).
# ------------------------------------------------------------
def puede_consultar(posicion_usuario):
    """Verifica si el usuario tiene permitido realizar otra consulta."""
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

# ------------------------------------------------------------
# MOSTRAR_EXPEDIENTES
# IMPRIME EN PANTALLA LOS EXPEDIENTES (ACTIVOS O HISTORIAL).
# ------------------------------------------------------------
def mostrar_expedientes(posicion_usuario, estado=None):
    """Muestra los expedientes del usuario o de todos si es administrador."""
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

# ------------------------------------------------------------
# GENERAR_REPORTE_ESTADISTICO
# MUESTRA UN RESUMEN CON TOTALES POR ESTADO, PRIORIDAD Y TIPO.
# ------------------------------------------------------------
def generar_reporte_estadistico():
    """Calcula y muestra las estadísticas generales de los expedientes."""
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

# ------------------------------------------------------------
# BUSCAR_EXPEDIENTE
# BUSCA UN EXPEDIENTE POR DNI O POR SU CÓDIGO ÚNICO.
# ------------------------------------------------------------
def buscar_expediente(posicion_usuario):
    """Permite buscar un expediente ingresando el DNI o el código."""
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

# ------------------------------------------------------------
# REGISTRAR_RESPUESTA_CITA
# REGISTRA LA FECHA DE UNA CITA Y SIMULA EL ENVÍO DE CORREO.
# ------------------------------------------------------------
def registrar_respuesta_cita():
    """Registra los detalles de una cita y actualiza el estado del expediente."""
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

    hoy = datetime.now().date()
    while True:
        fecha_cita = input("\nIngrese la fecha de la cita (DD/MM/AAAA): ").strip()
        if not validar_fecha(fecha_cita):
            print("Formato o fecha invalida. Use DD/MM/AAAA.")
            continue
        if datetime.strptime(fecha_cita, "%d/%m/%Y").date() <= hoy:
            print("La fecha de la cita debe ser mayor a la fecha actual (" + hoy.strftime("%d/%m/%Y") + ").")
            continue
        break

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

# ------------------------------------------------------------
# ACTUALIZAR_ESTADO
# CAMBIA EL ESTADO DE UN EXPEDIENTE (PENDIENTE, EN PROCESO, ATENDIDO).
# ------------------------------------------------------------
def actualizar_estado():
    """Permite modificar el estado de un expediente existente."""
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

# ------------------------------------------------------------
# ORDENAR_EXPEDIENTES
# ORDENA LA LISTA DE EXPEDIENTES POR PRIORIDAD (ALTA -> BAJA).
# ------------------------------------------------------------
def ordenar_expedientes():
    """Ordena los expedientes por prioridad usando el método de burbuja."""
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


# ============================================================
# EDICIÓN, ANULACIÓN Y ELIMINACIÓN
# ============================================================

# ------------------------------------------------------------
# EDITAR_ANULAR_EXPEDIENTE
# PERMITE CAMBIAR LA DESCRIPCIÓN O ANULAR UN TRÁMITE PENDIENTE.
# ------------------------------------------------------------
def editar_anular_expediente(posicion_usuario):
    """Edita la descripción o anula un expediente en estado Pendiente."""
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

# ------------------------------------------------------------
# ELIMINAR_EXPEDIENTE_NO_ATENDIDO
# BORRA UN EXPEDIENTE SI PASARON MÁS DE 10 DÍAS DESDE LA CITA.
# ------------------------------------------------------------
def eliminar_expediente_no_atendido():
    """Elimina un expediente por inasistencia (más de 10 días desde la cita)."""
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