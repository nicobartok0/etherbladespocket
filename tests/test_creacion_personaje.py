"""
Tests para el servicio de creación de personajes.
Ejecutar con: pytest tests/test_creacion_personaje.py -v
"""
import pytest
from unittest.mock import patch, MagicMock
from servicios.creacion_personaje_service import CreacionPersonajeService
from entidades import HephixTipo, ClaseTipo, Constantes


class TestCreacionPersonajeService:
    """Tests para el servicio de creación"""
    
    @pytest.fixture
    def servicio(self):
        """Crea una instancia del servicio"""
        return CreacionPersonajeService()
    
    def test_cargar_datos(self, servicio):
        """Verifica que se cargan los datos de clases y hephix"""
        assert len(servicio.clases_data) > 0
        assert len(servicio.hephix_data) > 0
        
        # Verificar que existen clases específicas
        assert 'curandero' in servicio.clases_data
        assert 'guerrero' in servicio.clases_data
        
        # Verificar que existen hephix específicos
        assert 'elemental' in servicio.hephix_data
        assert 'sangrienta' in servicio.hephix_data
    
    def test_solicitar_numero_valido(self, servicio):
        """Verifica validación de números"""
        with patch('builtins.input', return_value='5'):
            resultado = servicio._solicitar_numero("Test: ", 1, 10)
            assert resultado == 5
    
    def test_solicitar_numero_fuera_rango(self, servicio):
        """Verifica rechazo de números fuera de rango"""
        with patch('builtins.input', side_effect=['15', '0', '5']):
            resultado = servicio._solicitar_numero("Test: ", 1, 10)
            assert resultado == 5
    
    def test_solicitar_numero_invalido(self, servicio):
        """Verifica rechazo de entrada no numérica"""
        with patch('builtins.input', side_effect=['abc', '5']):
            resultado = servicio._solicitar_numero("Test: ", 1, 10)
            assert resultado == 5
    
    def test_distribuir_caracteristicas_suma_correcta(self, servicio):
        """Verifica que la distribución no exceda 20 puntos"""
        inputs = ['8', '4', '6', '0', '0', '2']  # Total = 20
        
        with patch('builtins.input', side_effect=inputs):
            carac = servicio._distribuir_caracteristicas()
            
            assert carac.total_puntos() == 20
            assert carac.fuerza == 8
            assert carac.reflejos == 4
            assert carac.resistencia == 6
    
    def test_distribuir_combate(self, servicio):
        """Verifica distribución de habilidades de combate"""
        inputs = ['5', '0', '0', '5', '0']  # Total = 10
        
        with patch('builtins.input', side_effect=inputs):
            combate = servicio._distribuir_combate()
            
            assert combate.total_puntos() == 10
            assert combate.armas_cortantes == 5
            assert combate.armas_distancia == 5
    
    def test_distribuir_educacion(self, servicio):
        """Verifica distribución de habilidades de educación"""
        inputs = ['3', '3', '2', '2']  # Total = 10
        
        with patch('builtins.input', side_effect=inputs):
            educacion = servicio._distribuir_educacion()
            
            assert educacion.total_puntos() == 10
    
    def test_distribuir_talento(self, servicio):
        """Verifica distribución de habilidades de talento"""
        inputs = ['4', '4', '2', '0']  # Total = 10
        
        with patch('builtins.input', side_effect=inputs):
            talento = servicio._distribuir_talento()
            
            assert talento.total_puntos() == 10
    
    def test_paso_datos_basicos(self, servicio):
        """Verifica paso de datos básicos"""
        inputs = ['Aldric', '25', 'Humano']
        
        with patch('builtins.input', side_effect=inputs):
            nombre, edad, raza = servicio._paso_datos_basicos()
            
            assert nombre == 'Aldric'
            assert edad == 25
            assert raza == 'Humano'
    
    def test_paso_historia(self, servicio):
        """Verifica paso de historia"""
        inputs = [
            'Un guerrero de las montañas buscando venganza',  # historia
            'Vengar a su familia'                              # objetivo
        ]
        
        with patch('builtins.input', side_effect=inputs):
            historia, objetivo = servicio._paso_historia()
            
            assert 'guerrero' in historia.lower()
            assert len(objetivo) > 0
    
    def test_paso_seleccion_hephix(self, servicio):
        """Verifica selección de hephix"""
        with patch('builtins.input', return_value='1'):  # Elemental
            hephix = servicio._paso_seleccion_hephix()
            
            assert hephix.tipo == HephixTipo.ELEMENTAL
            assert hephix.nivel == 1
    
    def test_paso_seleccion_clase(self, servicio):
        """Verifica selección de clase"""
        with patch('builtins.input', return_value='2'):  # Guerrero (segunda opción)
            clase = servicio._paso_seleccion_clase()
            
            assert clase in ClaseTipo
    
    def test_equipamiento_inicial_guerrero(self, servicio):
        """Verifica equipamiento inicial para guerrero"""
        from entidades import Personaje, Ficha, Hephix
        
        ficha = Ficha()
        ficha.combate.armas_cortantes = 10  # Suficiente para espada
        
        personaje = Personaje(
            nombre="Test",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
        
        servicio._paso_equipamiento_inicial(personaje, ClaseTipo.GUERRERO)
        
        assert personaje.arma_equipada is not None
        assert personaje.inventario.monedas == 100
    
    @pytest.mark.integration
    def test_creacion_completa_programatica(self, servicio):
        """
        Test de integración: crea un personaje completo sin interacción.
        Usa el método no interactivo para evitar problemas con mocks.
        """
        personaje = servicio.crear_personaje(
            nombre="Aldric",
            edad=25,
            raza="Humano",
            historia="Un guerrero valiente de las montañas del norte",
            objetivo="Proteger a los débiles y buscar justicia",
            hephix_tipo=HephixTipo.ELEMENTAL,
            clase=ClaseTipo.GUERRERO,
            caracteristicas={
                "fuerza": 8,
                "reflejos": 4,
                "resistencia": 6,
                "voluntad": 0,
                "punteria": 0,
                "stamina": 2
            },
            habilidades_combate={
                "armas_cortantes": 10,
                "armas_contundentes": 0,
                "armas_magicas": 0,
                "armas_distancia": 0,
                "pugilismo": 0
            },
            habilidades_educacion={
                "medicina": 5,
                "elocuencia": 5,
                "manual": 0,
                "arcanismo": 0
            },
            habilidades_talento={
                "sigilo": 5,
                "percepcion": 5,
                "mentalidad": 0,
                "astralidad": 0
            }
        )
        
        # Verificaciones básicas
        assert personaje.nombre == 'Aldric'
        assert personaje.edad == 25
        assert personaje.raza == 'Humano'
        assert personaje.nivel == 1
        assert personaje.clase == ClaseTipo.GUERRERO
        assert personaje.hephix.tipo == HephixTipo.ELEMENTAL
        
        # Verificar distribución de puntos
        assert personaje.ficha.caracteristicas.total_puntos() == 20
        assert personaje.ficha.combate.total_puntos() >= 10  # + bonificaciones clase
        
        # Verificar historia
        assert 'guerrero' in personaje.historia.lower()
        assert 'proteger' in personaje.objetivo.lower()
        
        # Verificar inicialización
        assert personaje.pv_actuales == personaje.pv_maximos
        assert personaje.pm_actuales == personaje.pm_maximos
        assert personaje.esta_vivo
        
        # Verificar equipamiento
        assert personaje.inventario.monedas == 100
        assert personaje.arma_equipada is not None  # Guerrero con armas_cortantes=10
        assert personaje.arma_equipada.nombre == "Espada Corta"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])