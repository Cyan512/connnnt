"""
Configuración del sistema de logging
src/utils/logger_config.py
"""

import logging
import os
from datetime import datetime
from src.constants import LOG_FORMAT, LOG_FILE

def configurar_logging(nivel: int = logging.INFO) -> logging.Logger:
    """
    Configura el sistema de logging para la aplicación
    
    Args:
        nivel: Nivel de logging (logging.INFO, logging.DEBUG, etc.)
    
    Returns:
        Logger configurado
    """
    # Crear directorio de logs si no existe
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Nombre del archivo con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(logs_dir, f"traffic_sim_{timestamp}.log")
    
    # Configurar logging básico
    logging.basicConfig(
        level=nivel,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(),  # Consola
            logging.FileHandler(log_filename, encoding='utf-8'),  # Archivo
            logging.FileHandler(LOG_FILE, encoding='utf-8')  # Archivo principal
        ]
    )
    
    # Obtener logger principal
    logger = logging.getLogger('traffic_simulation')
    
    # Log inicial
    logger.info("="*60)
    logger.info("SISTEMA DE LOGGING INICIALIZADO")
    logger.info(f"Archivo de log: {log_filename}")
    logger.info(f"Nivel de logging: {logging.getLevelName(nivel)}")
    logger.info("="*60)
    
    return logger

def obtener_logger(nombre: str) -> logging.Logger:
    """
    Obtiene un logger con el nombre especificado
    
    Args:
        nombre: Nombre del logger
    
    Returns:
        Logger configurado
    """
    return logging.getLogger(f"traffic_simulation.{nombre}")

def cambiar_nivel_logging(nuevo_nivel: int):
    """
    Cambia el nivel de logging en tiempo de ejecución
    
    Args:
        nuevo_nivel: Nuevo nivel de logging
    """
    logger = logging.getLogger('traffic_simulation')
    logger.setLevel(nuevo_nivel)
    
    # Cambiar también en todos los handlers
    for handler in logger.handlers:
        handler.setLevel(nuevo_nivel)
    
    logger.info(f"Nivel de logging cambiado a: {logging.getLevelName(nuevo_nivel)}")

def limpiar_logs_antiguos(dias_antiguedad: int = 7):
    """
    Elimina archivos de log más antiguos que los días especificados
    
    Args:
        dias_antiguedad: Días de antigüedad para considerar un log como antiguo
    """
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        return
    
    import time
    tiempo_limite = time.time() - (dias_antiguedad * 24 * 60 * 60)
    
    archivos_eliminados = 0
    for archivo in os.listdir(logs_dir):
        if archivo.startswith("traffic_sim_") and archivo.endswith(".log"):
            ruta_archivo = os.path.join(logs_dir, archivo)
            if os.path.getctime(ruta_archivo) < tiempo_limite:
                try:
                    os.remove(ruta_archivo)
                    archivos_eliminados += 1
                except OSError:
                    pass
    
    if archivos_eliminados > 0:
        logger = obtener_logger("cleanup")
        logger.info(f"Eliminados {archivos_eliminados} archivos de log antiguos")