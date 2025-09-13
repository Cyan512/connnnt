"""
Sistema de renderizado para el mapa y elementos visuales
src/renderizador.py
"""

import pygame
import math
from typing import List, Tuple

from src.constants import COLORES, ANCHO, ALTO
from src.models import Calle, Edificio, EstadisticasTrafico
from src.enums import TipoEdificio

class RenderizadorMapa:
    """Clase responsable de renderizar todos los elementos visuales del mapa"""
    
    def __init__(self, calles: List[Calle], edificios: List[Edificio], landmarks: List[Tuple[str, int, int]]):
        self.calles = calles
        self.edificios = edificios
        self.landmarks = landmarks
        
        # Inicializar fuentes
        pygame.font.init()
        self.font_titulo = pygame.font.Font(None, 28)
        self.font_stats = pygame.font.Font(None, 20)
        self.font_small = pygame.font.Font(None, 18)
        self.font_landmarks = pygame.font.Font(None, 24)
    
    def dibujar_mapa_completo(self, pantalla):
        """Dibuja el mapa completo con todos sus elementos"""
        pantalla.fill(COLORES['FONDO'])
        
        self._dibujar_calles(pantalla)
        self._dibujar_edificios(pantalla)
        self._dibujar_plazas(pantalla)
        self._dibujar_landmarks(pantalla)
    
    def _dibujar_calles(self, pantalla):
        """Dibuja todas las calles con texturas diferenciadas"""
        for calle in self.calles:
            # Seleccionar color según tipo
            color = COLORES['ASFALTO']
            if calle.tipo == 'empedrada':
                color = COLORES['PIEDRA']
            elif calle.tipo == 'secundaria':
                color = COLORES['ASFALTO_VIEJO']
            
            # Obtener esquinas de la calle
            esquinas = calle.obtener_esquinas()
            
            if len(esquinas) >= 4:
                # Convertir puntos a tuplas para pygame
                puntos_pygame = [(p.x, p.y) for p in esquinas]
                pygame.draw.polygon(pantalla, color, puntos_pygame)
                
                # Líneas divisorias para calles principales
                if calle.tipo == 'principal' and calle.ancho > 35:
                    pygame.draw.line(pantalla, COLORES['LINEA_AMARILLA'],
                                   (calle.inicio.x, calle.inicio.y),
                                   (calle.fin.x, calle.fin.y), 2)
    
    def _dibujar_edificios(self, pantalla):
        """Dibuja todos los edificios según su tipo"""
        for edificio in self.edificios:
            self._dibujar_edificio_individual(pantalla, edificio)
    
    def _dibujar_edificio_individual(self, pantalla, edificio: Edificio):
        """Dibuja un edificio individual según su tipo"""
        rect = edificio.rect
        
        if edificio.tipo == TipoEdificio.CATEDRAL.value:
            self._dibujar_catedral(pantalla, rect)
        elif edificio.tipo == TipoEdificio.IGLESIA.value:
            self._dibujar_iglesia(pantalla, rect)
        elif edificio.tipo == TipoEdificio.COLONIAL.value:
            self._dibujar_edificio_colonial(pantalla, rect)
        elif edificio.tipo == TipoEdificio.MODERNO.value:
            self._dibujar_edificio_moderno(pantalla, rect)
        elif edificio.tipo == TipoEdificio.MERCADO.value:
            self._dibujar_mercado(pantalla, rect)
        elif edificio.tipo == TipoEdificio.TEMPLO.value:
            self._dibujar_templo(pantalla, rect)
        else:
            # Edificio genérico
            pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], rect)
    
    def _dibujar_catedral(self, pantalla, rect):
        """Dibuja la catedral con torres"""
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], rect)
        
        # Torres de la catedral
        torre1 = pygame.Rect(rect.x + 20, rect.y - 30, 30, 30)
        torre2 = pygame.Rect(rect.x + 90, rect.y - 30, 30, 30)
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], torre1)
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], torre2)
        
        # Detalles góticos
        for i in range(3):
            x = rect.x + 20 + i * 30
            y = rect.y + 10
            pygame.draw.arc(pantalla, (100, 60, 30), (x, y, 20, 30), 0, math.pi, 2)
    
    def _dibujar_iglesia(self, pantalla, rect):
        """Dibuja una iglesia con cruz"""
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], rect)
        
        # Cruz en el techo
        cruz_x = rect.centerx
        cruz_y = rect.y - 10
        pygame.draw.line(pantalla, (200, 200, 200), 
                       (cruz_x, cruz_y - 10), (cruz_x, cruz_y + 10), 3)
        pygame.draw.line(pantalla, (200, 200, 200), 
                       (cruz_x - 7, cruz_y - 3), (cruz_x + 7, cruz_y - 3), 3)
    
    def _dibujar_edificio_colonial(self, pantalla, rect):
        """Dibuja un edificio colonial con balcones"""
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], rect)
        
        # Balcón colonial
        balcon = pygame.Rect(rect.x + 10, rect.y + 40, rect.width - 20, 15)
        pygame.draw.rect(pantalla, (120, 60, 30), balcon)
        
        # Ventanas coloniales
        for i in range(min(3, rect.width // 25)):
            ventana = pygame.Rect(rect.x + 15 + i * 25, rect.y + 20, 15, 20)
            pygame.draw.rect(pantalla, (80, 40, 20), ventana)
    
    def _dibujar_edificio_moderno(self, pantalla, rect):
        """Dibuja un edificio moderno con ventanas"""
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_MODERNO'], rect)
        
        # Ventanas en cuadrícula
        cols = min(3, rect.width // 25)
        rows = min(5, rect.height // 30)
        
        for i in range(cols):
            for j in range(rows):
                ventana = pygame.Rect(
                    rect.x + 15 + i * 25,
                    rect.y + 20 + j * 25,
                    15, 15
                )
                pygame.draw.rect(pantalla, (150, 150, 200), ventana)
    
    def _dibujar_mercado(self, pantalla, rect):
        """Dibuja un mercado con techo ondulado"""
        pygame.draw.rect(pantalla, (139, 125, 107), rect)
        
        # Techo ondulado característico
        for i in range(0, rect.width, 20):
            pygame.draw.arc(pantalla, (100, 100, 100),
                          (rect.x + i, rect.y - 15, 20, 30),
                          0, math.pi, 3)
    
    def _dibujar_templo(self, pantalla, rect):
        """Dibuja un templo con características especiales"""
        pygame.draw.rect(pantalla, COLORES['EDIFICIO_COLONIAL'], rect)
        
        # Características de templo inca
        for i in range(rect.width // 30):
            piedra = pygame.Rect(rect.x + i * 30, rect.y, 28, 20)
            color_piedra = (140 + i * 10, 120, 100)
            pygame.draw.rect(pantalla, color_piedra, piedra)
    
    def _dibujar_plazas(self, pantalla):
        """Dibuja las plazas principales"""
        # Plaza de Armas
        plaza_armas = pygame.Rect(420, 480, 180, 120)
        pygame.draw.rect(pantalla, COLORES['PLAZA'], plaza_armas)
        
        # Fuente central
        pygame.draw.circle(pantalla, (100, 100, 150), (510, 540), 25)
        pygame.draw.circle(pantalla, (150, 150, 200), (510, 540), 20)
        pygame.draw.circle(pantalla, (200, 200, 255), (510, 540), 15)
        
        # Plaza San Francisco
        plaza_sf = pygame.Rect(150, 350, 120, 80)
        pygame.draw.rect(pantalla, COLORES['PLAZA'], plaza_sf)
        
        # Plaza Regocijo
        plaza_regocijo = pygame.Rect(250, 550, 100, 70)
        pygame.draw.rect(pantalla, COLORES['PLAZA'], plaza_regocijo)
    
    def _dibujar_landmarks(self, pantalla):
        """Dibuja los nombres de lugares importantes"""
        for nombre, x, y in self.landmarks:
            # Sombra del texto
            texto_sombra = self.font_landmarks.render(nombre, True, (0, 0, 0))
            pantalla.blit(texto_sombra, (x + 1, y + 1))
            
            # Texto principal
            texto = self.font_landmarks.render(nombre, True, COLORES['TEXTO'])
            pantalla.blit(texto, (x, y))
    
    def dibujar_mapa_densidad(self, pantalla, vehiculos):
        """Dibuja overlay de densidad de tráfico"""
        tamano_celda = 100
        for x in range(0, ANCHO, tamano_celda):
            for y in range(0, ALTO, tamano_celda):
                vehiculos_en_celda = sum(1 for v in vehiculos 
                                       if x <= v.posicion.x < x + tamano_celda 
                                       and y <= v.posicion.y < y + tamano_celda)
                
                if vehiculos_en_celda > 0:
                    intensidad = min(255, vehiculos_en_celda * 30)
                    color = (intensidad, 255 - intensidad, 0)
                    
                    superficie = pygame.Surface((tamano_celda, tamano_celda))
                    superficie.set_alpha(100)
                    superficie.fill(color)
                    pantalla.blit(superficie, (x, y))
    
    def dibujar_mapa_velocidad(self, pantalla, vehiculos):
        """Dibuja líneas de velocidad para cada vehículo"""
        for vehiculo in vehiculos:
            if vehiculo.velocidad_actual > 0:
                longitud = vehiculo.velocidad_actual * 15
                end_x = vehiculo.posicion.x + math.cos(vehiculo.direccion) * longitud
                end_y = vehiculo.posicion.y + math.sin(vehiculo.direccion) * longitud
                
                # Color según velocidad relativa
                factor_vel = vehiculo.velocidad_actual / vehiculo.velocidad_maxima
                if factor_vel > 0.8:
                    color = (0, 255, 0)  # Verde - rápido
                elif factor_vel > 0.5:
                    color = (255, 255, 0)  # Amarillo - medio
                else:
                    color = (255, 0, 0)  # Rojo - lento
                
                pygame.draw.line(pantalla, color, 
                               (vehiculo.posicion.x, vehiculo.posicion.y),
                               (end_x, end_y), 3)
    
    def mostrar_estadisticas(self, pantalla, estadisticas: EstadisticasTrafico, 
                           hora_simulada: float, num_semaforos: int):
        """Muestra el panel de estadísticas"""
        # Panel semitransparente
        panel = pygame.Surface((380, 220))
        panel.set_alpha(180)
        panel.fill((20, 20, 20))
        pantalla.blit(panel, (10, 10))
        
        # Título
        titulo = self.font_titulo.render("TRÁFICO CUSCO CON NARRADOR", True, COLORES['TEXTO'])
        pantalla.blit(titulo, (20, 20))
        
        # Información básica
        info_semaforos = self.font_stats.render(f"Semáforos: {num_semaforos}", True, (150, 200, 255))
        pantalla.blit(info_semaforos, (20, 45))
        
        hora_texto = f"Hora: {int(hora_simulada):02d}:{int((hora_simulada % 1) * 60):02d}"
        hora_surface = self.font_stats.render(hora_texto, True, (200, 200, 255))
        pantalla.blit(hora_surface, (200, 45))
        
        # Estadísticas de vehículos
        y_offset = 65
        stats_vehiculos = [
            (f"Autos: {estadisticas.autos}", COLORES['AUTO_ROJO']),
            (f"Combis: {estadisticas.combis}", COLORES['COMBI_AMARILLA']),
            (f"Motos: {estadisticas.motos}", COLORES['MOTO_ROJA']),
            (f"Taxis: {estadisticas.taxis}", COLORES['TAXI']),
            (f"Total activos: {estadisticas.vehiculos_activos}", COLORES['TEXTO']),
            (f"Generados: {estadisticas.vehiculos_generados}", COLORES['TEXTO'])
        ]
        
        for i, (stat, color) in enumerate(stats_vehiculos):
            superficie = self.font_stats.render(stat, True, color)
            pantalla.blit(superficie, (20, y_offset + i * 18))
        
        # Métricas de rendimiento
        self._dibujar_barras_rendimiento(pantalla, estadisticas)
        
        # Densidad por zona
        self._dibujar_densidad_zonas(pantalla, estadisticas)
    
    def _dibujar_barras_rendimiento(self, pantalla, estadisticas: EstadisticasTrafico):
        """Dibuja barras de rendimiento para velocidad y congestión"""
        # Barra de velocidad
        pygame.draw.rect(pantalla, (100, 100, 100), (220, 110, 120, 15))
        ancho_velocidad = int((estadisticas.promedio_velocidad / 3.0) * 120)
        color_velocidad = (0, 255, 0) if estadisticas.promedio_velocidad > 2 else \
                         (255, 255, 0) if estadisticas.promedio_velocidad > 1 else (255, 0, 0)
        pygame.draw.rect(pantalla, color_velocidad, (220, 110, ancho_velocidad, 15))
        
        vel_texto = self.font_stats.render(f"Velocidad: {estadisticas.promedio_velocidad:.1f}", True, COLORES['TEXTO'])
        pantalla.blit(vel_texto, (220, 90))
        
        # Barra de congestión
        pygame.draw.rect(pantalla, (100, 100, 100), (220, 150, 120, 15))
        ancho_congestion = int((estadisticas.congestion / 100) * 120)
        color_congestion = (255, 0, 0) if estadisticas.congestion > 70 else \
                          (255, 255, 0) if estadisticas.congestion > 40 else (0, 255, 0)
        pygame.draw.rect(pantalla, color_congestion, (220, 150, ancho_congestion, 15))
        
        cong_texto = self.font_stats.render(f"Congestión: {estadisticas.congestion:.0f}%", True, COLORES['TEXTO'])
        pantalla.blit(cong_texto, (220, 130))
    
    def _dibujar_densidad_zonas(self, pantalla, estadisticas: EstadisticasTrafico):
        """Dibuja información de densidad por zonas (placeholder)"""
        densidad_texto = self.font_stats.render("Sistema funcionando correctamente", True, (200, 200, 200))
        pantalla.blit(densidad_texto, (20, 190))
    
    def mostrar_controles(self, pantalla, narrador_activo: bool):
        """Muestra los controles disponibles"""
        controles = [
            "CONTROLES:",
            "ESPACIO - Generar vehículo",
            "R - Reiniciar simulación", 
            "T - Cambiar hora del día",
            "N - Alternar narrador",
            "C - Mostrar/ocultar calles",
            "M - Modo de vista",
            "P - Pausar/Reanudar",
            "ESC - Salir"
        ]
        
        for i, control in enumerate(controles):
            if i == 0:
                color = (255, 255, 100)
            elif "narrador" in control.lower():
                color = (100, 255, 100) if narrador_activo else (255, 100, 100)
            else:
                color = (200, 200, 200)
                
            superficie = self.font_small.render(control, True, color)
            pantalla.blit(superficie, (ANCHO - 220, 20 + i * 22))