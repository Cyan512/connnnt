"""
Sistema de narración inteligente que explica el funcionamiento del software
src/narrador.py
"""

import pygame
import time
import datetime
from typing import List, Dict
from src.constants import EXPLICACIONES_TECNICAS, ANCHO, ALTO
from src.enums import TipoMensajeNarrador
from src.models import Punto

class MensajeNarrador:
    """Representa un mensaje del narrador"""
    
    def __init__(self, texto: str, tipo: TipoMensajeNarrador, tiempo: float):
        self.texto = texto
        self.tipo = tipo
        self.tiempo = tiempo
        self.timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.mensaje_completo = f"[{self.timestamp}] {texto}"

class NarradorSistema:
    """Sistema de narración que explica el funcionamiento del software en tiempo real"""
    
    def __init__(self):
        self.mensajes: List[MensajeNarrador] = []
        self.tiempo_ultimo_mensaje = time.time()
        self.explicaciones_mostradas = set()
        self.contador_eventos = 0
        self.activo = True
        self.modo_explicativo = True
        
        # Cola de explicaciones técnicas
        self.explicaciones_tecnicas = EXPLICACIONES_TECNICAS.copy()
        
        self.inicio_narracion()
    
    def inicio_narracion(self):
        """Mensaje inicial explicativo del sistema"""
        print("\n" + "="*80)
        print("🎙️  NARRADOR DEL SISTEMA ACTIVADO")
        print("="*80)
        print("¡Bienvenido a la simulación inteligente de tráfico del Cusco!")
        print("")
        print("EXPLICACIÓN DEL SISTEMA:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("Este software es una simulación avanzada que modela el comportamiento")
        print("del tráfico vehicular en el centro histórico del Cusco utilizando:")
        print("")
        print("🧠 INTELIGENCIA ARTIFICIAL:")
        print("   • Cada vehículo tiene su propia 'personalidad' de conducción")
        print("   • Los conductores reaccionan a semáforos, otros vehículos y condiciones")
        print("   • Algoritmos de toma de decisiones en tiempo real")
        print("")
        print("🗺️  MODELADO GEOGRÁFICO:")
        print("   • Réplica digital de calles reales del Cusco")
        print("   • Diferentes tipos de vías (principales, secundarias, empedradas)")
        print("   • Ubicaciones auténticas: Plaza de Armas, San Blas, San Pedro")
        print("")
        print("⚙️  MOTOR DE SIMULACIÓN:")
        print("   • 60 FPS de renderizado suave con pygame")
        print("   • Física de movimiento realista")
        print("   • Sistema de estados y eventos")
        print("   • Procesamiento paralelo para múltiples entidades")
        print("")
        print("📊 ANÁLISIS DE DATOS:")
        print("   • Estadísticas en tiempo real")
        print("   • Detección automática de patrones de congestión")
        print("   • Métricas de rendimiento del tráfico")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("\n🔄 La simulación iniciará en 3 segundos...")
        print("💡 Presiona 'N' durante la simulación para activar/desactivar narración")
        print("="*80)
        
    def agregar_mensaje(self, mensaje: str, tipo: TipoMensajeNarrador):
        """Agrega un mensaje narrativo a la cola"""
        if not self.activo:
            return
        
        # Controlar frecuencia de mensajes
        tiempo_actual = time.time()
        if tiempo_actual - self.tiempo_ultimo_mensaje < 2:  # Mínimo 2 segundos
            return
        
        nuevo_mensaje = MensajeNarrador(mensaje, tipo, tiempo_actual)
        self.mensajes.append(nuevo_mensaje)
        
        # Mantener solo los últimos 10 mensajes
        if len(self.mensajes) > 10:
            self.mensajes.pop(0)
        
        # Imprimir en consola con formato especial
        prefijos = {
            TipoMensajeNarrador.INFO: '📍',
            TipoMensajeNarrador.TECNICO: '⚙️',
            TipoMensajeNarrador.EVENTO: '🚨',
            TipoMensajeNarrador.ANALISIS: '📊'
        }
        
        prefijo = prefijos.get(tipo, '💬')
        print(f"\n{prefijo} NARRADOR: {mensaje}")
        
        self.tiempo_ultimo_mensaje = tiempo_actual
        self.contador_eventos += 1
    
    def explicar_evento_vehiculo(self, evento: str, vehiculo_tipo: str):
        """Explica eventos específicos de vehículos"""
        explicaciones = {
            'NUEVO': f"Se generó un nuevo {vehiculo_tipo}. El sistema evaluó patrones horarios y capacidad disponible antes de crearlo.",
            'DETENIDO': f"El {vehiculo_tipo} se detuvo. Esto puede deberse a un semáforo en rojo o congestión detectada por sus sensores virtuales.",
            'ACELERANDO': f"El {vehiculo_tipo} acelera. Su algoritmo de conducción determinó que las condiciones son favorables.",
            'FRENANDO': f"El {vehiculo_tipo} está frenando. Su sistema detectó un obstáculo o cambio en las condiciones del tráfico.",
            'CAMBIO DE VÍA': f"El {vehiculo_tipo} cambió de vía siguiendo su ruta calculada por el algoritmo de pathfinding.",
            'RUTA COMPLETADA': f"El {vehiculo_tipo} completó su ruta. El sistema lo eliminará y liberará recursos para nuevos vehículos.",
            'PARADA DE PASAJEROS': f"La {vehiculo_tipo} hizo una parada programada. Este comportamiento está simulado para mayor realismo."
        }
        
        if evento in explicaciones:
            self.agregar_mensaje(explicaciones[evento], TipoMensajeNarrador.EVENTO)
    
    def explicar_semaforo(self, estado: str):
        """Explica el funcionamiento de los semáforos"""
        explicaciones = {
            'ROJO': "Semáforo cambió a ROJO. Los algoritmos de control de tráfico gestionan estos cambios para optimizar el flujo.",
            'VERDE': "Semáforo cambió a VERDE. El sistema permite el paso basándose en temporizadores adaptativos.",
            'AMARILLO': "Semáforo en AMARILLO. Fase de transición que permite a los vehículos prepararse para el cambio."
        }
        
        clave_explicacion = f"semaforo_{estado}"
        if estado in explicaciones and clave_explicacion not in self.explicaciones_mostradas:
            self.agregar_mensaje(explicaciones[estado], TipoMensajeNarrador.TECNICO)
            self.explicaciones_mostradas.add(clave_explicacion)
    
    def analizar_congestion(self, nivel: float):
        """Analiza y explica los niveles de congestión"""
        if nivel > 80 and 'congestion_critica' not in self.explicaciones_mostradas:
            self.agregar_mensaje(
                f"CONGESTIÓN CRÍTICA DETECTADA ({nivel:.1f}%). Los algoritmos identificaron " +
                "múltiples vehículos operando por debajo del 50% de su velocidad óptima.",
                TipoMensajeNarrador.ANALISIS
            )
            self.explicaciones_mostradas.add('congestion_critica')
        elif nivel < 30 and 'flujo_optimo' not in self.explicaciones_mostradas:
            self.agregar_mensaje(
                "Flujo de tráfico ÓPTIMO detectado. Los vehículos se mueven a velocidades cercanas a sus máximos permitidos.",
                TipoMensajeNarrador.ANALISIS
            )
            self.explicaciones_mostradas.add('flujo_optimo')
    
    def explicacion_tecnica_periodica(self):
        """Proporciona explicaciones técnicas periódicas"""
        if self.contador_eventos % 50 == 0 and self.explicaciones_tecnicas:  # Cada 50 eventos
            explicacion = self.explicaciones_tecnicas.pop(0)
            self.agregar_mensaje(f"DETALLE TÉCNICO: {explicacion}", TipoMensajeNarrador.TECNICO)
    
    def analizar_vehiculos(self, cantidad: int, velocidad_promedio: float):
        """Analiza comportamiento general de vehículos"""
        if cantidad > 80 and 'alta_densidad' not in self.explicaciones_mostradas:
            self.agregar_mensaje(
                f"Alta densidad vehicular detectada: {cantidad} vehículos. " +
                "El sistema está operando cerca de su capacidad máxima.",
                TipoMensajeNarrador.ANALISIS
            )
            self.explicaciones_mostradas.add('alta_densidad')
        
        if velocidad_promedio > 2.5 and 'velocidad_optima' not in self.explicaciones_mostradas:
            self.agregar_mensaje(
                f"Excelente fluidez detectada. Velocidad promedio: {velocidad_promedio:.1f}km/h. " +
                "Los algoritmos de optimización están funcionando correctamente.",
                TipoMensajeNarrador.ANALISIS
            )
            self.explicaciones_mostradas.add('velocidad_optima')
    
    def explicar_generacion_vehiculo(self, tipo_vehiculo: str, patron_horario: str):
        """Explica la generación inteligente de vehículos"""
        self.agregar_mensaje(
            f"Generando {tipo_vehiculo} según patrón '{patron_horario}'. " +
            "El sistema evalúa hora simulada, capacidad y tipos de vehículos apropiados.",
            TipoMensajeNarrador.TECNICO
        )
    
    def dibujar_mensajes(self, pantalla):
        """Dibuja los mensajes del narrador en pantalla"""
        if not self.activo or not self.mensajes:
            return
        
        # Panel para mensajes del narrador
        panel_ancho = 500
        panel_alto = 250
        panel = pygame.Surface((panel_ancho, panel_alto))
        panel.set_alpha(220)
        panel.fill((0, 20, 40))
        
        # Borde del panel
        pygame.draw.rect(panel, (100, 150, 200), (0, 0, panel_ancho, panel_alto), 3)
        
        pantalla.blit(panel, (ANCHO - panel_ancho - 10, ALTO - panel_alto - 10))
        
        # Título
        font_titulo = pygame.font.Font(None, 24)
        titulo = font_titulo.render("🎙️ NARRADOR DEL SISTEMA", True, (255, 255, 100))
        pantalla.blit(titulo, (ANCHO - panel_ancho, ALTO - panel_alto + 10))
        
        # Indicador de estado
        estado_texto = "ACTIVO" if self.activo else "INACTIVO"
        font_estado = pygame.font.Font(None, 18)
        estado_surface = font_estado.render(f"Estado: {estado_texto}", True, 
                                          (100, 255, 100) if self.activo else (255, 100, 100))
        pantalla.blit(estado_surface, (ANCHO - panel_ancho + 10, ALTO - panel_alto + 35))
        
        # Mensajes
        font_mensaje = pygame.font.Font(None, 18)
        y_offset = 60
        
        for mensaje in self.mensajes[-8:]:  # Mostrar últimos 8 mensajes
            # Color según tipo
            colores = {
                TipoMensajeNarrador.INFO: (200, 200, 200),
                TipoMensajeNarrador.TECNICO: (150, 200, 255),
                TipoMensajeNarrador.EVENTO: (255, 150, 150),
                TipoMensajeNarrador.ANALISIS: (150, 255, 150)
            }
            color = colores.get(mensaje.tipo, (255, 255, 255))
            
            # Dividir mensajes largos
            palabras = mensaje.mensaje_completo.split()
            linea_actual = ""
            
            for palabra in palabras:
                test_linea = f"{linea_actual} {palabra}" if linea_actual else palabra
                if font_mensaje.size(test_linea)[0] < panel_ancho - 20:
                    linea_actual = test_linea
                else:
                    if linea_actual:
                        superficie = font_mensaje.render(linea_actual, True, color)
                        pantalla.blit(superficie, (ANCHO - panel_ancho + 10, ALTO - panel_alto + y_offset))
                        y_offset += 20
                        if y_offset > panel_alto - 20:  # Evitar salirse del panel
                            break
                    linea_actual = palabra
            
            # Renderizar última línea
            if linea_actual and y_offset <= panel_alto - 20:
                superficie = font_mensaje.render(linea_actual, True, color)
                pantalla.blit(superficie, (ANCHO - panel_ancho + 10, ALTO - panel_alto + y_offset))
                y_offset += 25
    
    def alternar_activacion(self):
        """Activa o desactiva el narrador"""
        self.activo = not self.activo
        estado = "ACTIVADO" if self.activo else "DESACTIVADO"
        print(f"\n🎙️ NARRADOR {estado}")
        if self.activo:
            self.agregar_mensaje("Sistema de narración reactivado. Continuando explicaciones...", TipoMensajeNarrador.INFO)
    
    def reset_explicaciones(self):
        """Reinicia las explicaciones mostradas"""
        self.explicaciones_mostradas.clear()
        self.explicaciones_tecnicas = EXPLICACIONES_TECNICAS.copy()
        self.contador_eventos = 0