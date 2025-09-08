"""
Enumeraciones y tipos de datos del sistema
src/enums.py
"""

from enum import Enum

class TipoVehiculo(Enum):
    """Tipos de vehículos disponibles en la simulación"""
    AUTO = 1
    COMBI = 2
    MOTO = 3
    TAXI = 4

class EstadoSemaforo(Enum):
    """Estados posibles de un semáforo"""
    ROJO = 1
    AMARILLO = 2
    VERDE = 3

class DireccionCalle(Enum):
    """Orientaciones de las calles"""
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 3

class TipoCalle(Enum):
    """Tipos de calles según su importancia y características"""
    PRINCIPAL = "principal"
    SECUNDARIA = "secundaria" 
    EMPEDRADA = "empedrada"

class TipoEdificio(Enum):
    """Tipos de edificios en el mapa"""
    CATEDRAL = "catedral"
    IGLESIA = "iglesia"
    COLONIAL = "colonial"
    MODERNO = "moderno"
    MERCADO = "mercado"
    TEMPLO = "templo"

class ZonaMapa(Enum):
    """Zonas del mapa para análisis de densidad"""
    CENTRO = "CENTRO"
    NORTE = "NORTE"
    SUR = "SUR"
    ESTE = "ESTE"
    OESTE = "OESTE"

class TipoMensajeNarrador(Enum):
    """Tipos de mensajes del narrador"""
    INFO = "info"
    TECNICO = "tecnico"
    EVENTO = "evento"
    ANALISIS = "analisis"

class ModoVista(Enum):
    """Modos de visualización disponibles"""
    NORMAL = "normal"
    DENSIDAD = "densidad"
    VELOCIDAD = "velocidad"