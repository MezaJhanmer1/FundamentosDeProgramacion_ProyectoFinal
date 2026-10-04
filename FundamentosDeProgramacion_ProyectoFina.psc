Algoritmo MesaDePartesSEDAPAL
	
    // ============================================================
    // SISTEMA DE MESA DE PARTES DIGITAL - SEDAPAL SJL
    // ============================================================
	
    Definir total Como Entero;
    Definir MAX Como Entero;
	
    Dimension expedientes[100, 8];
	
    MAX <- 100;
    total <- 0;
	
    menu(total, expedientes, MAX);
	
FinAlgoritmo


// ================================================================
// FUNCION: VALIDAR FECHA
// ================================================================
Funcion resultado <- validar_fecha(fecha)
	
    Definir partes, dia, mes, anio Como Cadena;
    Definir pos1, pos2, pos3, i Como Entero;
    Definir valido Como Logico;
    Definir c Como Cadena;
    Definir numDia, numMes, numAnio Como Entero;
	
    pos1 <- 0;
    pos2 <- 0;
    pos3 <- 0;
	
    Para i <- 1 Hasta Longitud(fecha) Hacer
        c <- Subcadena(fecha, i, i);
        Si c = "/" Entonces
            Si pos1 = 0 Entonces
                pos1 <- i;
            Sino
                Si pos2 = 0 Entonces
                    pos2 <- i;
                Sino
                    pos3 <- i;
                FinSi
            FinSi
        FinSi
    FinPara
	
    Si pos1 = 0 O pos2 = 0 O pos3 <> 0 Entonces
        resultado <- Falso;
    Sino
        dia  <- Subcadena(fecha, 1, pos1 - 1);
        mes  <- Subcadena(fecha, pos1 + 1, pos2 - 1);
        anio <- Subcadena(fecha, pos2 + 1, Longitud(fecha));
		
        Si Longitud(dia) <> 2 O Longitud(mes) <> 2 O Longitud(anio) <> 4 Entonces
            resultado <- Falso;
        Sino
            valido <- Verdadero;
			
            Para i <- 1 Hasta Longitud(dia) Hacer
                c <- Subcadena(dia, i, i);
                Si c < "0" O c > "9" Entonces
                    valido <- Falso;
                FinSi
            FinPara
			
            Para i <- 1 Hasta Longitud(mes) Hacer
                c <- Subcadena(mes, i, i);
                Si c < "0" O c > "9" Entonces
                    valido <- Falso;
                FinSi
            FinPara
			
            Para i <- 1 Hasta Longitud(anio) Hacer
                c <- Subcadena(anio, i, i);
                Si c < "0" O c > "9" Entonces
                    valido <- Falso;
                FinSi
            FinPara
			
            Si valido = Falso Entonces
                resultado <- Falso;
            Sino
                numDia  <- ConvertirANumero(dia);
                numMes  <- ConvertirANumero(mes);
                numAnio <- ConvertirANumero(anio);
				
                Si numDia < 1 O numDia > 31 Entonces
                    valido <- Falso;
                FinSi
				
                Si numMes < 1 O numMes > 12 Entonces
                    valido <- Falso;
                FinSi
				
                Si numAnio < 2026 O numAnio > 2100 Entonces
                    valido <- Falso;
                FinSi
				
                resultado <- valido;
            FinSi
        FinSi
    FinSi
	
FinFuncion


// ================================================================
// FUNCION: VALIDAR DNI
// ================================================================
Funcion resultado <- validar_dni(dni)
	
    Definir i Como Entero;
    Definir c Como Cadena;
    Definir valido Como Logico;
	
    valido <- Verdadero;
	
    Si Longitud(dni) <> 8 Entonces
        valido <- Falso;
    Sino
        Para i <- 1 Hasta 8 Hacer
            c <- Subcadena(dni, i, i);
            Si c < "0" O c > "9" Entonces
                valido <- Falso;
            FinSi
        FinPara
    FinSi
	
    resultado <- valido;
	
FinFuncion


// ================================================================
// FUNCION: GENERAR CODIGO
// ================================================================
Funcion codigo <- generar_codigo(total)
	
    Definir numero Como Entero;
    Definir numCadena, codigo2 Como Cadena;
	
    numero <- total + 1;
    numCadena <- ConvertirATexto(numero);
	
    Si numero < 10 Entonces
        codigo2 <- "SED-000" + numCadena;
    Sino
        Si numero < 100 Entonces
            codigo2 <- "SED-00" + numCadena;
        Sino
            codigo2 <- "SED-0" + numCadena;
        FinSi
    FinSi
	
    codigo <- codigo2;
	
FinFuncion


// ================================================================
// SUBPROCESO: REGISTRAR EXPEDIENTE
// ================================================================
SubProceso registrar_expediente(total Por Referencia, expedientes Por Referencia)
	
    Definir codigo, dni, nombre, tipo, descripcion, fecha, estado, opcion Como Cadena;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "       REGISTRO DE EXPEDIENTE";
    Escribir "==========================================";
	
    codigo <- generar_codigo(total);
    Escribir "Codigo del expediente: ", codigo;
	
    // ---- DNI ----
    Escribir Sin Saltar "Ingrese el DNI del ciudadano: ";
    Leer dni;
	
    Mientras validar_dni(dni) = Falso Hacer
        Escribir "Error: el DNI debe tener exactamente 8 numeros.";
        Escribir Sin Saltar "Ingrese nuevamente el DNI: ";
        Leer dni;
    FinMientras
	
    // ---- NOMBRE ----
    Escribir Sin Saltar "Ingrese el nombre completo: ";
    Leer nombre;
	
    Mientras nombre = "" Hacer
        Escribir "El nombre no puede estar vacio.";
        Escribir Sin Saltar "Ingrese el nombre completo: ";
        Leer nombre;
    FinMientras
	
    // ---- TIPO DE TRAMITE ----
    Escribir "";
    Escribir "Seleccione el tipo de tramite:";
    Escribir "1. Quejas y Reclamos";
    Escribir "2. Solicitud";
    Escribir "3. Consulta";
    Escribir Sin Saltar "Ingrese una opcion: ";
    Leer opcion;
	
    Mientras opcion <> "1" Y opcion <> "2" Y opcion <> "3" Hacer
        Escribir "Opcion incorrecta.";
        Escribir Sin Saltar "Ingrese una opcion: ";
        Leer opcion;
    FinMientras
	
    Si opcion = "1" Entonces
        tipo <- "Quejas y Reclamos";
    Sino
        Si opcion = "2" Entonces
            tipo <- "Solicitud";
        Sino
            tipo <- "Consulta";
        FinSi
    FinSi
	
    // ---- DESCRIPCION ----
    Escribir Sin Saltar "Ingrese la descripcion del tramite: ";
    Leer descripcion;
	
    Mientras descripcion = "" Hacer
        Escribir "La descripcion no puede estar vacia.";
        Escribir Sin Saltar "Ingrese la descripcion del tramite: ";
        Leer descripcion;
    FinMientras
	
    // ---- FECHA ----
    Escribir Sin Saltar "Ingrese la fecha (DD/MM/AAAA): ";
    Leer fecha;
	
    Mientras validar_fecha(fecha) = Falso Hacer
        Escribir "Fecha incorrecta.";
        Escribir "Debe utilizar el formato DD/MM/AAAA.";
        Escribir Sin Saltar "Ingrese la fecha (DD/MM/AAAA): ";
        Leer fecha;
    FinMientras
	
    // ---- ESTADO INICIAL ----
    estado <- "Pendiente";
	
    // ---- GUARDAR ----
    total <- total + 1;
    expedientes[total, 1] <- codigo;
    expedientes[total, 2] <- dni;
    expedientes[total, 3] <- nombre;
    expedientes[total, 4] <- tipo;
    expedientes[total, 5] <- descripcion;
    expedientes[total, 6] <- "SJL";
    expedientes[total, 7] <- fecha;
    expedientes[total, 8] <- estado;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "Expediente registrado correctamente.";
    Escribir "Codigo: ", codigo;
    Escribir "Estado: ", estado;
    Escribir "==========================================";
	
FinSubProceso


// ================================================================
// SUBPROCESO: MOSTRAR EXPEDIENTES
// ================================================================
SubProceso mostrar_expedientes(total, expedientes)
	
    Definir i Como Entero;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "          LISTA DE EXPEDIENTES";
    Escribir "==========================================";
	
    Si total = 0 Entonces
        Escribir "No existen expedientes registrados.";
    Sino
        Para i <- 1 Hasta total Hacer
            Escribir "------------------------------------------";
            Escribir "Codigo: ", expedientes[i, 1];
            Escribir "DNI: ", expedientes[i, 2];
            Escribir "Ciudadano: ", expedientes[i, 3];
            Escribir "Tipo: ", expedientes[i, 4];
            Escribir "Descripcion: ", expedientes[i, 5];
            Escribir "Sede: ", expedientes[i, 6];
            Escribir "Fecha: ", expedientes[i, 7];
            Escribir "Estado: ", expedientes[i, 8];
        FinPara
        Escribir "------------------------------------------";
    FinSi
	
FinSubProceso


// ================================================================
// SUBPROCESO: BUSCAR EXPEDIENTE
// ================================================================
SubProceso buscar_expediente(total, expedientes)
	
    Definir i Como Entero;
    Definir codigo_buscar Como Cadena;
    Definir encontrado Como Logico;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "        BUSCAR EXPEDIENTE";
    Escribir "==========================================";
    Escribir Sin Saltar "Ingrese el codigo del expediente: ";
    Leer codigo_buscar;
	
    encontrado <- Falso;
	
    Para i <- 1 Hasta total Hacer
        Si expedientes[i, 1] = codigo_buscar Entonces
            Escribir "";
            Escribir "Expediente encontrado:";
            Escribir "------------------------------------------";
            Escribir "Codigo: ", expedientes[i, 1];
            Escribir "DNI: ", expedientes[i, 2];
            Escribir "Ciudadano: ", expedientes[i, 3];
            Escribir "Tipo: ", expedientes[i, 4];
            Escribir "Descripcion: ", expedientes[i, 5];
            Escribir "Sede: ", expedientes[i, 6];
            Escribir "Fecha: ", expedientes[i, 7];
            Escribir "Estado: ", expedientes[i, 8];
            Escribir "------------------------------------------";
            encontrado <- Verdadero;
        FinSi
    FinPara
	
    Si encontrado = Falso Entonces
        Escribir "No se encontro el expediente.";
    FinSi
	
FinSubProceso


// ================================================================
// SUBPROCESO: ACTUALIZAR ESTADO
// ================================================================
SubProceso actualizar_estado(total, expedientes)
	
    Definir i Como Entero;
    Definir codigo_buscar, opcion Como Cadena;
    Definir encontrado Como Logico;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "       ACTUALIZAR ESTADO";
    Escribir "==========================================";
    Escribir Sin Saltar "Ingrese el codigo del expediente: ";
    Leer codigo_buscar;
	
    encontrado <- Falso;
	
    Para i <- 1 Hasta total Hacer
        Si expedientes[i, 1] = codigo_buscar Entonces
            encontrado <- Verdadero;
			
            Escribir "";
            Escribir "Expediente encontrado.";
            Escribir "Estado actual: ", expedientes[i, 8];
			
            Escribir "";
            Escribir "Seleccione el nuevo estado:";
            Escribir "1. Pendiente";
            Escribir "2. En proceso";
            Escribir "3. Atendido";
            Escribir Sin Saltar "Ingrese una opcion: ";
            Leer opcion;
			
            Mientras opcion <> "1" Y opcion <> "2" Y opcion <> "3" Hacer
                Escribir "Opcion incorrecta.";
                Escribir Sin Saltar "Ingrese una opcion: ";
                Leer opcion;
            FinMientras
			
            Si opcion = "1" Entonces
                expedientes[i, 8] <- "Pendiente";
            Sino
                Si opcion = "2" Entonces
                    expedientes[i, 8] <- "En proceso";
                Sino
                    expedientes[i, 8] <- "Atendido";
                FinSi
            FinSi
			
            Escribir "";
            Escribir "Estado actualizado correctamente.";
            Escribir "Nuevo estado: ", expedientes[i, 8];
        FinSi
    FinPara
	
    Si encontrado = Falso Entonces
        Escribir "No se encontro el expediente.";
    FinSi
	
FinSubProceso


// ================================================================
// SUBPROCESO: ORDENAR EXPEDIENTES (Burbuja por codigo)
// ================================================================
SubProceso ordenar_expedientes(total Por Referencia, expedientes Por Referencia)
	
    Definir i, j, k Como Entero;
    Definir temp Como Cadena;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "       ORDENAR EXPEDIENTES";
    Escribir "==========================================";
	
    Si total = 0 Entonces
        Escribir "No existen expedientes para ordenar.";
    Sino
        Para i <- 1 Hasta total - 1 Hacer
            Para j <- 1 Hasta total - i Hacer
                Si expedientes[j, 1] > expedientes[j + 1, 1] Entonces
                    Para k <- 1 Hasta 8 Hacer
                        temp <- expedientes[j, k];
                        expedientes[j, k] <- expedientes[j + 1, k];
                        expedientes[j + 1, k] <- temp;
                    FinPara
                FinSi
            FinPara
        FinPara
		
        Escribir "Los expedientes fueron ordenados correctamente.";
        mostrar_expedientes(total, expedientes);
    FinSi
	
FinSubProceso


// ================================================================
// SUBPROCESO: GUARDAR EN ARCHIVO
// ================================================================
SubProceso guardar_archivo(total, expedientes)
	
    Definir i Como Entero;
	
    Escribir "";
    Escribir "==========================================";
    Escribir "       GUARDAR EXPEDIENTES";
    Escribir "==========================================";
	
    Si total = 0 Entonces
        Escribir "No existen expedientes para guardar.";
    Sino
        // Nota: PSeInt no tiene manejo nativo de archivos.
        // Usamos Escribir; para guardar en archivo, configura
        // la salida del programa a un archivo .txt desde el menú.
        Para i <- 1 Hasta total Hacer
            Escribir "====================================";
            Escribir "Codigo: ", expedientes[i, 1];
            Escribir "DNI: ", expedientes[i, 2];
            Escribir "Ciudadano: ", expedientes[i, 3];
            Escribir "Tipo: ", expedientes[i, 4];
            Escribir "Descripcion: ", expedientes[i, 5];
            Escribir "Sede: ", expedientes[i, 6];
            Escribir "Fecha: ", expedientes[i, 7];
            Escribir "Estado: ", expedientes[i, 8];
        FinPara
		
        Escribir "";
        Escribir "Los expedientes fueron mostrados para guardado.";
    FinSi
	
FinSubProceso


// ================================================================
// SUBPROCESO: MENU PRINCIPAL
// ================================================================
SubProceso menu(total Por Referencia, expedientes Por Referencia, MAX)
	
    Definir opcion Como Cadena;
    Definir salir Como Logico;
	
    salir <- Falso;
	
    Mientras salir = Falso Hacer
		
        Escribir "";
        Escribir "==========================================";
        Escribir "      SEDAPAL - MESA DE PARTES DIGITAL";
        Escribir "           SEDE SAN JUAN DE LURIGANCHO";
        Escribir "==========================================";
        Escribir "1. Registrar expediente";
        Escribir "2. Mostrar expedientes";
        Escribir "3. Buscar expediente";
        Escribir "4. Actualizar estado";
        Escribir "5. Ordenar expedientes";
        Escribir "6. Guardar expedientes en archivo";
        Escribir "7. Salir";
        Escribir "==========================================";
        Escribir Sin Saltar "Seleccione una opcion: ";
        Leer opcion;
		
        Si opcion = "1" Entonces
            registrar_expediente(total, expedientes);
        Sino
            Si opcion = "2" Entonces
                mostrar_expedientes(total, expedientes);
            Sino
                Si opcion = "3" Entonces
                    buscar_expediente(total, expedientes);
                Sino
                    Si opcion = "4" Entonces
                        actualizar_estado(total, expedientes);
                    Sino
                        Si opcion = "5" Entonces
                            ordenar_expedientes(total, expedientes);
                        Sino
                            Si opcion = "6" Entonces
                                guardar_archivo(total, expedientes);
                            Sino
                                Si opcion = "7" Entonces
                                    Escribir "";
                                    Escribir "Gracias por utilizar el sistema.";
                                    Escribir "SEDAPAL - Mesa de Partes Digital";
                                    salir <- Verdadero;
                                Sino
                                    Escribir "";
                                    Escribir "Opcion incorrecta. Intente nuevamente.";
                                FinSi
                            FinSi
                        FinSi
                    FinSi
                FinSi
            FinSi
        FinSi
		
    FinMientras
	
FinSubProceso