from datetime import datetime ,date
# ============================================================
# FUNCIONES DE VALIDACION
# ============================================================
#validacion de textro 
def texto_valido(texto):
    texto_limpio = texto.strip()
    if texto_limpio == "": return False
    permitidas = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑ "
    for letra in texto_limpio:
        if letra not in permitidas: return False
    return True
#validacion de DNI
def validar_dni(dni):
    if len(dni) != 8: return False
    for caracter in dni:
        if caracter < "0" or caracter > "9": return False
    return True

#Validacion De Fecha
def validar_fecha(fecha):
    partes = fecha.split("/")
    if len(partes) != 3: return False

    dia_texto, mes_texto, anio_texto = partes

    if len(dia_texto) != 2 or len(mes_texto) != 2 or len(anio_texto) != 4:
        return False

    if not (dia_texto.isdigit() and mes_texto.isdigit() and anio_texto.isdigit()):
        return False

    dia = int(dia_texto)
    mes = int(mes_texto)
    anio = int(anio_texto)

    if anio < 1900 or anio > 2100: return False
    if mes < 1 or mes > 12: return False

    if mes in [4, 6, 9, 11]:
        maximo_dias = 30
    elif mes == 2:
        maximo_dias = 29 if (anio % 400 == 0 or (anio % 4 == 0 and anio % 100 != 0)) else 28
    else:
        maximo_dias = 31

    return 1 <= dia <= maximo_dias
#Validacion de fecha de emision de DNI
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
#validacion dias 
def dias_desde(fecha_texto):
    try:
        fecha = datetime.strptime(fecha_texto, "%d/%m/%Y")
        return (date.today() - fecha.date()).days
    except (ValueError, TypeError): return None
#extraccion de fecha de citas
def extraer_fecha_cita(respuesta_cita):
    if not respuesta_cita or not respuesta_cita.startswith("Fecha: "): return None
    resto = respuesta_cita[len("Fecha: "):]
    fecha = resto.split("|")[0].strip()
    return fecha if fecha != "" else None
#validacion de correos
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
#validacion de numero de telefono
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
#solicitud de telefono
def solicitar_telefono():
    telefono = input("Ingrese su telefono/celular: ").strip()
    while validar_telefono(telefono) == False:
        print("Telefono incorrecto. Verifique la cantidad de digitos.")
        telefono = input("Ingrese nuevamente su telefono: ").strip()
    return telefono
#solicitud de correo
def solicitar_correo():
    correo = input("Ingrese su correo electronico: ").strip()
    while validar_correo(correo) == False:
        print("Correo electronico incorrecto. Use una cuenta @gmail.com.")
        correo = input("Ingrese nuevamente su correo: ").strip()
    return correo
