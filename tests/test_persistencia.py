"""
Tests para el servicio de persistencia.
Ejecutar con: pytest tests/test_persistencia.py -v
"""
import pytest
import shutil
from pathlib import Path
from servicios.persistencia_service import PersistenciaService
from servicios.persistencia_estructuras import (
    ContextoNarrativo, EventoNarrativo, TipoEvento
)
from entidades import Personaje, Ficha, Hephix, HephixTipo, ClaseTipo
from patrones import SingletonMeta


class TestPersistenciaService:
    """Tests para el servicio de persistencia"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup y teardown para cada test"""
        # Usar directorio temporal para tests
        self.test_dir = Path("guardados_test")
        self.test_dir.mkdir(exist_ok=True)
        
        # Reset singleton antes de cada test
        SingletonMeta.reset_instances()
        
        yield
        
        # Limpiar después de cada test
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @pytest.fixture
    def servicio(self):
        """Crea un servicio de persistencia para testing"""
        return PersistenciaService(directorio_guardados=str(self.test_dir))
    
    @pytest.fixture
    def personaje_prueba(self):
        """Crea un personaje de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.stamina = 3
        
        return Personaje(
            nombre="Aldric Test",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha,
            historia="Un guerrero de prueba"
        )
    
    @pytest.fixture
    def contexto_prueba(self):
        """Crea un contexto de prueba"""
        contexto = ContextoNarrativo(
            checkpoint_actual="test_checkpoint",
            ubicacion_actual="Zona de Test"
        )
        contexto.npcs_conocidos.append("NPC Test")
        contexto.agregar_evento(EventoNarrativo(
            tipo=TipoEvento.COMBATE,
            descripcion="Combate de prueba",
            relevancia="alta"
        ))
        return contexto
    
    # ========================================================================
    # Tests de Singleton
    # ========================================================================
    
    def test_singleton_misma_instancia(self):
        """Verifica que siempre retorna la misma instancia"""
        servicio1 = PersistenciaService(directorio_guardados=str(self.test_dir))
        servicio2 = PersistenciaService(directorio_guardados=str(self.test_dir))
        
        assert servicio1 is servicio2
    
    # ========================================================================
    # Tests de Guardado
    # ========================================================================
    
    def test_guardar_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se guarda correctamente una partida"""
        archivo = servicio.guardar_partida(
            personaje_prueba,
            contexto_prueba,
            slot=1,
            nombre_partida="Partida de Prueba"
        )
        
        assert archivo.exists()
        assert archivo.name == "slot_01.json"
    
    def test_guardar_slot_invalido(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que rechaza slots inválidos"""
        with pytest.raises(ValueError, match="debe estar entre 1 y 10"):
            servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=0)
        
        with pytest.raises(ValueError, match="debe estar entre 1 y 10"):
            servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=11)
    
    def test_sobrescribir_slot(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se puede sobrescribir un slot"""
        # Guardar primera vez
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        # Modificar personaje
        personaje_prueba.nivel = 5
        
        # Guardar de nuevo en el mismo slot
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        # Verificar que se sobrescribió
        datos = servicio.cargar_partida(1)
        assert datos.personaje['nivel'] == 5
    
    def test_autoguardar(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica funcionamiento del autoguardado"""
        archivo = servicio.autoguardar(personaje_prueba, contexto_prueba, slot=2)
        
        assert archivo.exists()
        assert servicio.existe_partida(2)
    
    # ========================================================================
    # Tests de Carga
    # ========================================================================
    
    def test_cargar_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se carga correctamente una partida"""
        # Guardar
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        # Cargar
        datos = servicio.cargar_partida(1)
        
        assert datos.personaje['nombre'] == "Aldric Test"
        assert datos.contexto.ubicacion_actual == "Zona de Test"
        assert datos.slot == 1
    
    def test_cargar_slot_vacio(self, servicio):
        """Verifica error al cargar slot vacío"""
        with pytest.raises(FileNotFoundError, match="está vacío"):
            servicio.cargar_partida(3)
    
    def test_cargar_personaje(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se puede cargar solo el personaje"""
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        personaje_cargado = servicio.cargar_personaje(1)
        
        assert personaje_cargado.nombre == personaje_prueba.nombre
        assert personaje_cargado.nivel == personaje_prueba.nivel
        assert personaje_cargado.clase == personaje_prueba.clase
    
    def test_cargar_contexto(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se puede cargar solo el contexto"""
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        contexto_cargado = servicio.cargar_contexto(1)
        
        assert contexto_cargado.ubicacion_actual == contexto_prueba.ubicacion_actual
        assert contexto_cargado.checkpoint_actual == contexto_prueba.checkpoint_actual
        assert len(contexto_cargado.npcs_conocidos) > 0
    
    def test_integridad_datos_cargados(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que todos los datos se preservan correctamente"""
        # Configurar personaje con datos específicos
        personaje_prueba.nivel = 10
        personaje_prueba.experiencia = 5000
        personaje_prueba.pv_actuales = 50
        personaje_prueba.inventario.agregar_monedas(500)
        
        # Configurar contexto
        contexto_prueba.reputacion["Faccion Test"] = 25
        contexto_prueba.misiones_activas.append("Mision Test")
        
        # Guardar y cargar
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        personaje_cargado = servicio.cargar_personaje(1)
        contexto_cargado = servicio.cargar_contexto(1)
        
        # Verificar personaje
        assert personaje_cargado.nivel == 10
        assert personaje_cargado.experiencia == 5000
        assert personaje_cargado.pv_actuales == 50
        assert personaje_cargado.inventario.monedas == 500
        
        # Verificar contexto
        assert contexto_cargado.reputacion["Faccion Test"] == 25
        assert "Mision Test" in contexto_cargado.misiones_activas
    
    # ========================================================================
    # Tests de Gestión de Slots
    # ========================================================================
    
    def test_listar_partidas_vacio(self, servicio):
        """Verifica listado cuando no hay partidas"""
        slots = servicio.listar_partidas()
        
        assert len(slots) == 10
        assert all(not slot.existe for slot in slots)
    
    def test_listar_partidas_con_guardados(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica listado con partidas guardadas"""
        # Guardar en slots 1, 3 y 5
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=3)
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=5)
        
        slots = servicio.listar_partidas()
        
        assert slots[0].existe  # Slot 1
        assert not slots[1].existe  # Slot 2
        assert slots[2].existe  # Slot 3
        assert not slots[3].existe  # Slot 4
        assert slots[4].existe  # Slot 5
    
    def test_existe_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica detección de existencia de partida"""
        assert not servicio.existe_partida(1)
        
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        assert servicio.existe_partida(1)
    
    def test_eliminar_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica eliminación de partida"""
        # Guardar
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        assert servicio.existe_partida(1)
        
        # Eliminar
        resultado = servicio.eliminar_partida(1)
        
        assert resultado is True
        assert not servicio.existe_partida(1)
    
    def test_eliminar_partida_inexistente(self, servicio):
        """Verifica que eliminar partida inexistente retorna False"""
        resultado = servicio.eliminar_partida(5)
        assert resultado is False
    
    # ========================================================================
    # Tests de Tiempo de Juego
    # ========================================================================
    
    def test_tracking_tiempo_jugado(self, servicio):
        """Verifica tracking de tiempo de juego"""
        servicio.iniciar_sesion()
        
        # Simular algo de tiempo (no podemos esperar realmente)
        tiempo = servicio.obtener_tiempo_jugado()
        
        assert tiempo.total_seconds() >= 0
    
    def test_pausar_sesion(self, servicio):
        """Verifica pausa de sesión"""
        servicio.iniciar_sesion()
        servicio.pausar_sesion()
        
        tiempo = servicio.obtener_tiempo_jugado()
        assert tiempo.total_seconds() >= 0
    
    def test_formateo_tiempo(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica formato de tiempo en guardado"""
        servicio.iniciar_sesion()
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        datos = servicio.cargar_partida(1)
        
        # El formato debe ser "Xh Ym"
        assert "h" in datos.tiempo_jugado
        assert "m" in datos.tiempo_jugado
    
    # ========================================================================
    # Tests de Validación
    # ========================================================================
    
    def test_verificar_integridad_ok(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica validación de integridad correcta"""
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        valido, error = servicio.verificar_integridad(1)
        
        assert valido is True
        assert error is None
    
    def test_verificar_integridad_slot_vacio(self, servicio):
        """Verifica detección de slot vacío"""
        valido, error = servicio.verificar_integridad(1)
        
        assert valido is False
        assert "vacío" in error.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])