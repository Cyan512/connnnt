"""
Generador del mapa del centro histórico del Cusco
src/mapa_cusco.py
"""

from typing import List, Tuple
from src.models import Punto, Calle, Edificio
from src.enums import DireccionCalle, TipoEdificio
from src.constants import ANCHO, ALTO

class GeneradorMapaCusco:
    """Clase responsable de generar el mapa detallado de Cusco"""
    
    def __init__(self):
        self.calles: List[Calle] = []
        self.edificios: List[Edificio] = []
        self.landmarks: List[Tuple[str, int, int]] = []
        
    def generar_mapa_completo(self) -> Tuple[List[Calle], List[Edificio], List[Tuple[str, int, int]]]:
        """
        Genera el mapa completo del centro histórico de Cusco
        
        Returns:
            Tupla con (calles, edificios, landmarks)
        """
        self._crear_avenidas_principales()
        self._crear_calles_transversales()
        self._crear_calles_historicas()
        self._crear_calles_secundarias()
        self._crear_calles_barrios()
        
        self._crear_edificios_principales()
        self._crear_plazas_y_espacios()
        self._definir_landmarks()
        
        return self.calles, self.edificios, self.landmarks
    
    def _crear_avenidas_principales(self):
        """Crea las avenidas principales de Cusco"""
        # Av. El Sol - arteria principal este-oeste
        self.calles.extend([
            Calle(Punto(0, 400), Punto(ANCHO, 400), 45, 'principal', DireccionCalle.HORIZONTAL, 3.0),
            Calle(Punto(ANCHO, 425), Punto(0, 425), 45, 'principal', DireccionCalle.HORIZONTAL, 3.0),
        ])
        
        # Av. de la Cultura - norte-sur principal
        self.calles.extend([
            Calle(Punto(800, 0), Punto(800, ALTO), 40, 'principal', DireccionCalle.VERTICAL, 2.8),
            Calle(Punto(825, ALTO), Punto(825, 0), 40, 'principal', DireccionCalle.VERTICAL, 2.8),
        ])
        
        # Av. Garcilaso - paralela a El Sol
        self.calles.extend([
            Calle(Punto(0, 200), Punto(ANCHO, 200), 40, 'principal', DireccionCalle.HORIZONTAL, 2.8),
            Calle(Punto(ANCHO, 225), Punto(0, 225), 40, 'principal', DireccionCalle.HORIZONTAL, 2.8),
        ])
        
        # Av. Túpac Amaru
        self.calles.extend([
            Calle(Punto(0, 600), Punto(ANCHO, 600), 40, 'principal', DireccionCalle.HORIZONTAL, 2.8),
            Calle(Punto(ANCHO, 625), Punto(0, 625), 40, 'principal', DireccionCalle.HORIZONTAL, 2.8),
        ])
    
    def _crear_calles_transversales(self):
        """Crea las calles transversales principales"""
        calles_transversales = [
            (300, 'Av. Ejercito'),
            (500, 'Av. Huáscar'),
            (1100, 'Av. Pardo'),
            (1300, 'Av. de los Incas')
        ]
        
        for x, nombre in calles_transversales:
            self.calles.extend([
                Calle(Punto(x, 0), Punto(x, ALTO), 35, 'principal', DireccionCalle.VERTICAL, 2.5),
                Calle(Punto(x + 25, ALTO), Punto(x + 25, 0), 35, 'principal', DireccionCalle.VERTICAL, 2.5),
            ])
    
    def _crear_calles_historicas(self):
        """Crea las calles históricas del centro"""
        calles_historicas = [
            # Zona Plaza de Armas
            Calle(Punto(200, 320), Punto(900, 340), 22, 'empedrada', DireccionCalle.HORIZONTAL, 1.5),  # Plateros
            Calle(Punto(900, 360), Punto(200, 380), 22, 'empedrada', DireccionCalle.HORIZONTAL, 1.5),
            Calle(Punto(250, 280), Punto(850, 300), 20, 'empedrada', DireccionCalle.HORIZONTAL, 1.2),  # Procuradores
            Calle(Punto(350, 450), Punto(650, 450), 18, 'empedrada', DireccionCalle.HORIZONTAL, 1.0),  # Portal de Panes
            Calle(Punto(350, 500), Punto(650, 500), 18, 'empedrada', DireccionCalle.HORIZONTAL, 1.0),  # Portal Comercio
            
            # Calles verticales históricas
            Calle(Punto(400, 520), Punto(400, 720), 16, 'empedrada', DireccionCalle.VERTICAL, 1.0),    # Loreto
            Calle(Punto(600, 480), Punto(600, 650), 15, 'empedrada', DireccionCalle.VERTICAL, 0.8),   # Santa Catalina
            
            # Cuesta San Blas (serpenteante)
            Calle(Punto(650, 300), Punto(750, 500), 25, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
            Calle(Punto(750, 500), Punto(850, 600), 25, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
            
            # Zona San Pedro
            Calle(Punto(150, 700), Punto(400, 720), 20, 'empedrada', DireccionCalle.HORIZONTAL, 1.2),
            Calle(Punto(150, 750), Punto(350, 770), 20, 'empedrada', DireccionCalle.HORIZONTAL, 1.2),
        ]
        
        self.calles.extend(calles_historicas)
    
    def _crear_calles_secundarias(self):
        """Crea la red de calles secundarias"""
        # Calles horizontales secundarias
        y_coords = [100, 300, 500, 700, 800]
        for y in y_coords:
            ancho = 30 if y in [100, 700] else 28
            self.calles.append(
                Calle(Punto(0, y), Punto(ANCHO, y), ancho, 'secundaria', DireccionCalle.HORIZONTAL, 2.0)
            )
        
        # Calles verticales secundarias
        x_coords = [100, 200, 600, 700, 900, 1000, 1200, 1400]
        for x in x_coords:
            self.calles.append(
                Calle(Punto(x, 0), Punto(x, ALTO), 25, 'secundaria', DireccionCalle.VERTICAL, 1.8)
            )
        
        # Calles diagonales (características del Cusco)
        diagonales = [
            (Punto(400, 150), Punto(800, 350)),
            (Punto(900, 150), Punto(1200, 400)),
            (Punto(200, 600), Punto(500, 800)),
            (Punto(1000, 600), Punto(1300, 850))
        ]
        
        for inicio, fin in diagonales:
            self.calles.append(
                Calle(inicio, fin, 22, 'secundaria', DireccionCalle.DIAGONAL, 1.8)
            )
    
    def _crear_calles_barrios(self):
        """Crea calles específicas de barrios característicos"""
        # San Blas (calles empedradas y estrechas)
        calles_san_blas = [
            Calle(Punto(700, 100), Punto(950, 150), 18, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
            Calle(Punto(850, 50), Punto(900, 200), 16, 'empedrada', DireccionCalle.VERTICAL, 0.8),
            Calle(Punto(950, 100), Punto(1100, 180), 18, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
        ]
        
        # Santa Ana
        calles_santa_ana = [
            Calle(Punto(100, 150), Punto(250, 180), 20, 'empedrada', DireccionCalle.HORIZONTAL, 1.2),
            Calle(Punto(50, 200), Punto(200, 250), 18, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
        ]
        
        # Santiago
        calles_santiago = [
            Calle(Punto(1200, 700), Punto(1500, 750), 24, 'secundaria', DireccionCalle.HORIZONTAL, 1.8),
            Calle(Punto(1350, 650), Punto(1400, 850), 22, 'secundaria', DireccionCalle.VERTICAL, 1.6),
        ]
        
        self.calles.extend(calles_san_blas + calles_santa_ana + calles_santiago)
    
    def _crear_edificios_principales(self):
        """Crea los edificios y estructuras principales"""
        edificios_principales = [
            # Centro Histórico Principal
            Edificio(400, 480, 140, 140, TipoEdificio.CATEDRAL.value, "Catedral del Cusco"),
            Edificio(570, 520, 80, 100, TipoEdificio.IGLESIA.value, "La Compañía de Jesús"),
            Edificio(700, 450, 100, 90, TipoEdificio.TEMPLO.value, "Qorikancha"),
            
            # Barrio San Blas
            Edificio(800, 100, 100, 120, TipoEdificio.COLONIAL.value, "Casa Colonial San Blas"),
            Edificio(920, 120, 80, 100, TipoEdificio.COLONIAL.value),
            Edificio(750, 200, 90, 110, TipoEdificio.IGLESIA.value, "Iglesia San Blas"),
            
            # Zona Santa Ana
            Edificio(120, 150, 100, 140, TipoEdificio.COLONIAL.value),
            Edificio(80, 250, 90, 80, TipoEdificio.IGLESIA.value, "Iglesia Santa Ana"),
            
            # Zona San Pedro
            Edificio(80, 720, 200, 120, TipoEdificio.MERCADO.value, "Mercado San Pedro"),
            Edificio(150, 650, 120, 80, TipoEdificio.COLONIAL.value),
            
            # Zona Santiago
            Edificio(1250, 750, 150, 120, TipoEdificio.COLONIAL.value),
            Edificio(1350, 680, 100, 90, TipoEdificio.IGLESIA.value, "Iglesia Santiago"),
            
            # Edificios modernos en avenidas principales
            Edificio(1200, 100, 100, 180, TipoEdificio.MODERNO.value),
            Edificio(1400, 200, 120, 200, TipoEdificio.MODERNO.value),
            Edificio(100, 800, 150, 160, TipoEdificio.MODERNO.value),
            Edificio(1300, 800, 140, 150, TipoEdificio.MODERNO.value),
            
            # Edificios coloniales distribuidos
            Edificio(300, 150, 120, 160, TipoEdificio.COLONIAL.value),
            Edificio(500, 120, 100, 140, TipoEdificio.COLONIAL.value),
            Edificio(600, 200, 80, 120, TipoEdificio.COLONIAL.value),
            Edificio(900, 300, 110, 150, TipoEdificio.COLONIAL.value),
            Edificio(1100, 350, 90, 130, TipoEdificio.COLONIAL.value),
            Edificio(200, 700, 100, 120, TipoEdificio.COLONIAL.value),
            Edificio(400, 750, 100, 120, TipoEdificio.COLONIAL.value),
            Edificio(800, 720, 120, 140, TipoEdificio.COLONIAL.value),
            Edificio(1000, 750, 100, 110, TipoEdificio.COLONIAL.value),
        ]
        
        self.edificios.extend(edificios_principales)
    
    def _crear_plazas_y_espacios(self):
        """Crea plazas y espacios públicos"""
        # Plaza de Armas (espacio abierto, se maneja en el dibujo)
        # Plaza San Francisco
        # Plaza Regocijo
        # Estos se manejan como espacios especiales en el renderizado
        pass
    
    def _definir_landmarks(self):
        """Define puntos de referencia con nombres"""
        self.landmarks = [
            ("PLAZA DE ARMAS", 440, 460),
            ("CATEDRAL", 420, 450),
            ("AV. EL SOL", 20, 380),
            ("AV. DE LA CULTURA", 720, 50),
            ("AV. GARCILASO", 20, 180),
            ("AV. TUPAC AMARU", 20, 580),
            ("SAN BLAS", 820, 80),
            ("SANTA ANA", 80, 130),
            ("SAN PEDRO", 100, 700),
            ("SANTIAGO", 1280, 730),
            ("QORIKANCHA", 720, 430),
            ("MERCADO SAN PEDRO", 90, 680),
            ("LA COMPAÑIA", 590, 500),
            ("PLAZA SAN FRANCISCO", 180, 380),
            ("CUESTA SAN BLAS", 720, 400),
        ]
    
    def obtener_intersecciones_principales(self) -> List[Tuple[Punto, str]]:
        """Retorna las intersecciones principales para semáforos"""
        intersecciones = []
        
        # Intersecciones de avenidas principales
        avenidas_x = [300, 500, 800, 1100, 1300]
        avenidas_y = [200, 400, 600]
        
        for x in avenidas_x:
            for y in avenidas_y:
                tipo = 'principal' if (x == 800 and y == 400) else 'principal'  # Cruce principal
                intersecciones.append((Punto(x, y), tipo))
        
        return intersecciones
    
    def obtener_intersecciones_secundarias(self) -> List[Tuple[Punto, str]]:
        """Retorna intersecciones secundarias para semáforos"""
        intersecciones = []
        
        # Calles secundarias con principales
        secundarias_x = [100, 200, 600, 700, 900, 1000, 1200, 1400]
        principales_y = [200, 400, 600]
        
        for x in secundarias_x:
            for y in principales_y:
                intersecciones.append((Punto(x, y), 'normal'))
        
        # Intersecciones en calles transversales
        principales_x = [300, 500, 800, 1100]
        secundarias_y = [100, 300, 500, 700, 800]
        
        for x in principales_x:
            for y in secundarias_y:
                intersecciones.append((Punto(x, y), 'normal'))
        
        return intersecciones
    
    def obtener_intersecciones_historicas(self) -> List[Tuple[Punto, str]]:
        """Retorna intersecciones en zona histórica"""
        return [
            (Punto(400, 320), 'normal'),    # Plateros
            (Punto(600, 340), 'normal'),    # Plateros
            (Punto(350, 450), 'normal'),    # Portal de Panes
            (Punto(400, 520), 'normal'),    # Calle Loreto
            (Punto(600, 500), 'normal'),    # Santa Catalina
            (Punto(700, 350), 'normal'),    # San Blas
            (Punto(200, 720), 'normal'),    # San Pedro
        ]
    
    def obtener_puntos_generacion(self) -> List[Punto]:
        """Retorna puntos estratégicos para generación de vehículos"""
        return [
            # Entradas principales
            Punto(0, 400),      # Entrada oeste Av. El Sol
            Punto(ANCHO, 400),  # Entrada este Av. El Sol
            Punto(800, 0),      # Entrada norte Av. Cultura
            Punto(800, ALTO),   # Entrada sur Av. Cultura
            
            # Puntos secundarios
            Punto(0, 200),      # Av. Garcilaso oeste
            Punto(ANCHO, 200),  # Av. Garcilaso este
            Punto(300, 0),      # Av. Ejercito norte
            Punto(300, ALTO),   # Av. Ejercito sur
        ]
    
    def validar_mapa(self) -> bool:
        """Valida que el mapa generado sea consistente"""
        # Verificar que hay calles
        if not self.calles:
            return False
        
        # Verificar que las calles tienen dimensiones válidas
        for calle in self.calles:
            if calle.ancho <= 0 or calle.velocidad_maxima <= 0:
                return False
            if calle.longitud <= 0:
                return False
        
        # Verificar que hay edificios
        if not self.edificios:
            return False
        
        # Verificar que hay landmarks
        if not self.landmarks:
            return False
        
        return True