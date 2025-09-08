"""
Clase que representa un semáforo inteligente
src/semaforo.py
"""

import pygame
import time
import random
from typing import TYPE_CHECKING

from src.models import Punto
from src.enums import EstadoSemaforo
from src.constants import COLORES

if TYPE_CHECKING:
    from src.utils.console_logger import ConsoleLogger

class Semaforo:
    """Representa un semáforo con lógica de temporización inteligente"""
    
    def __init__(self, posicion: Punto, tipo: str = 'normal', console_logger: 'ConsoleLogger' = None):
        self.posicion = posicion
        self.estado = EstadoSemaforo.VERDE
        self.tipo = tipo
        self.console_logger = console_logger
        self.id = f"SEM_{posicion.x:.0f}_{posicion.y:.0f}"
        
        # Configuración de tiempos según el tipo
        self._configurar_tiempos(tipo)
        
        # Tiempo del próximo cambio
        self.tiempo_cambio = time.time() + random.uniform(5, 12)
        
        # Estados para tracking
        self.ultimo_estado = self.estado
        self.cambios_estado = 0
        self.tiempo_creacion = time.time()
        
    def _configurar_tiempos(self, tipo: str):
        """Configura los tiempos de duración según el tipo de semáforo"""
        if tipo == 'principal':
            # Semáforos en avenidas principales - ciclos más largos
            self.duracion_verde = random.uniform(8, 15)
            self.duracion_rojo = random.uniform(6, 12)
            self.duracion_amarillo = 3
        else:
            # Semáforos normales - ciclos más cortos
            self.duracion_verde = random.uniform(5, 10)
            self.duracion_rojo = random.uniform(4, 8)
            self.duracion_amarillo = 3
    
    def actualizar(self):
        """Actualiza el estado del semáforo según su ciclo temporal"""
        tiempo_actual = time.time()
        
        # Verificar si es momento de cambiar
        if tiempo_actual >= self.tiempo_cambio:
            estado_anterior = self.estado
            
            # Lógica de cambio de estados
            if self.estado == EstadoSemaforo.VERDE:
                self.estado = EstadoSemaforo.AMARILLO
                self.tiempo_cambio = tiempo_actual + self.duracion_amarillo
            elif self.estado == EstadoSemaforo.AMARILLO:
                self.estado = EstadoSemaforo.ROJO
                self.tiempo_cambio = tiempo_actual + self.duracion_rojo
            else:  # EstadoSemaforo.ROJO
                self.estado = EstadoSemaforo.VERDE
                self.tiempo_cambio = tiempo_actual + self.duracion_verde
            
            # Log del cambio de estado
            if self.console_logger and estado_anterior != self.estado:
                self.console_logger.log_cambio_semaforo(self.posicion, self.estado.name)
                self.cambios_estado += 1
    
    def tiempo_restante(self) -> float:
        """Retorna el tiempo restante en el estado actual"""
        return max(0, self.tiempo_cambio - time.time())
    
    def porcentaje_tiempo_restante(self) -> float:
        """Retorna el porcentaje de tiempo restante (0-100)"""
        if self.estado == EstadoSemaforo.VERDE:
            duracion_total = self.duracion_verde
        elif self.estado == EstadoSemaforo.AMARILLO:
            duracion_total = self.duracion_amarillo
        else:
            duracion_total = self.duracion_rojo
        
        tiempo_restante = self.tiempo_restante()
        return (tiempo_restante / duracion_total) * 100
    
    def forzar_estado(self, nuevo_estado: EstadoSemaforo, duracion: float = None):
        """Fuerza un cambio de estado (para testing o control manual)"""
        estado_anterior = self.estado
        self.estado = nuevo_estado
        
        # Establecer duración
        if duracion is None:
            if nuevo_estado == EstadoSemaforo.VERDE:
                duracion = self.duracion_verde
            elif nuevo_estado == EstadoSemaforo.AMARILLO:
                duracion = self.duracion_amarillo
            else:
                duracion = self.duracion_rojo
        
        self.tiempo_cambio = time.time() + duracion
        
        if self.console_logger:
            self.console_logger.log_cambio_semaforo(
                self.posicion, 
                f"{nuevo_estado.name} (FORZADO)"
            )
    
    def ajustar_ciclo(self, factor: float):
        """Ajusta la duración de los ciclos según un factor (para optimización)"""
        self.duracion_verde *= factor
        self.duracion_rojo *= factor
        # El amarillo se mantiene constante por seguridad
    
    def dibujar(self, pantalla):
        """Dibuja el semáforo en la pantalla"""
        # Poste del semáforo
        pygame.draw.rect(pantalla, (80, 80, 80), 
                        (self.posicion.x - 3, self.posicion.y - 20, 6, 40))
        
        # Caja del semáforo (fondo negro)
        pygame.draw.rect(pantalla, (40, 40, 40), 
                        (self.posicion.x - 15, self.posicion.y - 25, 30, 20))
        
        # Borde de la caja
        pygame.draw.rect(pantalla, (100, 100, 100), 
                        (self.posicion.x - 15, self.posicion.y - 25, 30, 20), 1)
        
        # Luces del semáforo
        self._dibujar_luces(pantalla)
        
        # Indicador de tiempo restante (opcional, para debugging)
        if hasattr(self, 'mostrar_tiempo') and self.mostrar_tiempo:
            self._dibujar_indicador_tiempo(pantalla)
    
    def _dibujar_luces(self, pantalla):
        """Dibuja las tres luces del semáforo"""
        # Posiciones de las luces (rojo, amarillo, verde)
        posiciones_luces = [
            (int(self.posicion.x - 10), int(self.posicion.y - 15)),  # Rojo
            (int(self.posicion.x), int(self.posicion.y - 15)),       # Amarillo
            (int(self.posicion.x + 10), int(self.posicion.y - 15))   # Verde
        ]
        
        # Colores base (apagados)
        colores_base = [(100, 100, 100)] * 3
        
        # Activar color según estado actual
        if self.estado == EstadoSemaforo.ROJO:
            colores_base[0] = COLORES['SEMAFORO_ROJO']
        elif self.estado == EstadoSemaforo.AMARILLO:
            colores_base[1] = COLORES['SEMAFORO_AMARILLO']
        else:  # EstadoSemaforo.VERDE
            colores_base[2] = COLORES['SEMAFORO_VERDE']
        
        # Dibujar cada luz
        for i, (pos, color) in enumerate(zip(posiciones_luces, colores_base)):
            pygame.draw.circle(pantalla, color, pos, 4)
            
            # Efecto de brillo para la luz activa
            if ((i == 0 and self.estado == EstadoSemaforo.ROJO) or
                (i == 1 and self.estado == EstadoSemaforo.AMARILLO) or
                (i == 2 and self.estado == EstadoSemaforo.VERDE)):
                pygame.draw.circle(pantalla, (255, 255, 255), pos, 4, 1)
    
    def _dibujar_indicador_tiempo(self, pantalla):
        """Dibuja un indicador del tiempo restante (para debugging)"""
        font = pygame.font.Font(None, 16)
        tiempo_restante = self.tiempo_restante()
        texto = font.render(f"{tiempo_restante:.1f}s", True, (255, 255, 255))
        pantalla.blit(texto, (self.posicion.x - 15, self.posicion.y + 20))
    
    def obtener_info(self) -> dict:
        """Retorna información del semáforo para debugging"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'estado': self.estado.name,
            'posicion': (self.posicion.x, self.posicion.y),
            'tiempo_restante': self.tiempo_restante(),
            'porcentaje_restante': self.porcentaje_tiempo_restante(),
            'cambios_realizados': self.cambios_estado,
            'tiempo_funcionamiento': time.time() - self.tiempo_creacion,
            'duraciones': {
                'verde': self.duracion_verde,
                'amarillo': self.duracion_amarillo,
                'rojo': self.duracion_rojo
            }
        }
    
    def es_momento_critico(self) -> bool:
        """Retorna True si está en un momento crítico del ciclo (cambio inminente)"""
        return self.tiempo_restante() < 1.0
    
    def permitir_paso(self) -> bool:
        """Retorna True si el semáforo permite el paso de vehículos"""
        return self.estado == EstadoSemaforo.VERDE