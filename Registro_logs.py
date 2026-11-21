"""Configuración del archivo de logs (único uso de archivos permitido)."""
import logging  # Módulo estándar de registro de eventos
import os       # Para crear la carpeta de logs

RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")  # Carpeta de logs junto al código
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")                      # Ruta del archivo de log


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema, configurado una sola vez."""
    os.makedirs(RUTA_LOGS, exist_ok=True)           # Crea la carpeta si no existe
    logger = logging.getLogger("software_fj")       # Obtiene (o crea) el logger por nombre
    if not logger.handlers:                         # Evita duplicar handlers si se llama varias veces
        logger.setLevel(logging.INFO)               # Registra INFO, WARNING y ERROR
        manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")  # Sobrescribe en cada ejecución
        formato = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")  # Formato de cada línea
        manejador.setFormatter(formato)             # Asocia el formato al manejador
        logger.addHandler(manejador)                # Añade el manejador al logger
    return logger                                   # Retorna el logger listo
