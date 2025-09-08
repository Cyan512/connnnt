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
        # Av. El Sol
        self.calles.extend([
            Calle(Punto(0, 400), Punto(ANCHO, 400), 45, 'principal', DireccionCalle.HORIZONTAL, 3.0),
            Calle(Punto(ANCHO, 425), Punto(0, 425), 45, 'principal', DireccionCalle.HORIZONTAL, 3.0),
        ])
        
        # Av. de la Cultura
        self.calles.extend([
            Calle(Punto(800, 0), Punto(800, ALTO), 40, 'principal', DireccionCalle.VERTICAL, 2.8),
            Calle(Punto(825, ALTO), Punto(825, 0), 40, 'principal', DireccionCalle.VERTICAL, 2.8),
        ])
        
        # Av. Garcilaso
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
            
            # Cuesta San Blas
            Calle(Punto(650, 300), Punto(750, 500), 25, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
            Calle(Punto(750, 500), Punto(850, 600), 25, 'empedrada', DireccionCalle.DIAGONAL, 1.0),
            
            # Zona San Pedro
            Calle(Punto(150, 700), Punto(400, 720), 20, 'empedrada', DireccionCalle.HORIZONTAL, 1.2),
            Calle(Punto(150, 750), Punto(350, 770), 20, 'empedrada', DireccionCalle.HORIZONTAL, 1.2),
        ]
        
        self.calles.extend(calles_historicas)
    
    def _crear_calles_secundarias(self):
        """Crea la red de calles secundarias"""
        # Calles horizontales secundarias (en pares)
        y_coords = [100, 300, 500, 700, 800]
        for y in y_coords:
            ancho = 30 if y in [100, 700] else 28
            self.calles.extend([
                Calle(Punto(0, y), Punto(ANCHO, y), ancho, 'secundaria', DireccionCalle.HORIZONTAL, 2.0),
                Calle(Punto(ANCHO, y + 25), Punto(0, y + 25), ancho, 'secundaria', DireccionCalle.HORIZONTAL, 2.0),
            ])
        
        # Calles verticales secundarias (en pares)
        x_coords = [100, 200, 600, 700, 900, 1000, 1200, 1400]
        for x in x_coords:
            self.calles.extend([
                Calle(Punto(x, 0), Punto(x, ALTO), 25, 'secundaria', DireccionCalle.VERTICAL, 1.8),
                Calle(Punto(x + 25, ALTO), Punto(x + 25, 0), 25, 'secundaria', DireccionCalle.VERTICAL, 1.8),
            ])
    
    def _crear_calles_barrios(self):
        """Crea calles menores en barrios (ejemplo, opcional para detalle)"""
        # Puedes añadir aquí calles diagonales o pequeñas
        pass
    
    def _crear_edificios_principales(self):
        """Define edificios históricos principales"""
        self.edificios.extend([
            Edificio("Catedral del Cusco", Punto(500, 500), 120, 80, TipoEdificio.HISTORICO),
            Edificio("Templo de la Compañía", Punto(620, 500), 100, 70, TipoEdificio.HISTORICO),
            Edificio("Mercado de San Pedro", Punto(200, 700), 150, 100, TipoEdificio.COMERCIAL),
        ])
    
    def _crear_plazas_y_espacios(self):
        """Define plazas y espacios importantes"""
        self.edificios.append(
            Edificio("Plaza de Armas", Punto(450, 450), 300, 200, TipoEdificio.ESPACIO_ABIERTO)
        )
    
    def _definir_landmarks(self):
        """Agrega landmarks clave para referencia"""
        self.landmarks.extend([
            ("Catedral del Cusco", 500, 500),
            ("Plaza de Armas", 450, 450),
            ("Mercado de San Pedro", 200, 700),
        ])
