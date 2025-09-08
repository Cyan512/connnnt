"""
Clase que representa un vehículo en la simulación
src/vehiculo.py
"""

import pygame
import random
import math
import time
from typing import List, Tuple, Optional, TYPE_CHECKING

from src.models import Punto, Calle
from src.enums import TipoVehiculo, EstadoSemaforo
from src.constants import VELOCIDADES_BASE, TAMANOS_VEHICULOS, COLORES

if TYPE_CHECKING:
    from src.semaforo import Semaforo
    from src.utils.console_logger import ConsoleLogger

class Vehiculo:
    """Representa un vehículo individual con comportamiento inteligente"""
    
    def __init__(self, tipo: TipoVehiculo, posicion: Punto, calle_actual: Calle, console_logger: 'ConsoleLogger'):
        self.tipo = tipo
        self.posicion = posicion
        self.calle_actual = calle_actual
        self.direccion = self._calcular_direccion_inicial()
        self.velocidad_maxima = self._obtener_velocidad_maxima()
        self.velocidad_actual = 0.0
        self.velocidad_objetivo = 0.0
        self.tamano = self._obtener_tamano()
        self.color = self._obtener_color()
        self.ruta: List[Calle] = []
        self.indice_ruta = 0
        self.tiempo_parada = 0
        self.comportamiento = self._obtener_comportamiento()
        self.carril = random.choice([-1, 1])  # Lado de la calle
        self.console_logger = console_logger
        self.id = f"{tipo.name}_{random.randint(1000, 9999)}"
        self.tiempo_creacion = time.time()
        self.distancia_recorrida = 0.0
        self.cambios_velocidad = 0
        self.tiempo_ultimo_evento = time.time()
        
        # Log creación del vehículo
        self.console_logger.log_evento_vehiculo(
            f"NUEVO {self.tipo.name}", self.id, self.posicion
        )
        
    def _calcular_direccion_inicial(self) -> float:
        """Calcula la dirección inicial basada en la calle actual"""
        dx = self.calle_actual.fin.x - self.calle_actual.inicio.x
        dy = self.calle_actual.fin.y - self.calle_actual.inicio.y
        return math.atan2(dy, dx)
        
    def _obtener_velocidad_maxima(self) -> float:
        """Determina la velocidad máxima según el tipo de vehículo y calle"""
        velocidad_base = VELOCIDADES_BASE[self.tipo.name]
        
        # Ajustar por tipo de calle
        factor = 1.0
        if self.calle_actual.tipo == 'empedrada':
            factor = 0.6
        elif self.calle_actual.tipo == 'secundaria':
            factor = 0.8
        
        # Añadir variación aleatoria para realismo
        variacion = random.uniform(0.8, 1.2)
        
        return velocidad_base * factor * variacion
    
    def _obtener_tamano(self) -> Tuple[int, int]:
        """Obtiene el tamaño del vehículo según su tipo"""
        return TAMANOS_VEHICULOS[self.tipo.name]
    
    def _obtener_color(self) -> Tuple[int, int, int]:
        """Selecciona un color aleatorio según el tipo de vehículo"""
        colores_por_tipo = {
            TipoVehiculo.AUTO: [
                COLORES['AUTO_ROJO'], COLORES['AUTO_AZUL'], 
                COLORES['AUTO_BLANCO'], COLORES['AUTO_NEGRO']
            ],
            TipoVehiculo.COMBI: [
                COLORES['COMBI_AMARILLA'], COLORES['COMBI_AZUL']
            ],
            TipoVehiculo.MOTO: [
                COLORES['MOTO_ROJA'], COLORES['MOTO_NEGRA']
            ],
            TipoVehiculo.TAXI: [
                COLORES['TAXI']
            ]
        }
        return random.choice(colores_por_tipo[self.tipo])
    
    def _obtener_comportamiento(self) -> dict:
        """Define comportamientos específicos por tipo de vehículo"""
        comportamientos = {
            TipoVehiculo.AUTO: {
                'paciencia': random.uniform(0.7, 1.0),
                'agresividad': random.uniform(0.3, 0.7),
                'tiempo_reaccion': random.uniform(0.5, 1.0)
            },
            TipoVehiculo.COMBI: {
                'paciencia': random.uniform(0.4, 0.8),
                'agresividad': random.uniform(0.6, 0.9),  # Más agresivas
                'tiempo_reaccion': random.uniform(0.8, 1.5),
                'paradas_frecuentes': True
            },
            TipoVehiculo.MOTO: {
                'paciencia': random.uniform(0.2, 0.5),
                'agresividad': random.uniform(0.8, 1.0),  # Muy agresivas
                'tiempo_reaccion': random.uniform(0.2, 0.5),
                'puede_zigzaguear': True
            },
            TipoVehiculo.TAXI: {
                'paciencia': random.uniform(0.5, 0.8),
                'agresividad': random.uniform(0.4, 0.8),
                'tiempo_reaccion': random.uniform(0.6, 1.0),
                'busca_pasajeros': True
            }
        }
        return comportamientos[self.tipo]
    
    def establecer_ruta(self, calles: List[Calle]):
        """Establece la ruta que seguirá el vehículo"""
        self.ruta = calles
        self.indice_ruta = 0
        
    def actualizar(self, otros_vehiculos: List['Vehiculo'], semaforos: List['Semaforo']) -> bool:
        """
        Actualiza el estado del vehículo
        Retorna False si el vehículo debe ser eliminado
        """
        tiempo_actual = time.time()
        posicion_anterior = Punto(self.posicion.x, self.posicion.y)
        
        # Verificar si la ruta está completa
        if not self.ruta or self.indice_ruta >= len(self.ruta):
            tiempo_vida = tiempo_actual - self.tiempo_creacion
            self.console_logger.log_evento_vehiculo(
                f"RUTA COMPLETADA (vida: {tiempo_vida:.1f}s, dist: {self.distancia_recorrida:.1f})", 
                self.id, self.posicion
            )
            return False
            
        calle_actual = self.ruta[self.indice_ruta]
        
        # Verificar progreso en la calle actual
        progreso = self._calcular_progreso_en_calle()
        if progreso >= 1.0:
            self.indice_ruta += 1
            if self.indice_ruta >= len(self.ruta):
                return False
            calle_actual = self.ruta[self.indice_ruta]
            self._actualizar_direccion()
            
            # Log cambio de calle ocasional
            if tiempo_actual - self.tiempo_ultimo_evento > 5:
                self.console_logger.log_evento_vehiculo(
                    f"CAMBIO DE VÍA (calle {self.calle_actual.tipo})", 
                    self.id, self.posicion
                )
                self.tiempo_ultimo_evento = tiempo_actual
        
        # Calcular nueva velocidad objetivo
        velocidad_anterior = self.velocidad_actual
        self.velocidad_objetivo = self._calcular_velocidad_objetivo(otros_vehiculos, semaforos)
        
        # Aplicar comportamientos especiales
        self._aplicar_comportamiento_especial()
        
        # Actualizar velocidad suavemente
        self._actualizar_velocidad()
        
        # Detectar cambios significativos de velocidad
        if abs(self.velocidad_actual - velocidad_anterior) > 1.0:
            self.cambios_velocidad += 1
            if self.cambios_velocidad % 5 == 0:  # Log cada 5 cambios
                evento = self._determinar_evento_velocidad(velocidad_anterior)
                self.console_logger.log_evento_vehiculo(
                    f"{evento} (vel: {self.velocidad_actual:.1f})", 
                    self.id, self.posicion
                )
        
        # Mover vehículo
        self._mover()
        
        # Actualizar estadísticas
        distancia_movida = posicion_anterior.distancia_a(self.posicion)
        self.distancia_recorrida += distancia_movida
        
        return True
    
    def _calcular_progreso_en_calle(self) -> float:
        """Calcula qué porcentaje de la calle actual ha recorrido"""
        if not self.ruta:
            return 1.0
        calle = self.ruta[self.indice_ruta]
        total = calle.inicio.distancia_a(calle.fin)
        actual = calle.inicio.distancia_a(self.posicion)
        return min(actual / total, 1.0) if total > 0 else 1.0
    
    def _actualizar_direccion(self):
        """Actualiza la dirección basada en la calle actual"""
        if self.indice_ruta < len(self.ruta):
            calle = self.ruta[self.indice_ruta]
            dx = calle.fin.x - calle.inicio.x
            dy = calle.fin.y - calle.inicio.y
            self.direccion = math.atan2(dy, dx)
    
    def _calcular_velocidad_objetivo(self, otros_vehiculos: List['Vehiculo'], 
                                   semaforos: List['Semaforo']) -> float:
        """Calcula la velocidad objetivo considerando obstáculos"""
        vel_objetivo = self.velocidad_maxima
        
        # Verificar semáforos
        for semaforo in semaforos:
            if self._debe_detenerse_por_semaforo(semaforo):
                vel_objetivo = 0
                break
        
        # Verificar otros vehículos
        vehiculo_adelante = self._encontrar_vehiculo_adelante(otros_vehiculos)
        if vehiculo_adelante:
            distancia = self.posicion.distancia_a(vehiculo_adelante.posicion)
            if distancia < 40:  # Muy cerca
                vel_objetivo = min(vel_objetivo, vehiculo_adelante.velocidad_actual * 0.5)
            elif distancia < 60:  # Cerca
                vel_objetivo = min(vel_objetivo, vehiculo_adelante.velocidad_actual * 0.8)
        
        return vel_objetivo
    
    def _debe_detenerse_por_semaforo(self, semaforo: 'Semaforo') -> bool:
        """Determina si debe detenerse por un semáforo"""
        if semaforo.estado == EstadoSemaforo.VERDE:
            return False
            
        distancia = self.posicion.distancia_a(semaforo.posicion)
        if distancia > 80:  # Muy lejos
            return False
            
        # Verificar si se acerca al semáforo
        dx = semaforo.posicion.x - self.posicion.x
        dy = semaforo.posicion.y - self.posicion.y
        angulo_al_semaforo = math.atan2(dy, dx)
        
        diferencia_angulo = abs(self.direccion - angulo_al_semaforo)
        diferencia_angulo = min(diferencia_angulo, 2 * math.pi - diferencia_angulo)
        
        return diferencia_angulo < math.pi / 3  # 60 grados
    
    def _encontrar_vehiculo_adelante(self, otros_vehiculos: List['Vehiculo']) -> Optional['Vehiculo']:
        """Encuentra el vehículo más cercano adelante"""
        vehiculo_mas_cercano = None
        distancia_minima = float('inf')
        
        for otro in otros_vehiculos:
            if otro == self:
                continue
                
            # Verificar si está adelante
            dx = otro.posicion.x - self.posicion.x
            dy = otro.posicion.y - self.posicion.y
            angulo_al_otro = math.atan2(dy, dx)
            
            diferencia_angulo = abs(self.direccion - angulo_al_otro)
            diferencia_angulo = min(diferencia_angulo, 2 * math.pi - diferencia_angulo)
            
            if diferencia_angulo < math.pi / 4:  # 45 grados adelante
                distancia = self.posicion.distancia_a(otro.posicion)
                if distancia < distancia_minima:
                    distancia_minima = distancia
                    vehiculo_mas_cercano = otro
        
        return vehiculo_mas_cercano
    
    def _aplicar_comportamiento_especial(self):
        """Aplica comportamientos específicos según el tipo de vehículo"""
        # Combis pueden hacer paradas ocasionales
        if (self.tipo == TipoVehiculo.COMBI and 
            self.comportamiento.get('paradas_frecuentes') and
            random.random() < 0.001):  # 0.1% chance por frame
            self.tiempo_parada = random.uniform(60, 180)  # 1-3 segundos
            
            self.console_logger.log_evento_vehiculo(
                f"PARADA DE PASAJEROS ({self.tiempo_parada/60:.1f}s)", 
                self.id, self.posicion
            )
        
        # Reducir tiempo de parada
        if self.tiempo_parada > 0:
            self.tiempo_parada -= 1
            self.velocidad_objetivo = 0
    
    def _actualizar_velocidad(self):
        """Actualiza la velocidad suavemente hacia el objetivo"""
        aceleracion = 0.08 * self.comportamiento['agresividad']
        frenado = 0.15
        
        if self.velocidad_actual < self.velocidad_objetivo:
            self.velocidad_actual = min(
                self.velocidad_actual + aceleracion, 
                self.velocidad_objetivo
            )
        else:
            self.velocidad_actual = max(
                self.velocidad_actual - frenado, 
                max(0, self.velocidad_objetivo)
            )
    
    def _determinar_evento_velocidad(self, velocidad_anterior: float) -> str:
        """Determina el tipo de evento de velocidad"""
        if self.velocidad_actual < 0.5:
            return "DETENIDO"
        elif self.velocidad_actual < velocidad_anterior:
            return "FRENANDO"
        else:
            return "ACELERANDO"
    
    def _mover(self):
        """Mueve el vehículo en la dirección actual"""
        # Añadir ruido para movimiento más realista
        ruido = random.uniform(-0.1, 0.1) * (1 - self.comportamiento['paciencia'])
        direccion_con_ruido = self.direccion + ruido
        
        # Calcular nueva posición
        self.posicion.x += math.cos(direccion_con_ruido) * self.velocidad_actual
        self.posicion.y += math.sin(direccion_con_ruido) * self.velocidad_actual
    
    def dibujar(self, pantalla):
        """Dibuja el vehículo en la pantalla"""
        # Dibujar sombra
        sombra_offset = 2
        self._dibujar_vehiculo(pantalla, 
                              Punto(self.posicion.x + sombra_offset, 
                                   self.posicion.y + sombra_offset),
                              (0, 0, 0))
        
        # Dibujar vehículo principal
        self._dibujar_vehiculo(pantalla, self.posicion, self.color)
        
        # Indicadores especiales
        if self.tiempo_parada > 0:
            pygame.draw.circle(pantalla, (255, 255, 0), 
                             (int(self.posicion.x), int(self.posicion.y - 20)), 3)
    
    def _dibujar_vehiculo(self, pantalla, posicion: Punto, color):
        """Dibuja la representación visual del vehículo"""
        ancho, alto = self.tamano
        cos_a = math.cos(self.direccion)
        sin_a = math.sin(self.direccion)
        
        # Puntos del rectángulo del vehículo
        puntos = [
            (-ancho/2, -alto/2), (ancho/2, -alto/2),
            (ancho/2, alto/2), (-ancho/2, alto/2)
        ]
        
        # Rotar y trasladar puntos
        puntos_rotados = []
        for px, py in puntos:
            x_rot = px * cos_a - py * sin_a + posicion.x
            y_rot = px * sin_a + py * cos_a + posicion.y
            puntos_rotados.append((x_rot, y_rot))
        
        pygame.draw.polygon(pantalla, color, puntos_rotados)
        
        # Detalles específicos por tipo
        if self.tipo == TipoVehiculo.TAXI:
            # Letrero de taxi
            pygame.draw.rect(pantalla, (0, 0, 0), 
                           (posicion.x - 8, posicion.y - 12, 16, 6))
    
    def obtener_info(self) -> dict:
        """Retorna información del vehículo para debugging"""
        return {
            'id': self.id,
            'tipo': self.tipo.name,
            'posicion': (self.posicion.x, self.posicion.y),
            'velocidad_actual': self.velocidad_actual,
            'velocidad_maxima': self.velocidad_maxima,
            'distancia_recorrida': self.distancia_recorrida,
            'tiempo_vida': time.time() - self.tiempo_creacion,
            'progreso_ruta': f"{self.indice_ruta + 1}/{len(self.ruta)}" if self.ruta else "Sin ruta"
        }