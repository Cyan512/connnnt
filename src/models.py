"""
Modelos y clases de datos básicas
src/models.py
"""

import math
from dataclasses import dataclass
from typing import List
from src.enums import DireccionCalle

@dataclass
class Punto:
    """Representa una coordenada en el espacio 2D"""
    x: float
    y: float
    
    def distancia_a(self, otro: 'Punto') -> float:
        """Calcula la distancia euclidiana a otro punto"""
        return math.sqrt((self.x - otro.x)**2 + (self.y - otro.y)**2)
    
    def angulo_hacia(self, otro: 'Punto') -> float:
        """Calcula el ángulo hacia otro punto en radianes"""
        dx = otro.x - self.x
        dy = otro.y - self.y
        return math.atan2(dy, dx)
    
    def mover_en_direccion(self, angulo: float, distancia: float) -> 'Punto':
        """Retorna un nuevo punto movido en la dirección y distancia especificada"""
        nuevo_x = self.x + math.cos(angulo) * distancia
        nuevo_y = self.y + math.sin(angulo) * distancia
        return Punto(nuevo_x, nuevo_y)

@dataclass
class Calle:
    """Representa una calle en el mapa"""
    inicio: Punto
    fin: Punto
    ancho: int
    tipo: str
    direccion: DireccionCalle
    velocidad_maxima: float
    
    @property
    def longitud(self) -> float:
        """Calcula la longitud de la calle"""
        return self.inicio.distancia_a(self.fin)
    
    @property
    def angulo(self) -> float:
        """Calcula el ángulo de la calle en radianes"""
        return self.inicio.angulo_hacia(self.fin)
    
    def punto_en_progreso(self, progreso: float) -> Punto:
        """Obtiene un punto en la calle según el progreso (0.0 a 1.0)"""
        progreso = max(0.0, min(1.0, progreso))  # Clamp entre 0 y 1
        x = self.inicio.x + (self.fin.x - self.inicio.x) * progreso
        y = self.inicio.y + (self.fin.y - self.inicio.y) * progreso
        return Punto(x, y)
    
    def obtener_esquinas(self) -> List[Punto]:
        """Obtiene las 4 esquinas del rectángulo que representa la calle"""
        if self.longitud == 0:
            return [self.inicio] * 4
            
        # Vector unitario perpendicular
        dx = self.fin.x - self.inicio.x
        dy = self.fin.y - self.inicio.y
        longitud = math.sqrt(dx*dx + dy*dy)
        
        ux = -dy / longitud
        uy = dx / longitud
        
        ancho_mitad = self.ancho / 2
        
        return [
            Punto(self.inicio.x + ux * ancho_mitad, self.inicio.y + uy * ancho_mitad),
            Punto(self.inicio.x - ux * ancho_mitad, self.inicio.y - uy * ancho_mitad),
            Punto(self.fin.x - ux * ancho_mitad, self.fin.y - uy * ancho_mitad),
            Punto(self.fin.x + ux * ancho_mitad, self.fin.y + uy * ancho_mitad)
        ]

@dataclass
class Edificio:
    """Representa un edificio en el mapa"""
    x: int
    y: int
    ancho: int
    alto: int
    tipo: str
    nombre: str = ""
    
    @property
    def rect(self):
        """Retorna un rectángulo pygame para el edificio"""
        import pygame
        return pygame.Rect(self.x, self.y, self.ancho, self.alto)
    
    @property
    def centro(self) -> Punto:
        """Obtiene el punto central del edificio"""
        return Punto(self.x + self.ancho // 2, self.y + self.alto // 2)

@dataclass
class EstadisticasTrafico:
    """Almacena estadísticas del tráfico"""
    autos: int = 0
    combis: int = 0
    motos: int = 0
    taxis: int = 0
    promedio_velocidad: float = 0.0
    congestion: float = 0.0
    vehiculos_activos: int = 0
    vehiculos_generados: int = 0
    
    @property
    def total_vehiculos(self) -> int:
        """Total de vehículos por tipo"""
        return self.autos + self.combis + self.motos + self.taxis
    
    def porcentaje_tipo(self, tipo: str) -> float:
        """Calcula el porcentaje de un tipo de vehículo"""
        if self.total_vehiculos == 0:
            return 0.0
        
        cantidad = getattr(self, tipo.lower(), 0)
        return (cantidad / self.total_vehiculos) * 100
    
    def reset(self):
        """Reinicia las estadísticas"""
        self.autos = 0
        self.combis = 0
        self.motos = 0
        self.taxis = 0
        self.promedio_velocidad = 0.0
        self.congestion = 0.0
        self.vehiculos_activos = 0
        # Nota: vehiculos_generados no se reinicia intencionalmente

@dataclass
class ConfiguracionSimulacion:
    """Configuración general de la simulación"""
    ancho_pantalla: int = 1600
    alto_pantalla: int = 1000
    fps: int = 60
    max_vehiculos: int = 120
    hora_inicial: float = 8.0
    narrador_activo: bool = True
    logging_detallado: bool = True
    
    def validar(self) -> bool:
        """Valida que la configuración sea correcta"""
        return (
            self.ancho_pantalla > 0 and 
            self.alto_pantalla > 0 and 
            self.fps > 0 and 
            self.max_vehiculos > 0 and
            0 <= self.hora_inicial < 24
        )