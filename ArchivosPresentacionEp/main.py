
# ============================================================
# SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL
# ARCHIVO PRINCIPAL
# ============================================================

# ------------------------------------------------------------
# IMPORTACION DE MODULOS
# ------------------------------------------------------------

from config import LIMITE_EXPEDIENTES_PERSONA_NATURAL

from almacenamiento import usuarios

from usuarios import (
    registrar_usuario,
    iniciar_sesion,
    recuperar_contrasena,
    actualizar_datos_usuario,
    registrar_dni_simulado
)

from expedientes import (
    registrar_expediente,
    contar_expedientes_usuario,
    mostrar_expedientes,
    buscar_expediente,
    actualizar_estado,
    editar_anular_expediente,
    eliminar_expediente_no_atendido,
    registrar_respuesta_cita,
    ordenar_expedientes,
    guardar_archivo,
    generar_reporte_estadistico
)


# ============================================================
# MENU - PERSONA NATURAL
# ============================================================

def menu_persona_natural(posicion_usuario):

    opcion = ""

    while opcion != "6":

        print("\n========================================")
        print("       MENU - PERSONA NATURAL")
        print("========================================")

        usados = contar_expedientes_usuario(usuarios[posicion_usuario][0])
        disponibles = LIMITE_EXPEDIENTES_PERSONA_NATURAL - usados

        if disponibles < 0:
            disponibles = 0

        print("Expedientes disponibles:", disponibles, "/", LIMITE_EXPEDIENTES_PERSONA_NATURAL)

        print("\n1. Registrar/enviar documento")
        print("2. Editar o anular expediente pendiente")
        print("3. Ver mis expedientes activos")
        print("4. Historial de expedientes")
        print("5. Actualizar datos de contacto y contraseña")
        print("6. Cerrar sesion")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            registrar_expediente(posicion_usuario)

        elif opcion == "2":
            editar_anular_expediente(posicion_usuario)

        elif opcion == "3":
            mostrar_expedientes(posicion_usuario, "activo")

        elif opcion == "4":
            mostrar_expedientes(posicion_usuario, "historial")

        elif opcion == "5":
            actualizar_datos_usuario(posicion_usuario)

        elif opcion == "6":
            print("\nSesion cerrada.")

        else:
            print("\nOpcion incorrecta. Intente nuevamente.")


# ============================================================
# MENU - ADMINISTRADOR
# ============================================================

def menu_administrador(posicion_usuario):

    opcion = ""

    while opcion != "12":

        print("\n========================================")
        print("         MENU - ADMINISTRADOR")
        print("========================================")

        print("\n1. Registrar expediente")
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

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            registrar_expediente(posicion_usuario)

        elif opcion == "2":
            mostrar_expedientes(posicion_usuario)

        elif opcion == "3":
            buscar_expediente(posicion_usuario)

        elif opcion == "4":
            actualizar_estado()

        elif opcion == "5":
            editar_anular_expediente(posicion_usuario)

        elif opcion == "6":
            eliminar_expediente_no_atendido()

        elif opcion == "7":
            registrar_respuesta_cita()

        elif opcion == "8":
            ordenar_expedientes()

        elif opcion == "9":
            guardar_archivo()

        elif opcion == "10":
            registrar_dni_simulado()

        elif opcion == "11":
            generar_reporte_estadistico()

        elif opcion == "12":
            print("\nSesion cerrada.")

        else:
            print("\nOpcion incorrecta. Intente nuevamente.")


# ============================================================
# MENU INICIAL DEL SISTEMA
# ============================================================

def menu_inicial():

    opcion = ""

    while opcion != "4":

        print("\n========================================")
        print("    SEDAPAL - MESA DE PARTES DIGITAL")
        print("       SEDE SAN JUAN DE LURIGANCHO")
        print("========================================")

        print("\n1. Iniciar sesion")
        print("2. Crear nuevo usuario")
        print("3. Recuperar contraseña")
        print("4. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

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
            print("\nGracias por utilizar el sistema.")

        else:
            print("\nOpcion incorrecta. Intente nuevamente.")


# ============================================================
# INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    menu_inicial()
