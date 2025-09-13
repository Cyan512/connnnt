"""
Configuración global y constantes del sistema
src/constants.py
"""

# Configuración de pantalla
ANCHO = 1600
ALTO = 1000
FPS = 60

# Colores del sistema
COLORES = {
    # Colores de calles y infraestructura
    'ASFALTO': (45, 45, 45),
    'ASFALTO_VIEJO': (55, 50, 45),
    'LINEA_AMARILLA': (255, 255, 100),
    'LINEA_BLANCA': (220, 220, 220),
    'ACERA': (180, 180, 180),
    'PIEDRA': (120, 110, 100),
    
    # Colores de edificios
    'EDIFICIO_COLONIAL': (160, 82, 45),
    'EDIFICIO_MODERNO': (100, 100, 120),
    'PLAZA': (85, 140, 85),
    'PASTO': (60, 120, 60),
    'TIERRA': (139, 125, 107),
    
    # Colores de vehículos
    'AUTO_ROJO': (180, 30, 30),
    'AUTO_AZUL': (30, 80, 180),
    'AUTO_BLANCO': (240, 240, 240),
    'AUTO_NEGRO': (40, 40, 40),
    'COMBI_AMARILLA': (255, 200, 0),
    'COMBI_AZUL': (0, 120, 200),
    'MOTO_ROJA': (200, 50, 50),
    'MOTO_NEGRA': (60, 60, 60),
    'TAXI': (255, 255, 0),
    
    # Colores de semáforos
    'SEMAFORO_ROJO': (255, 50, 50),
    'SEMAFORO_VERDE': (50, 255, 50),
    'SEMAFORO_AMARILLO': (255, 255, 50),
    
    # Colores generales
    'FONDO': (25, 35, 25),
    'TEXTO': (255, 255, 255)
}

# Configuración de vehículos
VELOCIDADES_BASE = {
    'AUTO': 2.5,
    'COMBI': 1.8,
    'MOTO': 3.2,
    'TAXI': 2.0
}

TAMANOS_VEHICULOS = {
    'AUTO': (22, 14),
    'COMBI': (35, 18),
    'MOTO': (14, 10),
    'TAXI': (22, 14)
}

# Configuración de simulación
MAX_VEHICULOS_SIMULTANEOS = 120
INTERVALO_GENERACION_BASE = (1.0, 3.0)  # rango en segundos
DISTANCIA_DETECCION_SEMAFORO = 80
DISTANCIA_SEGUIMIENTO_VEHICULO = 60

# Configuración del narrador
INTERVALO_REPORTE_NARRADOR = 15  # segundos
MAX_MENSAJES_NARRADOR = 10
MIN_TIEMPO_ENTRE_MENSAJES = 2  # segundos

# Patrones horarios
PATRONES_TRAFICO = {
    'mañana': {
        'factor': 1.2, 
        'tipos': ['AUTO', 'COMBI', 'TAXI'],
        'hora_inicio': 6,
        'hora_fin': 12
    },
    'tarde': {
        'factor': 1.5, 
        'tipos': ['COMBI', 'AUTO', 'TAXI'],
        'hora_inicio': 12,
        'hora_fin': 18
    },
    'mediodia': {
        'factor': 0.8, 
        'tipos': ['AUTO', 'MOTO'],
        'hora_inicio': 18,
        'hora_fin': 22
    },
    'noche': {
        'factor': 0.4, 
        'tipos': ['TAXI', 'AUTO'],
        'hora_inicio': 22,
        'hora_fin': 6
    }
}

# Configuración de logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'traffic_simulation.log'

# Mensajes del narrador
EXPLICACIONES_TECNICAS = [
    "El sistema utiliza pygame para renderizar gráficos 2D en tiempo real",
    "Cada vehículo tiene comportamientos únicos definidos por algoritmos de IA",
    "Los semáforos operan con temporizadores independientes y lógica adaptativa",
    "La generación de vehículos sigue patrones horarios basados en datos reales",
    "El sistema de rutas utiliza algoritmos de pathfinding simplificados",
    "La detección de colisiones se basa en cálculos de distancia euclidiana",
    "Los patrones de tráfico cambian dinámicamente según la hora simulada",
    "Cada tipo de vehículo tiene parámetros únicos de velocidad y comportamiento"
]

# Agregar al final
SONIDOS = {
    'MOTOR_AUTO': 'sounds/car_engine.wav',
    'BOCINA': 'sounds/horn.wav', 
    'FRENOS': 'sounds/brakes.wav',
    'AMBIENTE_CIUDAD': 'sounds/city_ambient.wav'
}