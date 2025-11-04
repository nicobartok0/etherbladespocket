"""
Tests unitarios para los patrones de diseño.
Ejecutar con: pytest tests/test_patrones.py -v
"""
import pytest
from patrones import (
    SingletonMeta, 
    FactoryConRegistro,
    EventBus,
    TipoEvento,
    RegistroEstrategiasAtaque,
    TipoAtaque
)


# ============================================================================
# Tests de Singleton
# ============================================================================

class TestSingleton:
    """Tests para el patrón Singleton"""
    
    def test_singleton_misma_instancia(self):
        """Verifica que siempre retorna la misma instancia"""
        
        class MiSingleton(metaclass=SingletonMeta):
            def __init__(self):
                self.valor = 42
        
        instancia1 = MiSingleton()
        instancia2 = MiSingleton()
        
        assert instancia1 is instancia2
        assert id(instancia1) == id(instancia2)
    
    def test_singleton_comparte_estado(self):
        """Verifica que las instancias comparten estado"""
        
        class Config(metaclass=SingletonMeta):
            def __init__(self):
                self.version = "1.0"
        
        config1 = Config()
        config1.version = "2.0"
        
        config2 = Config()
        assert config2.version == "2.0"
    
    def test_singleton_reset(self):
        """Verifica que se puede resetear para testing"""
        
        class TestSingleton(metaclass=SingletonMeta):
            def __init__(self, valor=0):
                self.valor = valor
        
        inst1 = TestSingleton(10)
        assert inst1.valor == 10
        
        # Reset
        SingletonMeta.reset_instances()
        
        inst2 = TestSingleton(20)
        assert inst2.valor == 20
        assert inst1 is not inst2


# ============================================================================
# Tests de Factory
# ============================================================================

class TestFactory:
    """Tests para el patrón Factory"""
    
    def test_factory_registro(self):
        """Verifica que se pueden registrar y crear tipos"""
        
        class Arma:
            def __init__(self, nombre: str):
                self.nombre = nombre
        
        class Espada(Arma):
            pass
        
        factory = FactoryConRegistro[Arma]()
        factory.registrar("espada", Espada)
        
        arma = factory.crear("espada", nombre="Excalibur")
        assert isinstance(arma, Espada)
        assert arma.nombre == "Excalibur"
    
    def test_factory_tipo_invalido(self):
        """Verifica que lanza error con tipo inválido"""
        
        class Arma:
            pass
        
        factory = FactoryConRegistro[Arma]()
        
        with pytest.raises(ValueError, match="no reconocido"):
            factory.crear("tipo_inexistente")
    
    def test_factory_tipos_disponibles(self):
        """Verifica que lista tipos correctamente"""
        
        class Item:
            pass
        
        factory = FactoryConRegistro[Item]()
        factory.registrar("tipo_a", Item)
        factory.registrar("tipo_b", Item)
        
        tipos = factory.obtener_tipos_disponibles()
        assert "tipo_a" in tipos
        assert "tipo_b" in tipos
        assert len(tipos) == 2


# ============================================================================
# Tests de Observer
# ============================================================================

class TestObserver:
    """Tests para el patrón Observer"""
    
    def test_eventbus_suscripcion(self):
        """Verifica que los callbacks se ejecutan"""
        bus = EventBus()
        
        eventos_recibidos = []
        
        def callback(evento):
            eventos_recibidos.append(evento)
        
        bus.suscribir(TipoEvento.ATAQUE_REALIZADO, callback)
        bus.publicar(TipoEvento.ATAQUE_REALIZADO, {"daño": 10})
        
        assert len(eventos_recibidos) == 1
        assert eventos_recibidos[0].tipo == TipoEvento.ATAQUE_REALIZADO
    
    def test_eventbus_multiples_subscriptores(self):
        """Verifica que múltiples subscriptores reciben el evento"""
        bus = EventBus()
        
        contador1 = []
        contador2 = []
        
        bus.suscribir(TipoEvento.DAÑO_RECIBIDO, lambda e: contador1.append(1))
        bus.suscribir(TipoEvento.DAÑO_RECIBIDO, lambda e: contador2.append(1))
        
        bus.publicar(TipoEvento.DAÑO_RECIBIDO)
        
        assert len(contador1) == 1
        assert len(contador2) == 1
    
    def test_eventbus_desuscripcion(self):
        """Verifica que se puede desuscribir"""
        bus = EventBus()
        
        contador = []
        callback = lambda e: contador.append(1)
        
        bus.suscribir(TipoEvento.TURNO_INICIADO, callback)
        bus.publicar(TipoEvento.TURNO_INICIADO)
        assert len(contador) == 1
        
        bus.desuscribir(TipoEvento.TURNO_INICIADO, callback)
        bus.publicar(TipoEvento.TURNO_INICIADO)
        assert len(contador) == 1  # No aumentó
    
    def test_eventbus_historial(self):
        """Verifica que mantiene historial de eventos"""
        bus = EventBus()
        
        bus.publicar(TipoEvento.COMBATE_INICIADO, {"combatientes": 2})
        bus.publicar(TipoEvento.ATAQUE_REALIZADO, {"daño": 5})
        
        historial = bus.obtener_historial()
        assert len(historial) == 2
        assert historial[0].tipo == TipoEvento.ATAQUE_REALIZADO  # Más reciente
    
    def test_eventbus_pausar(self):
        """Verifica que se puede pausar"""
        bus = EventBus()
        
        contador = []
        bus.suscribir(TipoEvento.NIVEL_SUBIDO, lambda e: contador.append(1))
        
        bus.pausar()
        bus.publicar(TipoEvento.NIVEL_SUBIDO)
        assert len(contador) == 0  # No se ejecutó
        
        bus.reanudar()
        bus.publicar(TipoEvento.NIVEL_SUBIDO)
        assert len(contador) == 1  # Ahora sí


# ============================================================================
# Tests de Strategy
# ============================================================================

class TestStrategy:
    """Tests para el patrón Strategy"""
    
    def test_registro_estrategias_ataque(self):
        """Verifica que el registro tiene todas las estrategias"""
        estrategias = [
            TipoAtaque.MELEE,
            TipoAtaque.DISTANCIA,
            TipoAtaque.MAGICO
        ]
        
        for tipo in estrategias:
            estrategia = RegistroEstrategiasAtaque.obtener(tipo)
            assert estrategia is not None
    
    def test_estrategias_diferentes(self):
        """Verifica que cada estrategia es diferente"""
        melee = RegistroEstrategiasAtaque.obtener(TipoAtaque.MELEE)
        distancia = RegistroEstrategiasAtaque.obtener(TipoAtaque.DISTANCIA)
        magico = RegistroEstrategiasAtaque.obtener(TipoAtaque.MAGICO)
        
        assert type(melee).__name__ == "EstrategiaAtaqueMelee"
        assert type(distancia).__name__ == "EstrategiaAtaqueDistancia"
        assert type(magico).__name__ == "EstrategiaAtaqueMagico"


# ============================================================================
# Test de Integración
# ============================================================================

class TestIntegracionPatrones:
    """Tests de integración entre patrones"""
    
    def test_factory_con_eventbus(self):
        """Verifica que Factory y EventBus trabajan juntos"""
        
        class Arma:
            def __init__(self, nombre: str, bus: EventBus):
                self.nombre = nombre
                self.bus = bus
            
            def atacar(self):
                self.bus.publicar(TipoEvento.ATAQUE_REALIZADO, 
                                 {"arma": self.nombre})
        
        factory = FactoryConRegistro[Arma]()
        factory.registrar("espada", Arma)
        
        bus = EventBus()
        eventos = []
        bus.suscribir(TipoEvento.ATAQUE_REALIZADO, lambda e: eventos.append(e))
        
        espada = factory.crear("espada", nombre="Excalibur", bus=bus)
        espada.atacar()
        
        assert len(eventos) == 1
        assert eventos[0].datos["arma"] == "Excalibur"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])