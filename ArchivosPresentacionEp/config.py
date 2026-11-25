import os

# ============================================================
# CONFIGURACION GENERAL: RUTAS Y LIMITES DEL SISTEMA
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# ARCHIVO JSON PARA GUARDAR LOS EXPEDIENTES
# ============================================================
EXPEDIENTES_ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SEDAPAL_expedientes.json"
)

# ============================================================
# CONFIGURACION: LIMITES DE EXPEDIENTES POR USUARIO
# ============================================================
LIMITE_EXPEDIENTES_PERSONA_NATURAL = 5
LIMITE_EXPEDIENTES_ADMINISTRADOR = 50
LIMITE_CONSULTAS_PERSONA_NATURAL = 3

# ============================================================
# ARCHIVO JSON PARA SIMULAR UNA CONSULTA A RENIEC
# ============================================================
BASE_DNI_ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SEDAPAL_base_DNI.json"
)

# ============================================================
# ARCHIVO JSON PARA GUARDAR LOS USUARIOS DEL SISTEMA
# ============================================================
USUARIOS_ARCHIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "SEDAPAL_usuarios.json"
)

# ============================================================
# ARCHIVO JSON PARA GUARDAR/EXPORTAR EL ARCHIVO
# ============================================================
EXPORTAR_TXT_ARCHIVO = os.path.join(
    BASE_DIR, "expedientes_sedapal.txt")