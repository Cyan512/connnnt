"""
Sistema avanzado de logging para la consola con integración del narrador
src/utils/console_logger.py
"""

import time
import datetime
import logging
from typing import List, Dict, TYPE_CHECKING

from src.models import Punto
from src.enums import TipoMensajeNarrador

if TYPE_CHECKING:
    from src.narrador import NarradorSistema

# Configurar logger
logger = logging.getLogger(__name__)

class ConsoleLogger:
    """Sistema de logging mejorado con integración del narrador"""
    
    def __init__(self, narrador: 'NarradorSistema'):
        self.narrador = narrador
        self.ultimo_reporte = time.time()
        self.intervalo_reporte = 15  # Segundos entre reportes
        self.eventos_recientes = []
        self.estadisticas_historial = []
        self.alertas_activas = set()
        
        # Contadores para análisis
        self.total_eventos = 0
        self.eventos_por_tipo = {}
        
    def log_evento_vehiculo(self, evento: str, vehiculo_id: str, posicion: Punto):
        """Registra eventos específicos de vehículos con narración"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        mensaje = f"[{timestamp}] {evento} - {vehiculo_id} en ({posicion.x:.0f},{posicion.y:.0f})"
        
        # Log tradicional
        logger.info(mensaje)
        
        # Agregar a eventos recientes
        self.eventos_recientes.append((time.time(), mensaje))
        if len(self.eventos_recientes) > 20:
            self.eventos_recientes.pop(0)
        
        # Contar eventos por tipo
        self.eventos_por_tipo[evento] = self.eventos_por_tipo.get(evento, 0) + 1
        self.total_eventos += 1
        
        # Notificar al narrador
        tipo_vehiculo = vehiculo_id.split('_')[0]
        self.narrador.explicar_evento_vehiculo(evento, tipo_vehiculo)
        self.narrador.explicacion_tecnica_periodica()
    
    def log_cambio_semaforo(self, semaforo_pos: Punto, estado_nuevo: str):
        """Registra cambios de estado en semáforos con narración"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        mensaje = f"[{timestamp}] SEMÁFORO ({semaforo_pos.x:.0f},{semaforo_pos.y:.0f}) -> {estado_nuevo}"
        
        logger.info(mensaje)
        
        # Notificar al narrador
        self.narrador.explicar_semaforo(estado_nuevo)
    
    def detectar_congestion(self, nivel_congestion: float, zona: str = "GENERAL"):
        """Detecta y reporta congestión con análisis del narrador"""
        clave_alerta = f"CONGESTION_{zona}"
        
        if nivel_congestion > 80 and clave_alerta not in self.alertas_activas:
            self.alertas_activas.add(clave_alerta)
            mensaje = f"🚨 ALERTA: Congestión CRÍTICA en {zona} ({nivel_congestion:.1f}%)"
            print(f"\n{mensaje}")
            logger.warning(mensaje)
            
            # Análisis del narrador
            self.narrador.analizar_congestion(nivel_congestion)
            
        elif nivel_congestion < 60 and clave_alerta in self.alertas_activas:
            self.alertas_activas.remove(clave_alerta)
            mensaje = f"✅ Congestión en {zona} normalizada ({nivel_congestion:.1f}%)"
            print(f"\n{mensaje}")
            logger.info(mensaje)
    
    def reporte_periodico(self, estadisticas: dict, vehiculos_activos: int, hora_sim: float):
        """Genera reporte periódico con explicaciones del narrador"""
        tiempo_actual = time.time()
        
        if tiempo_actual - self.ultimo_reporte >= self.intervalo_reporte:
            self._generar_reporte_consola(estadisticas, vehiculos_activos, hora_sim)
            self._analizar_para_narrador(estadisticas, vehiculos_activos)
            self._guardar_estadisticas_historial(tiempo_actual, vehiculos_activos, estadisticas, hora_sim)
            
            self.ultimo_reporte = tiempo_actual
    
    def _generar_reporte_consola(self, estadisticas: dict, vehiculos_activos: int, hora_sim: float):
        """Genera el reporte en consola de manera compacta"""
        print("\n" + "="*60)
        print(f"📊 REPORTE - HORA: {int(hora_sim):02d}:{int((hora_sim % 1) * 60):02d}")
        print(f"🚗 Vehículos: {vehiculos_activos} | Vel.Prom: {estadisticas['promedio_velocidad']:.1f}km/h")
        
        # Estado del tráfico con emoji
        congestion = estadisticas['congestion']
        if congestion < 40:
            estado = "🟢 FLUIDO"
        elif congestion < 70:
            estado = "🟡 MODERADO"
        else:
            estado = "🔴 CRÍTICO"
        
        print(f"🚦 Congestión: {congestion:.1f}% | Estado: {estado}")
        
        # Distribución de vehículos
        tipos = ['autos', 'combis', 'motos', 'taxis']
        distribucion = " | ".join([f"{tipo.capitalize()}: {estadisticas.get(tipo, 0)}" 
                                  for tipo in tipos])
        print(f"🚙 {distribucion}")
        
        # Eventos más frecuentes
        if self.eventos_por_tipo:
            evento_top = max(self.eventos_por_tipo.items(), key=lambda x: x[1])
            print(f"📝 Evento más frecuente: {evento_top[0]} ({evento_top[1]} veces)")
        
        print("="*60)
    
    def _analizar_para_narrador(self, estadisticas: dict, vehiculos_activos: int):
        """Realiza análisis específicos para el narrador"""
        # Análisis de vehículos
        self.narrador.analizar_vehiculos(vehiculos_activos, estadisticas['promedio_velocidad'])
        
        # Análisis de congestión
        self.narrador.analizar_congestion(estadisticas['congestion'])
        
        # Análisis de patrones si hay suficiente historial
        if len(self.estadisticas_historial) >= 3:
            self._analizar_tendencias()
    
    def _analizar_tendencias(self):
        """Analiza tendencias en los datos históricos"""
        if len(self.estadisticas_historial) < 3:
            return
        
        # Obtener últimas 3 mediciones
        ultimas = self.estadisticas_historial[-3:]
        
        # Analizar tendencia de congestión
        congestiones = [h['congestion'] for h in ultimas]
        if congestiones[-1] > congestiones[0] + 20:  # Aumento significativo
            self.narrador.agregar_mensaje(
                "TENDENCIA DETECTADA: La congestión está aumentando rápidamente. " +
                "Esto podría indicar un evento de tráfico o hora pico.",
                TipoMensajeNarrador.ANALISIS
            )
        elif congestiones[0] > congestiones[-1] + 20:  # Disminución significativa
            self.narrador.agregar_mensaje(
                "TENDENCIA POSITIVA: La congestión está disminuyendo. " +
                "Los algoritmos de optimización están mejorando el flujo.",
                TipoMensajeNarrador.ANALISIS
            )
        
        # Analizar estabilidad de velocidad
        velocidades = [h['velocidad'] for h in ultimas]
        variacion = max(velocidades) - min(velocidades)
        if variacion < 0.2:  # Muy estable
            self.narrador.agregar_mensaje(
                f"SISTEMA ESTABLE: La velocidad promedio se mantiene constante ({velocidades[-1]:.1f}km/h). " +
                "Indica un funcionamiento equilibrado del sistema.",
                TipoMensajeNarrador.ANALISIS
            )
    
    def _guardar_estadisticas_historial(self, tiempo: float, vehiculos: int, estadisticas: dict, hora_sim: float):
        """Guarda estadísticas para análisis histórico"""
        entrada = {
            'tiempo': tiempo,
            'vehiculos': vehiculos,
            'velocidad': estadisticas['promedio_velocidad'],
            'congestion': estadisticas['congestion'],
            'hora_sim': hora_sim,
            'distribucion_vehiculos': {
                'autos': estadisticas.get('autos', 0),
                'combis': estadisticas.get('combis', 0),
                'motos': estadisticas.get('motos', 0),
                'taxis': estadisticas.get('taxis', 0)
            }
        }
        
        self.estadisticas_historial.append(entrada)
        
        # Mantener solo las últimas 50 entradas
        if len(self.estadisticas_historial) > 50:
            self.estadisticas_historial.pop(0)
    
    def reporte_final(self, tiempo_total: float, vehiculos_generados: int, estadisticas: dict):
        """Genera reporte final completo de la simulación"""
        print("\n" + "🏁"*40)
        print("REPORTE FINAL DE SIMULACIÓN")
        print("🏁"*40)
        
        # Información básica
        print(f"\n⏱️  DURACIÓN TOTAL: {tiempo_total:.1f} segundos ({tiempo_total/60:.1f} minutos)")
        print(f"🚗 VEHÍCULOS GENERADOS: {vehiculos_generados}")
        print(f"📊 TASA DE GENERACIÓN: {(vehiculos_generados / tiempo_total) * 60:.1f} vehículos/minuto")
        print(f"📝 EVENTOS TOTALES REGISTRADOS: {self.total_eventos}")
        
        # Análisis de rendimiento
        if self.estadisticas_historial:
            velocidades = [h['velocidad'] for h in self.estadisticas_historial]
            congestiones = [h['congestion'] for h in self.estadisticas_historial]
            
            print(f"\n📈 ANÁLISIS DE RENDIMIENTO:")
            print(f"   ├─ Velocidad promedio: {sum(velocidades)/len(velocidades):.2f} km/h")
            print(f"   ├─ Velocidad máxima: {max(velocidades):.2f} km/h")
            print(f"   ├─ Velocidad mínima: {min(velocidades):.2f} km/h")
            print(f"   ├─ Congestión promedio: {sum(congestiones)/len(congestiones):.1f}%")
            print(f"   ├─ Congestión máxima: {max(congestiones):.1f}%")
            print(f"   └─ Congestión mínima: {min(congestiones):.1f}%")
        
        # Top eventos
        if self.eventos_por_tipo:
            print(f"\n🔢 EVENTOS MÁS FRECUENTES:")
            eventos_ordenados = sorted(self.eventos_por_tipo.items(), key=lambda x: x[1], reverse=True)
            for i, (evento, cantidad) in enumerate(eventos_ordenados[:5]):
                print(f"   {i+1}. {evento}: {cantidad} veces")
        
        # Distribución final de vehículos
        total_vehiculos = sum([estadisticas.get('autos', 0), estadisticas.get('combis', 0), 
                              estadisticas.get('motos', 0), estadisticas.get('taxis', 0)])
        
        if total_vehiculos > 0:
            print(f"\n🚙 DISTRIBUCIÓN FINAL DE VEHÍCULOS:")
            tipos = ['autos', 'combis', 'motos', 'taxis']
            for tipo in tipos:
                cantidad = estadisticas.get(tipo, 0)
                porcentaje = (cantidad / total_vehiculos * 100) if total_vehiculos > 0 else 0
                print(f"   ├─ {tipo.capitalize()}: {cantidad} ({porcentaje:.1f}%)")
        
        # Clasificación final
        congestion_final = estadisticas.get('congestion', 0)
        if congestion_final < 30:
            clasificacion = "🟢 EXCELENTE - Tráfico muy fluido"
        elif congestion_final < 50:
            clasificacion = "🟡 BUENO - Tráfico con fluidez normal"
        elif congestion_final < 70:
            clasificacion = "🟠 REGULAR - Tráfico con cierta congestión"
        else:
            clasificacion = "🔴 CRÍTICO - Tráfico muy congestionado"
        
        print(f"\n🏆 CLASIFICACIÓN FINAL: {clasificacion}")
        
        # Mensaje final del narrador
        self.narrador.agregar_mensaje(
            f"Simulación finalizada. Duración: {tiempo_total:.1f}s, " +
            f"Vehículos generados: {vehiculos_generados}, " +
            f"Eventos registrados: {self.total_eventos}",
            TipoMensajeNarrador.ANALISIS
        )
        
        print("🏁"*40)
    
    def obtener_estadisticas_logger(self) -> dict:
        """Retorna estadísticas del sistema de logging"""
        return {
            'total_eventos': self.total_eventos,
            'eventos_por_tipo': self.eventos_por_tipo.copy(),
            'alertas_activas': len(self.alertas_activas),
            'entradas_historial': len(self.estadisticas_historial),
            'tiempo_funcionamiento': time.time() - (self.estadisticas_historial[0]['tiempo'] 
                                                   if self.estadisticas_historial else time.time())
        }