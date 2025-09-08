#!/usr/bin/env python3
"""
Simulación de Tráfico del Centro Histórico del Cusco con Narrador Inteligente
Archivo Principal - main.py
"""

import pygame
import sys
import time
from src.simulacion import SimulacionTrafico
from src.utils.logger_config import configurar_logging

def mostrar_bienvenida():
    """Muestra el mensaje de bienvenida del sistema"""
    print("🎙️ SIMULACIÓN INTELIGENTE DE TRÁFICO CON NARRADOR EXPLICATIVO")
    print("=" * 80)
    print("Una simulación avanzada que incluye:")
    print("🧠 IA para comportamientos realistas de vehículos")
    print("🎙️ NARRADOR que explica el funcionamiento en tiempo real")
    print("🗺️ Mapa detallado del centro histórico del Cusco")
    print("🚦 Sistema de semáforos inteligente")
    print("📊 Análisis de datos y estadísticas avanzadas")
    print("⚙️ Motor de simulación con física realista")
    print("")
    print("CARACTERÍSTICAS ESPECIALES DEL NARRADOR:")
    print("💬 Explicaciones técnicas del funcionamiento interno")
    print("📈 Análisis en tiempo real de patrones de tráfico")
    print("🚨 Alertas automáticas de situaciones críticas")
    print("🎯 Detalles sobre algoritmos y toma de decisiones")
    print("📝 Panel visual con mensajes explicativos")
    print("")
    print("CONTROLES PRINCIPALES:")
    print("N - Activar/Desactivar narrador explicativo")
    print("ESPACIO - Generar vehículo | P - Pausar | ESC - Salir")
    print("=" * 80)

def main():
    """Función principal del programa"""
    # Configurar logging
    logger = configurar_logging()
    
    # Verificar pygame
    try:
        pygame.init()
    except Exception as e:
        print(f"❌ Error inicializando pygame: {e}")
        print("Instala pygame: pip install pygame")
        sys.exit(1)
    
    # Mostrar bienvenida
    mostrar_bienvenida()
    
    try:
        # Crear y ejecutar simulación
        simulacion = SimulacionTrafico()
        simulacion.ejecutar()
        
    except KeyboardInterrupt:
        print("\n👋 Simulación terminada por el usuario")
        logger.info("Simulación terminada por interrupción del usuario")
        
    except Exception as e:
        print(f"\n❌ Error en la simulación: {e}")
        logger.error(f"Error crítico en simulación: {e}")
        print("Verifica que pygame esté instalado correctamente")
        
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()