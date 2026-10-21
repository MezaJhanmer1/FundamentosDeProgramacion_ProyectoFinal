Proceso MesaPartesSEDAPAL
    // SISTEMA SIMULADO DE MESA DE PARTES SEDAPAL
    // Perfiles: 2 = Administrador, 1 = Persona natural
    // Credenciales iniciales:
    // Administrador 1: DNI 60549429, clave admin123
    // Administrador 2: DNI 12345678, clave admin456

    Definir MAX_U, MAX_E, N_REN Como Entero
    Definir i, j, numU, numE, usuarioActual, opcion, encontrado, indiceReniec, salirSistema Como Entero
    Definir perfil, dniIngresado, claveIngresada Como Caracter
    Definir dniConsulta, tipo, descripcion, sede, prioridad, estado Como Caracter
    Definir nuevoEstado, codigoBuscado Como Caracter
    Definir r_dni, r_nom, r_ape Como Caracter
    Definir u_dni, u_nom, u_ape, u_tel, u_cor, u_cla Como Caracter
    Definir u_per Como Entero
    Definir e_cod, e_dni, e_nom, e_ape, e_tel, e_cor Como Caracter
    Definir e_tip, e_des, e_sed, e_fec, e_est, e_pri Como Caracter

    MAX_U <- 50
    MAX_E <- 200
    N_REN <- 30

    Dimension r_dni[30], r_nom[30], r_ape[30]
    Dimension u_dni[50], u_nom[50], u_ape[50]
    Dimension u_tel[50], u_cor[50], u_cla[50], u_per[50]
    Dimension e_cod[200], e_dni[200], e_nom[200], e_ape[200]
    Dimension e_tel[200], e_cor[200], e_tip[200], e_des[200]
    Dimension e_sed[200], e_fec[200], e_est[200], e_pri[200]

    // DATOS SIMULADOS DE RENIEC
    r_dni[1] <- "60549429"
    r_nom[1] <- "Jhanmer"
    r_ape[1] <- "Meza"
    r_dni[2] <- "11111111"
    r_nom[2] <- "Ana"
    r_ape[2] <- "Torres"
    r_dni[3] <- "22222222"
    r_nom[3] <- "Carlos"
    r_ape[3] <- "Ramirez"
    r_dni[4] <- "33333333"
    r_nom[4] <- "Maria"
    r_ape[4] <- "Flores"
    r_dni[5] <- "44444444"
    r_nom[5] <- "Luis"
    r_ape[5] <- "Mendoza"
    r_dni[6] <- "55555555"
    r_nom[6] <- "Rosa"
    r_ape[6] <- "Castillo"
    r_dni[7] <- "66666666"
    r_nom[7] <- "Pedro"
    r_ape[7] <- "Vargas"
    r_dni[8] <- "77777777"
    r_nom[8] <- "Lucia"
    r_ape[8] <- "Herrera"
    r_dni[9] <- "88888888"
    r_nom[9] <- "Jose"
    r_ape[9] <- "Rojas"
    r_dni[10] <- "99999999"
    r_nom[10] <- "Carmen"
    r_ape[10] <- "Diaz"
    r_dni[11] <- "10101010"
    r_nom[11] <- "Miguel"
    r_ape[11] <- "Soto"
    r_dni[12] <- "12121212"
    r_nom[12] <- "Elena"
    r_ape[12] <- "Cruz"
    r_dni[13] <- "13131313"
    r_nom[13] <- "Jorge"
    r_ape[13] <- "Ramos"
    r_dni[14] <- "14141414"
    r_nom[14] <- "Patricia"
    r_ape[14] <- "Leon"
    r_dni[15] <- "15151515"
    r_nom[15] <- "Diego"
    r_ape[15] <- "Silva"
    r_dni[16] <- "16161616"
    r_nom[16] <- "Andrea"
    r_ape[16] <- "Ruiz"
    r_dni[17] <- "17171717"
    r_nom[17] <- "Marco"
    r_ape[17] <- "Vega"
    r_dni[18] <- "18181818"
    r_nom[18] <- "Sofia"
    r_ape[18] <- "Castro"
    r_dni[19] <- "19191919"
    r_nom[19] <- "Daniel"
    r_ape[19] <- "Paredes"
    r_dni[20] <- "20202020"
    r_nom[20] <- "Valeria"
    r_ape[20] <- "Reyes"
    r_dni[21] <- "21212121"
    r_nom[21] <- "Fernando"
    r_ape[21] <- "Luna"
    r_dni[22] <- "23232323"
    r_nom[22] <- "Gabriela"
    r_ape[22] <- "Rios"
    r_dni[23] <- "24242424"
    r_nom[23] <- "Alberto"
    r_ape[23] <- "Salas"
    r_dni[24] <- "25252525"
    r_nom[24] <- "Claudia"
    r_ape[24] <- "Pena"
    r_dni[25] <- "26262626"
    r_nom[25] <- "Ricardo"
    r_ape[25] <- "Flores"
    r_dni[26] <- "27272727"
    r_nom[26] <- "Monica"
    r_ape[26] <- "Campos"
    r_dni[27] <- "28282828"
    r_nom[27] <- "Eduardo"
    r_ape[27] <- "Chavez"
    r_dni[28] <- "29292929"
    r_nom[28] <- "Paola"
    r_ape[28] <- "Medina"
    r_dni[29] <- "30303030"
    r_nom[29] <- "Oscar"
    r_ape[29] <- "Navarro"
    r_dni[30] <- "31313131"
    r_nom[30] <- "Teresa"
    r_ape[30] <- "Aguilar"

    // USUARIOS ADMINISTRADORES INICIALES
    u_dni[1] <- "60549429"
    u_nom[1] <- "Jhanmer"
    u_ape[1] <- "Meza"
    u_tel[1] <- ""
    u_cor[1] <- ""
    u_cla[1] <- "admin123"
    u_per[1] <- 2

    u_dni[2] <- "12345678"
    u_nom[2] <- "Carlos"
    u_ape[2] <- "Ramirez"
    u_tel[2] <- ""
    u_cor[2] <- ""
    u_cla[2] <- "admin456"
    u_per[2] <- 2

    numU <- 2
    numE <- 0
    usuarioActual <- 0
    salirSistema <- 0

    Repetir
        Limpiar Pantalla
        Escribir "======================================"
        Escribir " SISTEMA DE MESA DE PARTES - SEDAPAL"
        Escribir "======================================"
        Escribir "1. Iniciar sesion"
        Escribir "2. Registrar persona natural"
        Escribir "0. Salir"
        Escribir "Seleccione una opcion:"
        Leer opcion

        Segun opcion Hacer
            1:
                Escribir "Ingrese DNI:"
                Leer dniIngresado
                Escribir "Ingrese clave:"
                Leer claveIngresada
                usuarioActual <- 0

                Para i <- 1 Hasta numU Hacer
                    Si u_dni[i] = dniIngresado Y u_cla[i] = claveIngresada Entonces
                        usuarioActual <- i
                    FinSi
                FinPara

                Si usuarioActual = 0 Entonces
                    Escribir "DNI o clave incorrectos."
                    Esperar Tecla
                SiNo
                    Si u_per[usuarioActual] = 2 Entonces
                        // MENU ADMINISTRADOR
                        Repetir
                            Limpiar Pantalla
                            Escribir "===== MENU ADMINISTRADOR ====="
                            Escribir "1. Registrar expediente"
                            Escribir "2. Listar expedientes"
                            Escribir "3. Buscar expediente por codigo"
                            Escribir "4. Cambiar estado de expediente"
                            Escribir "5. Listar usuarios"
                            Escribir "0. Cerrar sesion"
                            Leer opcion

                            Segun opcion Hacer
                                1:
                                    Si numE >= MAX_E Entonces
                                        Escribir "No hay espacio para mas expedientes."
                                    SiNo
                                        Escribir "DNI del solicitante:"
                                        Leer dniConsulta
                                        encontrado <- 0
                                        Para i <- 1 Hasta N_REN Hacer
                                            Si r_dni[i] = dniConsulta Entonces
                                                encontrado <- i
                                            FinSi
                                        FinPara

                                        Si encontrado = 0 Entonces
                                            Escribir "DNI no encontrado en la base simulada RENIEC."
                                        SiNo
                                            numE <- numE + 1
                                            e_cod[numE] <- "EXP-" + ConvertirATexto(1000 + numE)
                                            e_dni[numE] <- r_dni[encontrado]
                                            e_nom[numE] <- r_nom[encontrado]
                                            e_ape[numE] <- r_ape[encontrado]

                                            Escribir "Telefono:"
                                            Leer e_tel[numE]
                                            Escribir "Correo:"
                                            Leer e_cor[numE]
                                            Escribir "Tipo de tramite:"
                                            Leer e_tip[numE]
                                            Escribir "Descripcion:"
                                            Leer e_des[numE]
                                            Escribir "Sede:"
                                            Leer e_sed[numE]
                                            Escribir "Fecha (DD/MM/AAAA):"
                                            Leer e_fec[numE]
                                            Escribir "Prioridad (Normal/Alta):"
                                            Leer e_pri[numE]
                                            e_est[numE] <- "Registrado"

                                            Escribir "Expediente registrado correctamente."
                                            Escribir "Codigo: ", e_cod[numE]
                                            Escribir "Solicitante: ", e_nom[numE], " ", e_ape[numE]
                                        FinSi
                                    FinSi
                                    Esperar Tecla
                                2:
                                    Si numE = 0 Entonces
                                        Escribir "No hay expedientes registrados."
                                    SiNo
                                        Para i <- 1 Hasta numE Hacer
                                            Escribir "------------------------------"
                                            Escribir "Codigo: ", e_cod[i]
                                            Escribir "DNI: ", e_dni[i]
                                            Escribir "Solicitante: ", e_nom[i], " ", e_ape[i]
                                            Escribir "Tramite: ", e_tip[i]
                                            Escribir "Estado: ", e_est[i]
                                            Escribir "Prioridad: ", e_pri[i]
                                        FinPara
                                    FinSi
                                    Esperar Tecla
                                3:
                                    Escribir "Ingrese codigo del expediente:"
                                    Leer codigoBuscado
                                    encontrado <- 0
                                    Para i <- 1 Hasta numE Hacer
                                        Si e_cod[i] = codigoBuscado Entonces
                                            encontrado <- i
                                        FinSi
                                    FinPara
                                    Si encontrado = 0 Entonces
                                        Escribir "No se encontro el expediente."
                                    SiNo
                                        Escribir "Codigo: ", e_cod[encontrado]
                                        Escribir "Solicitante: ", e_nom[encontrado], " ", e_ape[encontrado]
                                        Escribir "DNI: ", e_dni[encontrado]
                                        Escribir "Telefono: ", e_tel[encontrado]
                                        Escribir "Correo: ", e_cor[encontrado]
                                        Escribir "Tipo: ", e_tip[encontrado]
                                        Escribir "Descripcion: ", e_des[encontrado]
                                        Escribir "Sede: ", e_sed[encontrado]
                                        Escribir "Fecha: ", e_fec[encontrado]
                                        Escribir "Estado: ", e_est[encontrado]
                                        Escribir "Prioridad: ", e_pri[encontrado]
                                    FinSi
                                    Esperar Tecla
                                4:
                                    Escribir "Codigo del expediente:"
                                    Leer codigoBuscado
                                    encontrado <- 0
                                    Para i <- 1 Hasta numE Hacer
                                        Si e_cod[i] = codigoBuscado Entonces
                                            encontrado <- i
                                        FinSi
                                    FinPara
                                    Si encontrado = 0 Entonces
                                        Escribir "No se encontro el expediente."
                                    SiNo
                                        Escribir "Estados: Registrado, En proceso, Observado, Atendido"
                                        Escribir "Ingrese el nuevo estado:"
                                        Leer nuevoEstado
                                        e_est[encontrado] <- nuevoEstado
                                        Escribir "Estado actualizado."
                                    FinSi
                                    Esperar Tecla
                                5:
                                    Escribir "===== USUARIOS REGISTRADOS ====="
                                    Para i <- 1 Hasta numU Hacer
                                        Escribir "DNI: ", u_dni[i], " | ", u_nom[i], " ", u_ape[i]
                                        Si u_per[i] = 2 Entonces
                                            Escribir "Perfil: Administrador"
                                        SiNo
                                            Escribir "Perfil: Persona natural"
                                        FinSi
                                    FinPara
                                    Esperar Tecla
                                0:
                                    Escribir "Sesion cerrada."
                                De Otro Modo:
                                    Escribir "Opcion invalida."
                                    Esperar Tecla
                            FinSegun
                        Hasta Que opcion = 0
                    SiNo
                        // MENU PERSONA NATURAL
                        Repetir
                            Limpiar Pantalla
                            Escribir "===== MENU PERSONA NATURAL ====="
                            Escribir "1. Registrar expediente"
                            Escribir "2. Consultar mis expedientes"
                            Escribir "0. Cerrar sesion"
                            Leer opcion
                            Segun opcion Hacer
                                1:
                                    Si numE >= MAX_E Entonces
                                        Escribir "No hay espacio para mas expedientes."
                                    SiNo
                                        numE <- numE + 1
                                        e_cod[numE] <- "EXP-" + ConvertirATexto(1000 + numE)
                                        e_dni[numE] <- u_dni[usuarioActual]
                                        e_nom[numE] <- u_nom[usuarioActual]
                                        e_ape[numE] <- u_ape[usuarioActual]
                                        e_tel[numE] <- u_tel[usuarioActual]
                                        e_cor[numE] <- u_cor[usuarioActual]
                                        Escribir "Tipo de tramite:"
                                        Leer e_tip[numE]
                                        Escribir "Descripcion:"
                                        Leer e_des[numE]
                                        Escribir "Sede:"
                                        Leer e_sed[numE]
                                        Escribir "Fecha (DD/MM/AAAA):"
                                        Leer e_fec[numE]
                                        Escribir "Prioridad (Normal/Alta):"
                                        Leer e_pri[numE]
                                        e_est[numE] <- "Registrado"
                                        Escribir "Expediente registrado. Codigo: ", e_cod[numE]
                                    FinSi
                                    Esperar Tecla
                                2:
                                    encontrado <- 0
                                    Para i <- 1 Hasta numE Hacer
                                        Si e_dni[i] = u_dni[usuarioActual] Entonces
                                            encontrado <- encontrado + 1
                                            Escribir "Codigo: ", e_cod[i], " | Tramite: ", e_tip[i], " | Estado: ", e_est[i]
                                        FinSi
                                    FinPara
                                    Si encontrado = 0 Entonces
                                        Escribir "No tienes expedientes registrados."
                                    FinSi
                                    Esperar Tecla
                                0:
                                    Escribir "Sesion cerrada."
                                De Otro Modo:
                                    Escribir "Opcion invalida."
                                    Esperar Tecla
                            FinSegun
                        Hasta Que opcion = 0
                    FinSi
                FinSi
            2:
                Si numU >= MAX_U Entonces
                    Escribir "Se alcanzo el limite de usuarios."
                    Esperar Tecla
                SiNo
                    Escribir "Ingrese DNI:"
                    Leer dniConsulta
                    indiceReniec <- 0
                    Para i <- 1 Hasta N_REN Hacer
                        Si r_dni[i] = dniConsulta Entonces
                            indiceReniec <- i
                        FinSi
                    FinPara
                    Si indiceReniec = 0 Entonces
                        Escribir "DNI no encontrado en RENIEC simulado."
                        Esperar Tecla
                    SiNo
                        encontrado <- 0
                        Para i <- 1 Hasta numU Hacer
                            Si u_dni[i] = dniConsulta Entonces
                                encontrado <- i
                            FinSi
                        FinPara
                        Si encontrado <> 0 Entonces
                            Escribir "Ese DNI ya tiene una cuenta."
                        SiNo
                            numU <- numU + 1
                            u_dni[numU] <- r_dni[indiceReniec]
                            u_nom[numU] <- r_nom[indiceReniec]
                            u_ape[numU] <- r_ape[indiceReniec]
                            u_per[numU] <- 1
                            Escribir "Telefono:"
                            Leer u_tel[numU]
                            Escribir "Correo:"
                            Leer u_cor[numU]
                            Escribir "Cree una clave:"
                            Leer u_cla[numU]
                            Escribir "Usuario registrado correctamente."
                        FinSi
                        Esperar Tecla
                    FinSi
                FinSi
            0:
                Escribir "Gracias por usar el sistema."
                salirSistema <- 1
            De Otro Modo:
                Escribir "Opcion invalida."
                Esperar Tecla
        FinSegun
    Hasta Que salirSistema = 1
FinProceso
