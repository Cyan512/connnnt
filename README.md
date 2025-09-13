# README.md
# Simulación de Tráfico del Cusco con Narrador Inteligente

## Descripción
Simulación avanzada del tráfico vehicular en el centro histórico del Cusco que incluye:
- 🎙️ **Narrador inteligente** que explica el funcionamiento en tiempo real
- 🧠 **IA de comportamiento** para vehículos realistas
- 🗺️ **Mapa detallado** del centro histórico
- 🚦 **Sistema de semáforos** inteligente
- 📊 **Estadísticas** avanzadas en tiempo real

## Estructura del Proyecto
```
traffic_simulation/
├── main.py                    # Archivo principal
├── requirements.txt           # Dependencias
├── README.md                 # Este archivo
├── logs/                     # Archivos de log
└── src/
    ├── __init__.py
    ├── constants.py          # Configuración global
    ├── enums.py              # Tipos y enumeraciones
    ├── models.py             # Clases de datos
    ├── vehiculo.py           # Clase Vehiculo
    ├── semaforo.py           # Clase Semaforo
    ├── narrador.py           # Sistema de narración
    ├── simulacion.py         # Simulación principal
    ├── renderizador.py       # Sistema de renderizado
    ├── mapa_cusco.py         # Generador del mapa
    └── utils/
        ├── __init__.py
        ├── console_logger.py # Sistema de logging
        └── logger_config.py  # Configuración logging
```

## Instalación

1. **Clonar el repositorio**
```bash
git clone <repository_url>
cd traffic_simulation
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la simulación**
```bash
python main.py
```

## Características del Narrador

### 🎙️ Explicaciones en Tiempo Real
- **Técnicas**: Explica algoritmos, IA y física de la simulación
- **Eventos**: Comenta sobre comportamientos de vehículos
- **Análisis**: Detecta patrones y situaciones críticas

### 📊 Análisis Inteligente
- Detección automática de congestión
- Explicación de comportamientos emergentes
- Métricas de rendimiento explicadas

## Controles

| Tecla | Función |
|-------|---------|
| `ESPACIO` | Generar vehículo manualmente |
| `N` | Activar/desactivar narrador |
| `P` | Pausar/reanudar simulación |
| `R` | Reiniciar simulación |
| `T` | Cambiar hora del día |
| `C` | Mostrar/ocultar calles |
| `M` | Cambiar modo de vista |
| `ESC` | Salir |

## Modos de Vista

1. **Normal**: Vista estándar del mapa
2. **Densidad**: Muestra densidad de tráfico por zonas
3. **Velocidad**: Visualiza velocidades de vehículos

## Tipos de Vehículos

- 🚗 **Autos**: Comportamiento moderado
- 🚐 **Combis**: Agresivos, paradas frecuentes
- 🏍️ **Motos**: Muy ágiles, zigzaguean
- 🚕 **Taxis**: Buscan pasajeros

## Patrones Horarios

El sistema simula diferentes patrones de tráfico:
- **Mañana (6-12h)**: Mayor tráfico de autos y combis
- **Tarde (12-18h)**: Pico de tráfico, todos los tipos
- **Noche (18-22h)**: Tráfico moderado
- **Madrugada (22-6h)**: Principalmente taxis

## Logging

El sistema genera logs detallados en:
- `logs/traffic_sim_TIMESTAMP.log`
- `traffic_simulation.log`
- Consola en tiempo real

## Configuración

Personaliza la simulación modificando `src/constants.py`:
- Velocidades de vehículos
- Colores y visualización
- Patrones de tráfico
- Intervalos de reporte

## Arquitectura

### Componentes Principales

1. **SimulacionTrafico**: Controlador principal
2. **NarradorSistema**: Sistema de narración inteligente
3. **Vehiculo**: Entidades con IA de comportamiento
4. **Semaforo**: Control de tráfico inteligente
5. **RenderizadorMapa**: Sistema de visualización
6. **GeneradorMapaCusco**: Creación del mapa realista

### Flujo de Datos

1. **Inicialización**: Se carga el mapa y configuración
2. **Bucle Principal**: 
   - Generación inteligente de vehículos
   - Actualización de entidades
   - Análisis de patrones
   - Narración explicativa
   - Renderizado
3. **Logging**: Registro continuo de eventos

## Características Técnicas

### Sistema de IA
- Algoritmos de pathfinding para rutas
- Comportamiento emergente de vehículos
- Detección de patrones de congestión
- Optimización automática de semáforos

### Renderizado
- 60 FPS con pygame
- Múltiples modos de visualización
- Efectos visuales dinámicos
- Interfaz responsive

### Narrador Inteligente
- Análisis semántico de eventos
- Explicaciones contextuales
- Detección de situaciones críticas
- Educación sobre algoritmos

## Extensibilidad

El sistema está diseñado para ser extensible:

```python
# Agregar nuevo tipo de vehículo
class NuevoVehiculo(Vehiculo):
    def __init__(self, ...):
        # Implementación personalizada
        pass

# Modificar comportamiento del narrador
narrador.agregar_explicacion_personalizada("EVENTO", "Explicación")

# Agregar nuevas métricas
estadisticas.nueva_metrica = valor
```

## Casos de Uso

1. **Educativo**: Entender sistemas complejos y algoritmos
2. **Investigación**: Analizar patrones de tráfico urbano
3. **Planificación**: Simular cambios en infraestructura
4. **Entretenimiento**: Observar comportamientos emergentes

## Limitaciones

- Simulación 2D simplificada
- Modelo físico básico
- Patrones predefinidos (no machine learning)
- Mapa estático

## Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa cambios siguiendo la arquitectura existente
4. Agrega tests si es necesario
5. Crea un pull request

## Licencia

Este proyecto es de código abierto para fines educativos y de investigación.

## Soporte

Para reportar bugs o solicitar features:
- Crear un issue en el repositorio
- Incluir logs relevantes
- Describir pasos para reproducir

---

**Desarrollado con ❤️ para la educación en sistemas complejos e inteligencia artificial**