Algoritmo MesaPartesDigital_SEDAPAL
    Definir opcion, opcionAdmin, totalUsuarios, totalExpedientes Como Entero
    Definir i, posUsuario Como Entero
    Definir dni, clave, nombre, apellido, descripcion, estado, codigo Como Cadena
    Definir usuariosDni, usuariosClave, usuariosNombre, usuariosApellido Como Cadena
    Definir expedientesCodigo, expedientesDni, expedientesNombre, expedientesDescripcion, expedientesEstado Como Cadena
    Definir encontrado Como Logico

    Dimension usuariosDni[50]
    Dimension usuariosClave[50]
    Dimension usuariosNombre[50]
    Dimension usuariosApellido[50]
    Dimension expedientesCodigo[100]
    Dimension expedientesDni[100]
    Dimension expedientesNombre[100]
    Dimension expedientesDescripcion[100]
    Dimension expedientesEstado[100]

    totalUsuarios <- 2
    usuariosDni[1] <- "60549429"
    usuariosClave[1] <- "admin123"
    usuariosNombre[1] <- "Administrador"
    usuariosApellido[1] <- "SEDAPAL"
    usuariosDni[2] <- "12345678"
    usuariosClave[2] <- "admin456"
    usuariosNombre[2] <- "Carlos"
    usuariosApellido[2] <- "Ramirez"
    totalExpedientes <- 0
    opcion <- 0

    Mientras opcion <> 3 Hacer
        Escribir ""
        Escribir "======================================"
        Escribir " SEDAPAL - MESA DE PARTES DIGITAL"
        Escribir "======================================"
        Escribir "1. Iniciar sesion"
        Escribir "2. Registrar usuario"
        Escribir "3. Salir"
        Escribir "Seleccione una opcion:"
        Leer opcion

        Si opcion = 1 Entonces
            Escribir "Ingrese DNI:"
            Leer dni
            Escribir "Ingrese clave:"
            Leer clave
            posUsuario <- 0
            Para i <- 1 Hasta totalUsuarios Hacer
                Si usuariosDni[i] = dni Y usuariosClave[i] = clave Entonces
                    posUsuario <- i
                FinSi
            FinPara

            Si posUsuario = 0 Entonces
                Escribir "DNI o clave incorrectos."
            SiNo
                Escribir "Bienvenido/a ", usuariosNombre[posUsuario], " ", usuariosApellido[posUsuario]
                opcionAdmin <- 0
                Mientras opcionAdmin <> 4 Hacer
                    Escribir ""
                    Escribir "========= MENU DE EXPEDIENTES ========="
                    Escribir "1. Registrar expediente"
                    Escribir "2. Mostrar expedientes"
                    Escribir "3. Buscar expediente por codigo"
                    Escribir "4. Cerrar sesion"
                    Leer opcionAdmin

                    Si opcionAdmin = 1 Entonces
                        Si totalExpedientes < 100 Entonces
                            totalExpedientes <- totalExpedientes + 1
                            codigo <- Concatenar("SED-", ConvertirATexto(totalExpedientes))
                            expedientesCodigo[totalExpedientes] <- codigo
                            Escribir "Ingrese DNI del ciudadano:"
                            Leer expedientesDni[totalExpedientes]
                            Escribir "Ingrese nombre del ciudadano:"
                            Leer expedientesNombre[totalExpedientes]
                            Escribir "Describa el tramite:"
                            Leer expedientesDescripcion[totalExpedientes]
                            expedientesEstado[totalExpedientes] <- "Recibido"
                            Escribir "Expediente registrado. Codigo: ", codigo
                        SiNo
                            Escribir "Se alcanzo el limite de expedientes."
                        FinSi
                    SiNo
                        Si opcionAdmin = 2 Entonces
                            Si totalExpedientes = 0 Entonces
                                Escribir "No hay expedientes registrados."
                            SiNo
                                Para i <- 1 Hasta totalExpedientes Hacer
                                    Escribir "Codigo: ", expedientesCodigo[i]
                                    Escribir "DNI: ", expedientesDni[i]
                                    Escribir "Ciudadano: ", expedientesNombre[i]
                                    Escribir "Descripcion: ", expedientesDescripcion[i]
                                    Escribir "Estado: ", expedientesEstado[i]
                                    Escribir "-----------------------------"
                                FinPara
                            FinSi
                        SiNo
                            Si opcionAdmin = 3 Entonces
                                Escribir "Ingrese el codigo a buscar (ejemplo SED-1):"
                                Leer codigo
                                encontrado <- Falso
                                Para i <- 1 Hasta totalExpedientes Hacer
                                    Si expedientesCodigo[i] = codigo Entonces
                                        encontrado <- Verdadero
                                        Escribir "Codigo: ", expedientesCodigo[i]
                                        Escribir "Ciudadano: ", expedientesNombre[i]
                                        Escribir "Descripcion: ", expedientesDescripcion[i]
                                        Escribir "Estado: ", expedientesEstado[i]
                                    FinSi
                                FinPara
                                Si encontrado = Falso Entonces
                                    Escribir "No se encontro el expediente."
                                FinSi
                            SiNo
                                Si opcionAdmin <> 4 Entonces
                                    Escribir "Opcion no valida."
                                FinSi
                            FinSi
                        FinSi
                    FinSi
                FinMientras
            FinSi
        SiNo
            Si opcion = 2 Entonces
                Si totalUsuarios < 50 Entonces
                    totalUsuarios <- totalUsuarios + 1
                    Escribir "Ingrese DNI:"
                    Leer usuariosDni[totalUsuarios]
                    Escribir "Ingrese clave:"
                    Leer usuariosClave[totalUsuarios]
                    Escribir "Ingrese nombres:"
                    Leer usuariosNombre[totalUsuarios]
                    Escribir "Ingrese apellidos:"
                    Leer usuariosApellido[totalUsuarios]
                    Escribir "Usuario registrado correctamente."
                SiNo
                    Escribir "Se alcanzo el limite de usuarios."
                FinSi
            SiNo
                Si opcion <> 3 Entonces
                    Escribir "Opcion no valida."
                FinSi
            FinSi
        FinSi
    FinMientras

    Escribir "Gracias por usar Mesa de Partes Digital."
FinAlgoritmo
