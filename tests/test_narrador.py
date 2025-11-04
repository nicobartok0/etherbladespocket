"""
Tests para el servicio de narrador.
Ejecutar con: pytest tests/test_narrador.py -v
"""
import pytest
from servicios.narrador_service import NarradorService
from servicios.cliente_ia import ClienteIA, ClienteIAMock
from servicios.persistencia_estructuras import ContextoNarrativo
from entidades import Personaje, Ficha, Hephix, HephixTipo, ClaseTipo
from patrones import EventBus, TipoEvento, SingletonMeta


class TestClienteIA:
    """Tests para el cliente de IA"""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton antes de cada test"""
        SingletonMeta.reset_instances()
        yield
    
    def test_cliente_ia_singleton(self):
        """Verifica que ClienteIA es singleton"""
        cliente1 = ClienteIA()
        cliente2 = ClienteIA()
        
        assert cliente1 is cliente2
    
    def test_cliente_mock_disponible(self):
        """Verifica que el cliente mock está siempre disponible"""
        cliente = ClienteIAMock()
        
        assert cliente.esta_disponible()
    
    def test_cliente_mock_genera_texto(self):
        """Verifica que el mock genera texto"""
        cliente = ClienteIAMock()
        
        respuesta = cliente.generar_texto("Describe un combate")
        
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0
    
    def test_cliente_mock_respuestas_contextuales(self):
        """Verifica que el mock da respuestas según el contexto"""
        cliente = ClienteIAMock()
        
        # Combate
        respuesta_combate = cliente.generar_texto("Narra un ataque en combate")
        assert "combate" in respuesta_combate.lower() or "ataque" in respuesta_combate.lower()
        
        # Exploración
        respuesta_explorar = cliente.generar_texto("Describe explorar una cueva")
        assert "explor" in respuesta_explorar.lower() or "descubr" in respuesta_explorar.lower()
    
    def test_cliente_mock_con_system_message(self):
        """Verifica que el mock acepta system_message"""
        cliente = ClienteIAMock()
        
        respuesta = cliente.generar_texto(
            "Narra algo épico",
            system_message="Eres un narrador épico"
        )
        
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0


class TestNarradorService:
    """Tests para el servicio de narrador"""
    
    @pytest.fixture
    def event_bus(self):
        """Crea un event bus"""
        return EventBus()
    
    @pytest.fixture
    def contexto(self):
        """Crea un contexto narrativo"""
        return ContextoNarrativo(
            ubicacion_actual="Taberna del Dragón",
            checkpoint_actual="taberna_inicio"
        )
    
    @pytest.fixture
    def narrador(self, event_bus, contexto):
        """Crea un narrador con mock"""
        return NarradorService(event_bus, contexto, usar_mock=True)
    
    @pytest.fixture
    def personaje(self):
        """Crea un personaje de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.resistencia = 7
        
        return Personaje(
            nombre="Aldric",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
    
    # ========================================================================
    # Tests de Inicialización
    # ========================================================================
    
    def test_crear_narrador(self, narrador):
        """Verifica creación del narrador"""
        assert narrador is not None
        assert narrador.cliente is not None
        assert narrador.contexto is not None
    
    def test_narrador_usa_mock_por_defecto(self, event_bus, contexto):
        """Verifica que usa mock cuando se solicita"""
        narrador = NarradorService(event_bus, contexto, usar_mock=True)
        
        assert isinstance(narrador.cliente, ClienteIAMock)
    
    def test_system_message_creado(self, narrador):
        """Verifica que se crea el system message"""
        assert narrador.system_message is not None
        assert len(narrador.system_message) > 0
        assert "Ether Blades" in narrador.system_message
    
    # ========================================================================
    # Tests de Suscripción a Eventos
    # ========================================================================
    
    def test_suscripcion_eventos(self, narrador):
        """Verifica que se suscribe a eventos relevantes"""
        event_bus = narrador.event_bus
        
        # Verificar que hay subscriptores para eventos de combate
        assert event_bus.contar_subscriptores(TipoEvento.COMBATE_INICIADO) > 0
        assert event_bus.contar_subscriptores(TipoEvento.ATAQUE_REALIZADO) > 0
        assert event_bus.contar_subscriptores(TipoEvento.GOLPE_GRACIA) > 0
    
    # ========================================================================
    # Tests de Narración de Eventos
    # ========================================================================
    
    def test_narrar_inicio_combate(self, event_bus, narrador, capsys):
        """Verifica narración de inicio de combate"""
        # Publicar evento
        event_bus.publicar(TipoEvento.COMBATE_INICIADO, {
            "combatientes": ["Aldric", "Goblin"]
        })
        
        # Capturar output
        captured = capsys.readouterr()
        
        # Verificar que se generó alguna narración
        assert "INICIO DE COMBATE" in captured.out or len(captured.out) > 0
    
    def test_narrar_ataque(self, event_bus, narrador, capsys):
        """Verifica narración de ataque"""
        event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
            "atacante": "Aldric",
            "defensor": "Goblin"
        })
        
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    
    def test_narrar_golpe_gracia(self, event_bus, narrador, capsys):
        """Verifica narración de golpe de gracia"""
        event_bus.publicar(TipoEvento.GOLPE_GRACIA, {
            "atacante": "Aldric",
            "defensor": "Goblin"
        })
        
        captured = capsys.readouterr()
        assert "GOLPE DE GRACIA" in captured.out or len(captured.out) > 0
    
    def test_narrar_muerte(self, event_bus, narrador, capsys):
        """Verifica narración de muerte"""
        event_bus.publicar(TipoEvento.PERSONAJE_MUERTO, {
            "personaje": "Goblin"
        })
        
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    
    # ========================================================================
    # Tests de Narración Libre
    # ========================================================================
    
    def test_narrar_situacion(self, narrador, personaje):
        """Verifica narración de situación libre"""
        narracion = narrador.narrar_situacion(
            "El personaje encuentra una puerta misteriosa",
            personaje
        )
        
        assert isinstance(narracion, str)
        assert len(narracion) > 0
    
    def test_narrar_situacion_sin_personaje(self, narrador):
        """Verifica narración sin personaje"""
        narracion = narrador.narrar_situacion(
            "Una tormenta se avecina"
        )
        
        assert isinstance(narracion, str)
        assert len(narracion) > 0
    
    def test_narrar_decision(self, narrador, personaje):
        """Verifica narración de decisión"""
        narracion = narrador.narrar_decision(
            "Debes elegir entre dos caminos",
            ["Camino de la luz", "Camino de la oscuridad"],
            personaje
        )
        
        assert isinstance(narracion, str)
        assert len(narracion) > 0
    
    # ========================================================================
    # Tests de Contexto
    # ========================================================================
    
    def test_actualizar_contexto(self, narrador):
        """Verifica actualización de contexto"""
        nuevo_contexto = ContextoNarrativo(
            ubicacion_actual="Bosque Oscuro",
            checkpoint_actual="bosque_entrada"
        )
        
        narrador.actualizar_contexto(nuevo_contexto)
        
        assert narrador.contexto.ubicacion_actual == "Bosque Oscuro"
        assert narrador.contexto.checkpoint_actual == "bosque_entrada"
    
    def test_contexto_en_narracion(self, narrador, personaje):
        """Verifica que el contexto influye en la narración"""
        # Actualizar contexto
        contexto = ContextoNarrativo(
            ubicacion_actual="Catacumbas Malditas"
        )
        narrador.actualizar_contexto(contexto)
        
        # Narrar algo
        narracion = narrador.narrar_situacion(
            "Exploras el lugar",
            personaje
        )
        
        # La narración debería existir
        assert len(narracion) > 0
    
    # ========================================================================
    # Tests de Manejo de Errores
    # ========================================================================
    
    def test_narrar_con_datos_incompletos(self, event_bus, narrador, capsys):
        """Verifica manejo de datos incompletos"""
        # Publicar evento con datos mínimos
        event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {})
        
        # No debería crashear
        captured = capsys.readouterr()
        # Puede tener output o no, pero no debería haber error
    
    # ========================================================================
    # Tests de Integración
    # ========================================================================
    
    @pytest.mark.integration
    def test_flujo_combate_completo(self, event_bus, narrador, capsys):
        """Test de integración: flujo completo de combate narrado"""
        # Inicio
        event_bus.publicar(TipoEvento.COMBATE_INICIADO, {
            "combatientes": ["Héroe", "Villano"]
        })
        
        # Ataques
        event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
            "atacante": "Héroe",
            "defensor": "Villano"
        })
        
        # Golpe de gracia
        event_bus.publicar(TipoEvento.GOLPE_GRACIA, {
            "atacante": "Héroe",
            "defensor": "Villano"
        })
        
        # Muerte
        event_bus.publicar(TipoEvento.PERSONAJE_MUERTO, {
            "personaje": "Villano"
        })
        
        captured = capsys.readouterr()
        
        # Debería haber generado múltiples narraciones
        assert len(captured.out) > 0


class TestIntegracionNarradorCombate:
    """Tests de integración entre narrador y combate"""
    
    @pytest.mark.integration
    def test_narrador_en_combate_real(self):
        """Verifica que el narrador funciona durante un combate"""
        from servicios import CombateService
        
        # Crear personajes
        ficha1 = Ficha()
        ficha1.caracteristicas.fuerza = 8
        ficha1.caracteristicas.resistencia = 7
        ficha1.caracteristicas.stamina = 3
        
        personaje1 = Personaje(
            nombre="Guerrero",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha1
        )
        
        ficha2 = Ficha()
        ficha2.caracteristicas.fuerza = 5
        ficha2.caracteristicas.resistencia = 4
        ficha2.caracteristicas.stamina = 2
        
        personaje2 = Personaje(
            nombre="Goblin",
            edad=10,
            raza="Goblin",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha2
        )
        
        # Crear servicios
        event_bus = EventBus()
        narrador = NarradorService(event_bus, usar_mock=True)
        combate = CombateService(event_bus)
        
        # Iniciar combate (debería generar narración)
        combate.iniciar_combate([personaje1, personaje2])
        
        # Realizar ataque (debería generar narración)
        combate.resolver_ataque(personaje1, personaje2)
        
        # Si llegamos aquí sin errores, la integración funciona
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])