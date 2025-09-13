"""
Clase principal que maneja toda la simulación de tráfico
src/simulacion.py
"""

import pygame
import random
import time
import threading
from typing import List, Dict, Tuple

from src.constants import ANCHO, ALTO, FPS, COLORES, PATRONES_TRAFICO, MAX_VEHICULOS_SIMULTANEOS
from src.enums import TipoVehiculo, ModoVista
from src.models import Punto, ConfiguracionSimulacion, EstadisticasTrafico
from src.vehiculo import Vehiculo
from src.semaforo import Semaforo
from src.narrador import NarradorSistema
from src.utils.console_logger import ConsoleLogger
from src.mapa_cusco import GeneradorMapaCusco
from src.renderizador import RenderizadorMapa
from src.utils.logger_config import obtener_logger

logger = obtener_logger("simulacion")

class SimulacionTrafico:
    """Clase principal que controla toda la simulación de tráfico"""
    
    def __init__(self, config: ConfiguracionSimulacion = None):
        # Configuración
        self.config = config or ConfiguracionSimulacion()
        
        # Inicializar Pygame
        self.pantalla = pygame.display.set_mode((self.config.ancho_pantalla, self.config.alto_pantalla))
        pygame.display.set_caption("Simulación Inteligente - Centro Histórico del Cusco con Narrador")
        self.reloj = pygame.time.Clock()
        
        # Inicializar sistemas principales
        self.narrador = NarradorSistema() if self.config.narrador_activo else None
        self.console_logger = ConsoleLogger(self.narrador) if self.narrador else None
        
        # Generar mapa de Cusco
        generador_mapa = GeneradorMapaCusco()
        self.calles, self.edificios, self.landmarks = generador_mapa.generar_mapa_completo()
        self.intersecciones_principales = generador_mapa.obtener_intersecciones_principales()
        self.intersecciones_secundarias = generador_mapa.obtener_intersecciones_secundarias()
        self.intersecciones_historicas = generador_mapa.obtener_intersecciones_historicas()
        
        # Inicializar renderizador
        self.renderizador = RenderizadorMapa(self.calles, self.edificios, self.landmarks)
        
        # Entidades de simulación
        self.vehiculos: List[Vehiculo] = []
        self.semaforos: List[Semaforo] = []
        
        # Crear semáforos
        self._crear_semaforos()
        
        # Estado de la simulación
        self.estadisticas = EstadisticasTrafico()
        self.hora_simulada = self.config.hora_inicial
        self.vehiculos_generados = 0
        self.tiempo_ultima_generacion = time.time()
        self.tiempo_inicio = time.time()
        self.max_vehiculos_simultaneos = 0
        
        # Controles de la simulación
        self.ejecutando = False
        self.pausado = False
        self.mostrar_calles = True
        self.modo_vista = ModoVista.NORMAL
        
        # Log inicial
        self._log_inicializacion()
    
    def _log_inicializacion(self):
        """Registra la inicialización del sistema"""
        logger.info("Simulación inicializada correctamente")
        logger.info(f"Configuración: {self.config.ancho_pantalla}x{self.config.alto_pantalla}")
        logger.info(f"Calles creadas: {len(self.calles)}")
        logger.info(f"Semáforos instalados: {len(self.semaforos)}")
        logger.info(f"Edificios: {len(self.edificios)}")
        logger.info(f"Hora inicial: {int(self.hora_simulada):02d}:00")
        
        if self.narrador:
            self.narrador.agregar_mensaje(
                "Sistema iniciado correctamente. Comenzando simulación del tráfico en el Cusco histórico.",
                self.narrador.agregar_mensaje.__annotations__.get('tipo', 'info')
            )
    
    def _crear_semaforos(self):
        """Crea todos los semáforos en las intersecciones"""
        # Semáforos principales
        for posicion, tipo in self.intersecciones_principales:
            self.semaforos.append(Semaforo(posicion, tipo, self.console_logger))
        
        # Semáforos secundarios
        for posicion, tipo in self.intersecciones_secundarias:
            self.semaforos.append(Semaforo(posicion, tipo, self.console_logger))
        
        # Semáforos en zona histórica
        for posicion, tipo in self.intersecciones_historicas:
            self.semaforos.append(Semaforo(posicion, tipo, self.console_logger))
        
        logger.info(f"Creados {len(self.semaforos)} semáforos en total")
    
    def _obtener_patron_horario_actual(self) -> Dict:
        """Obtiene el patrón de tráfico según la hora actual"""
        if 6 <= self.hora_simulada < 12:
            return PATRONES_TRAFICO['mañana']
        elif 12 <= self.hora_simulada < 18:
            return PATRONES_TRAFICO['tarde']
        elif 18 <= self.hora_simulada < 22:
            return PATRONES_TRAFICO['mediodia']
        else:
            return PATRONES_TRAFICO['noche']
    
    def _generar_vehiculo_inteligente(self):
        """Genera un vehículo siguiendo patrones inteligentes"""
        tiempo_actual = time.time()
        patron = self._obtener_patron_horario_actual()
        
        # Verificar si debe generar según el patrón
        intervalo_base = random.uniform(1.0, 3.0)
        intervalo_ajustado = intervalo_base / patron['factor']
        
        if tiempo_actual - self.tiempo_ultima_generacion < intervalo_ajustado:
            return False
        
        # Verificar capacidad
        if len(self.vehiculos) >= self.config.max_vehiculos:
            return False
        
        # Seleccionar tipo de vehículo
        tipos_disponibles = [TipoVehiculo[tipo] for tipo in patron['tipos']]
        tipo_vehiculo = random.choice(tipos_disponibles)
        
        # Seleccionar calle inicial
        calles_principales = [c for c in self.calles if c.tipo in ['principal', 'secundaria']]
        if not calles_principales:
            return False
        
        calle_inicial = random.choice(calles_principales)
        
        # Posición inicial
        progreso_inicial = random.uniform(0, 0.1)
        posicion_inicial = calle_inicial.punto_en_progreso(progreso_inicial)
        
        # Crear vehículo
        vehiculo = Vehiculo(tipo_vehiculo, posicion_inicial, calle_inicial, self.console_logger)
        
        # Generar ruta
        ruta = self._generar_ruta_realista(calle_inicial)
        vehiculo.establecer_ruta(ruta)
        
        # Añadir a la simulación
        self.vehiculos.append(vehiculo)
        self.vehiculos_generados += 1
        self._actualizar_estadisticas_vehiculo(tipo_vehiculo, 1)
        self.tiempo_ultima_generacion = tiempo_actual
        
        # Actualizar máximo simultáneo
        if len(self.vehiculos) > self.max_vehiculos_simultaneos:
            self.max_vehiculos_simultaneos = len(self.vehiculos)
        
        # Notificar al narrador
        if self.narrador:
            self.narrador.explicar_generacion_vehiculo(tipo_vehiculo.name, list(PATRONES_TRAFICO.keys())[0])
        
        return True
    
    def _generar_ruta_realista(self, calle_inicial) -> List:
        """Genera una ruta realista conectando calles"""
        ruta = [calle_inicial]
        calle_actual = calle_inicial
        intentos = 0
        max_intentos = 20
        
        for _ in range(random.randint(3, 7)):
            if intentos >= max_intentos:
                break
                
            # Buscar calles conectadas
            calles_conectadas = []
            for calle in self.calles:
                if calle != calle_actual:
                    # Verificar conexión por proximidad
                    if (calle_actual.fin.distancia_a(calle.inicio) < 50 or
                        calle_actual.fin.distancia_a(calle.fin) < 50):
                        calles_conectadas.append(calle)
            
            if calles_conectadas:
                calle_actual = random.choice(calles_conectadas)
                ruta.append(calle_actual)
                intentos = 0
            else:
                intentos += 1
                if intentos >= max_intentos:
                    break
        
        return ruta
    
    def _actualizar_estadisticas_vehiculo(self, tipo: TipoVehiculo, incremento: int):
        """Actualiza las estadísticas por tipo de vehículo"""
        if tipo == TipoVehiculo.AUTO:
            self.estadisticas.autos += incremento
        elif tipo == TipoVehiculo.COMBI:
            self.estadisticas.combis += incremento
        elif tipo == TipoVehiculo.MOTO:
            self.estadisticas.motos += incremento
        elif tipo == TipoVehiculo.TAXI:
            self.estadisticas.taxis += incremento
    
    def _actualizar_simulacion(self):
        """Actualiza todos los elementos de la simulación"""
        # Avanzar hora simulada
        self.hora_simulada += 0.001
        if self.hora_simulada >= 24:
            self.hora_simulada = 0
        
        # Generar vehículos automáticamente
        if len(self.vehiculos) < self.config.max_vehiculos:
            if random.random() < 0.4:  # 40% chance por frame
                self._generar_vehiculo_inteligente()
        
        # Actualizar semáforos
        for semaforo in self.semaforos:
            semaforo.actualizar()
        
        # Actualizar vehículos
        vehiculos_a_eliminar = []
        for vehiculo in self.vehiculos:
            if not vehiculo.actualizar(self.vehiculos, self.semaforos):
                vehiculos_a_eliminar.append(vehiculo)
        
        # Eliminar vehículos que completaron su ruta
        for vehiculo in vehiculos_a_eliminar:
            self.vehiculos.remove(vehiculo)
            self._actualizar_estadisticas_vehiculo(vehiculo.tipo, -1)
        
        # Actualizar estadísticas generales
        self._actualizar_estadisticas_generales()
    
    def _actualizar_estadisticas_generales(self):
        """Actualiza las estadísticas generales del tráfico"""
        self.estadisticas.vehiculos_activos = len(self.vehiculos)
        self.estadisticas.vehiculos_generados = self.vehiculos_generados
        
        if not self.vehiculos:
            self.estadisticas.promedio_velocidad = 0.0
            self.estadisticas.congestion = 0.0
            return
        
        # Velocidad promedio
        velocidad_total = sum(v.velocidad_actual for v in self.vehiculos)
        self.estadisticas.promedio_velocidad = velocidad_total / len(self.vehiculos)
        
        # Nivel de congestión
        vehiculos_lentos = sum(1 for v in self.vehiculos 
                              if v.velocidad_actual < v.velocidad_maxima * 0.5)
        self.estadisticas.congestion = min(100, (vehiculos_lentos / len(self.vehiculos)) * 100)
        
        # Detectar congestión por zonas
        if self.console_logger:
            self._analizar_congestion_por_zonas()
    
    def _analizar_congestion_por_zonas(self):
        """Analiza la congestión en diferentes zonas del mapa"""
        zonas = {
            'CENTRO': [400, 800, 300, 700],
            'NORTE': [0, ANCHO, 0, 300],
            'SUR': [0, ANCHO, 700, ALTO],
            'ESTE': [800, ANCHO, 0, ALTO],
            'OESTE': [0, 400, 0, ALTO]
        }
        
        for zona, (x_min, x_max, y_min, y_max) in zonas.items():
            vehiculos_zona = [v for v in self.vehiculos 
                            if x_min <= v.posicion.x <= x_max and y_min <= v.posicion.y <= y_max]
            
            if vehiculos_zona:
                vehiculos_lentos = sum(1 for v in vehiculos_zona 
                                     if v.velocidad_actual < v.velocidad_maxima * 0.5)
                congestion_zona = (vehiculos_lentos / len(vehiculos_zona)) * 100
                self.console_logger.detectar_congestion(congestion_zona, zona)
    
    def _manejar_eventos(self):
        """Maneja los eventos de Pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
                
            elif evento.type == pygame.KEYDOWN:
                self._manejar_tecla(evento.key)
    
    def _manejar_tecla(self, tecla):
        """Maneja las teclas presionadas"""
        if tecla == pygame.K_SPACE:
            self._generar_vehiculo_inteligente()
            if self.narrador:
                self.narrador.agregar_mensaje(
                    f"Vehículo generado manualmente. Total activos: {len(self.vehiculos)}"
                )
                
        elif tecla == pygame.K_r:
            self._reiniciar_simulacion()
            
        elif tecla == pygame.K_t:
            self.hora_simulada = (self.hora_simulada + 2) % 24
            if self.narrador:
                self.narrador.agregar_mensaje(
                    f"Hora simulada cambiada a {int(self.hora_simulada):02d}:00. " +
                    "Los patrones de tráfico se ajustarán automáticamente."
                )
                
        elif tecla == pygame.K_n and self.narrador:
            self.narrador.alternar_activacion()
            
        elif tecla == pygame.K_c:
            self.mostrar_calles = not self.mostrar_calles
            if self.narrador:
                estado = "visibles" if self.mostrar_calles else "ocultas"
                self.narrador.agregar_mensaje(f"Vista de calles {estado}")
                
        elif tecla == pygame.K_m:
            modos = list(ModoVista)
            idx_actual = modos.index(self.modo_vista)
            self.modo_vista = modos[(idx_actual + 1) % len(modos)]
            if self.narrador:
                self.narrador.agregar_mensaje(f"Modo de vista cambiado a: {self.modo_vista.value}")
                
        elif tecla == pygame.K_p:
            self.pausado = not self.pausado
            estado = "pausada" if self.pausado else "reanudada"
            if self.narrador:
                self.narrador.agregar_mensaje(f"Simulación {estado}")
            logger.info(f"Simulación {estado}")
            
        elif tecla == pygame.K_ESCAPE:
            self.ejecutando = False
    
    def _reiniciar_simulacion(self):
        """Reinicia la simulación completa"""
        self.vehiculos.clear()
        self.vehiculos_generados = 0
        self.estadisticas.reset()
        self.hora_simulada = self.config.hora_inicial
        
        if self.narrador:
            self.narrador.reset_explicaciones()
            self.narrador.agregar_mensaje("Sistema reiniciado completamente")
        
        if self.console_logger:
            self.console_logger = ConsoleLogger(self.narrador)
        
        logger.info("Simulación reiniciada por usuario")
    
    def _renderizar(self):
        """Renderiza toda la escena"""
        # Limpiar pantalla
        if self.mostrar_calles:
            self.renderizador.dibujar_mapa_completo(self.pantalla)
        else:
            self.pantalla.fill(COLORES['FONDO'])
        
        # Efectos especiales según modo de vista
        if self.modo_vista == ModoVista.DENSIDAD:
            self.renderizador.dibujar_mapa_densidad(self.pantalla, self.vehiculos)
        elif self.modo_vista == ModoVista.VELOCIDAD:
            self.renderizador.dibujar_mapa_velocidad(self.pantalla, self.vehiculos)
        
        # Dibujar semáforos
        for semaforo in self.semaforos:
            semaforo.dibujar(self.pantalla)
        
        # Dibujar vehículos
        for vehiculo in self.vehiculos:
            vehiculo.dibujar(self.pantalla)
        
        # Indicador de pausa
        if self.pausado:
            self._dibujar_indicador_pausa()
        
        # Interfaz
        self.renderizador.mostrar_estadisticas(self.pantalla, self.estadisticas, self.hora_simulada, len(self.semaforos))
        self.renderizador.mostrar_controles(self.pantalla, self.narrador.activo if self.narrador else False)
        
        # Mensajes del narrador
        if self.narrador:
            self.narrador.dibujar_mensajes(self.pantalla)
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def _dibujar_indicador_pausa(self):
        """Dibuja el indicador de pausa"""
        font_pausa = pygame.font.Font(None, 48)
        texto_pausa = font_pausa.render("PAUSADO", True, (255, 255, 0))
        rect_pausa = texto_pausa.get_rect(center=(ANCHO//2, 50))
        self.pantalla.blit(texto_pausa, rect_pausa)
    
    def _iniciar_hilo_reportes(self):
        """Inicia el hilo para reportes automáticos"""
        def reporte_automatico():
            while self.ejecutando:
                if not self.pausado and self.console_logger:
                    self.console_logger.reporte_periodico(
                        self.estadisticas.__dict__, 
                        len(self.vehiculos), 
                        self.hora_simulada
                    )
                time.sleep(15)  # Reportar cada 15 segundos
        
        if self.config.logging_detallado:
            hilo_reporte = threading.Thread(target=reporte_automatico, daemon=True)
            hilo_reporte.start()
            return hilo_reporte
        return None
    
    def ejecutar(self):
        """Bucle principal de la simulación"""
        self.ejecutando = True
        
        # Mostrar información inicial
        self._mostrar_info_inicial()
        
        # Iniciar hilo de reportes
        hilo_reportes = self._iniciar_hilo_reportes()
        
        # Bucle principal
        try:
            while self.ejecutando:
                # Manejar eventos
                self._manejar_eventos()
                
                # Actualizar simulación si no está pausada
                if not self.pausado:
                    self._actualizar_simulacion()
                
                # Renderizar
                self._renderizar()
                
                # Controlar FPS
                self.reloj.tick(self.config.fps)
                
        except Exception as e:
            logger.error(f"Error en bucle principal: {e}")
            raise
            
        finally:
            # Generar reporte final
            self._generar_reporte_final()
            
            # Cerrar pygame
            pygame.quit()
    
    def _mostrar_info_inicial(self):
        """Muestra información inicial de la simulación"""
        print("Iniciando Simulación INTELIGENTE del Tráfico en Cusco con NARRADOR")
        print("=" * 70)
        print(f"Zona AMPLIADA - Características implementadas:")
        print(f"✅ Red de {len(self.calles)} calles (principal, secundaria, empedrada)")
        print(f"✅ {len(self.semaforos)} semáforos inteligentes en intersecciones clave")
        print("✅ Comportamientos realistas por tipo de vehículo")
        print("✅ Patrones de tráfico por horarios")
        print("✅ Barrios específicos: San Blas, Santa Ana, Santiago, San Pedro")
        print("✅ Landmarks: Plaza de Armas, Catedral, Qorikancha, Mercado San Pedro")
        print("✅ Estadísticas avanzadas en tiempo real")
        print(f"✅ Capacidad para hasta {self.config.max_vehiculos} vehículos simultáneos")
        if self.narrador:
            print("✅ SISTEMA DE NARRADOR EXPLICATIVO ACTIVADO")
        print("=" * 70)
    
    def _generar_reporte_final(self):
        """Genera el reporte final de la simulación"""
        tiempo_total = time.time() - self.tiempo_inicio
        
        if self.console_logger:
            self.console_logger.reporte_final(
                tiempo_total, 
                self.vehiculos_generados, 
                self.estadisticas.__dict__
            )
        
        # Log final
        logger.info("Simulación finalizada")
        logger.info(f"Duración total: {tiempo_total:.1f} segundos")
        logger.info(f"Vehículos generados: {self.vehiculos_generados}")
        logger.info(f"Máximo simultáneo: {self.max_vehiculos_simultaneos}")
    
    def obtener_info_debug(self) -> Dict:
        """Retorna información detallada para debugging"""
        return {
            'simulacion': {
                'ejecutando': self.ejecutando,
                'pausado': self.pausado,
                'hora_simulada': self.hora_simulada,
                'tiempo_funcionamiento': time.time() - self.tiempo_inicio
            },
            'vehiculos': {
                'activos': len(self.vehiculos),
                'generados': self.vehiculos_generados,
                'maximo_simultaneo': self.max_vehiculos_simultaneos
            },
            'infraestructura': {
                'calles': len(self.calles),
                'semaforos': len(self.semaforos),
                'edificios': len(self.edificios)
            },
            'estadisticas': self.estadisticas.__dict__,
            'sistemas': {
                'narrador_activo': self.narrador.activo if self.narrador else False,
                'logger_activo': self.console_logger is not None,
                'modo_vista': self.modo_vista.value,
                'mostrar_calles': self.mostrar_calles
            }
        }
    
    def pausar(self):
        """Pausa la simulación"""
        self.pausado = True
        logger.info("Simulación pausada programáticamente")
    
    def reanudar(self):
        """Reanuda la simulación"""
        self.pausado = False
        logger.info("Simulación reanudada programáticamente")
    
    def cambiar_hora(self, nueva_hora: float):
        """Cambia la hora simulada"""
        if 0 <= nueva_hora < 24:
            self.hora_simulada = nueva_hora
            logger.info(f"Hora simulada cambiada a {nueva_hora:.1f}")
            return True
        return False