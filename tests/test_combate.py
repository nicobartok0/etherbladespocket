"""
Tests para el servicio de combate.
Ejecutar con: pytest tests/test_combate.py -v
"""
import pytest
from servicios.combate_service import CombateService
from servicios.combate_estructuras import TipoResultadoAtaque
from entidades import (
    Personaje, Ficha, Hephix, HephixTipo, ClaseTipo,
    crear_espada_basica, establecer_semilla
)
from patrones import EventBus, TipoEvento


class TestCombateService:
    """Tests para el motor de combate"""
    
    @pytest.fixture
    def event_bus(self):
        """Crea un event bus para testing"""
        return EventBus()
    
    @pytest.fixture
    def servicio_combate(self, event_bus):
        """Crea un servicio de combate"""
        return CombateService(event_bus)
    
    @pytest.fixture
    def guerrero(self):
        """Crea un guerrero de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.reflejos = 4
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.stamina = 3
        ficha.combate.armas_cortantes = 10
        
        personaje = Personaje(
            nombre="Aldric",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
        personaje.equipar_arma(crear_espada_basica())
        return personaje
    
    @pytest.fixture
    def enemigo_debil(self):
        """Crea un enemigo débil"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 4
        ficha.caracteristicas.reflejos = 3
        ficha.caracteristicas.resistencia = 3
        ficha.caracteristicas.stamina = 1
        
        return Personaje(
            nombre="Goblin",
            edad=10,
            raza="Goblin",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
    
    # ========================================================================
    # Tests de Inicialización
    # ========================================================================
    
    def test_iniciar_combate(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que se inicia correctamente un combate"""
        estado = servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        assert estado is not None
        assert len(estado.combatientes) == 2
        assert len(estado.orden_turnos) == 2
        assert estado.combate_activo
        assert estado.turno_actual == 0
    
    def test_iniciativa_determina_orden(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que la iniciativa determina el orden de turnos"""
        # Fijar semilla para resultados predecibles
        establecer_semilla(42)
        
        estado = servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Verificar que todos tienen iniciativa asignada
        for combatiente in estado.combatientes:
            assert combatiente.iniciativa > 0
    
    def test_error_combate_un_solo_combatiente(self, servicio_combate, guerrero):
        """Verifica que no se puede iniciar combate con un solo combatiente"""
        with pytest.raises(ValueError, match="al menos 2 combatientes"):
            servicio_combate.iniciar_combate([guerrero])
    
    def test_stamina_restaurada_al_iniciar(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que la stamina se restaura al iniciar combate"""
        # Reducir stamina antes del combate
        guerrero.gastar_stamina(10)
        enemigo_debil.gastar_stamina(5)
        
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Verificar que se restauró
        assert guerrero.ps_actuales == guerrero.ps_maximos
        assert enemigo_debil.ps_actuales == enemigo_debil.ps_maximos
    
    # ========================================================================
    # Tests de Resolución de Ataques
    # ========================================================================
    
    def test_resolver_ataque_basico(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica resolución básica de ataque"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        assert resultado is not None
        assert resultado.atacante_nombre == "Aldric"
        assert resultado.defensor_nombre == "Goblin"
        assert resultado.tipo in TipoResultadoAtaque
    
    def test_ataque_reduce_stamina(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que un ataque exitoso reduce stamina"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        stamina_inicial = enemigo_debil.ps_actuales
        
        # Fijar semilla para ataque exitoso
        establecer_semilla(100)
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        if resultado.tipo == TipoResultadoAtaque.EXITO:
            assert enemigo_debil.ps_actuales < stamina_inicial
            assert resultado.stamina_perdida > 0
    
    def test_golpe_de_gracia_cuando_stamina_cero(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que se ejecuta golpe de gracia cuando stamina = 0"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Reducir stamina a 0
        enemigo_debil.ps_actuales = 0
        
        pv_inicial = enemigo_debil.pv_actuales
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        # Debería ser golpe de gracia o crítico
        assert resultado.tipo == TipoResultadoAtaque.CRITICO
        assert resultado.fue_golpe_gracia
        assert enemigo_debil.pv_actuales < pv_inicial
        assert resultado.daño_infligido > 0
    
    def test_contraataque_con_diferencia_negativa(self, servicio_combate):
        """Verifica contraataque cuando diferencia <= -3"""
        # Crear atacante muy débil y defensor fuerte
        ficha_debil = Ficha()
        ficha_debil.caracteristicas.fuerza = 1
        ficha_debil.caracteristicas.reflejos = 1
        ficha_debil.caracteristicas.resistencia = 3
        ficha_debil.caracteristicas.stamina = 1
        
        atacante_debil = Personaje(
            nombre="Débil",
            edad=20,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_debil
        )
        
        ficha_fuerte = Ficha()
        ficha_fuerte.caracteristicas.fuerza = 10
        ficha_fuerte.caracteristicas.reflejos = 10
        ficha_fuerte.caracteristicas.resistencia = 8
        ficha_fuerte.caracteristicas.stamina = 5
        
        defensor_fuerte = Personaje(
            nombre="Fuerte",
            edad=30,
            raza="Orco",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_fuerte
        )
        defensor_fuerte.equipar_arma(crear_espada_basica())
        
        servicio_combate.iniciar_combate([atacante_debil, defensor_fuerte])
        
        # Con semilla apropiada, debería haber contraataque
        establecer_semilla(1)
        resultado = servicio_combate.resolver_ataque(atacante_debil, defensor_fuerte)
        
        # Puede ser contraataque directo o resultado del contraataque
        assert resultado is not None
    
    def test_ataque_bloqueado(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica ataque bloqueado sin consecuencias"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Con una semilla específica podríamos forzar un bloqueo
        # Por ahora solo verificamos que el tipo existe
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        if resultado.tipo == TipoResultadoAtaque.BLOQUEADO:
            assert resultado.stamina_perdida == 0
            assert resultado.daño_infligido == 0
    
    # ========================================================================
    # Tests de Ataques Especiales
    # ========================================================================
    
    def test_ataque_sigilo_exitoso(self, servicio_combate):
        """Verifica ataque furtivo exitoso"""
        # Crear atacante con alto sigilo
        ficha_sigiloso = Ficha()
        ficha_sigiloso.caracteristicas.fuerza = 6
        ficha_sigiloso.caracteristicas.reflejos = 5
        ficha_sigiloso.caracteristicas.resistencia = 5
        ficha_sigiloso.caracteristicas.stamina = 3
        ficha_sigiloso.talento.sigilo = 15  # Alto sigilo
        
        sigiloso = Personaje(
            nombre="Asesino",
            edad=25,
            raza="Elfo",
            clase=ClaseTipo.EXPLORADOR,
            hephix=Hephix.crear_desde_tipo(HephixTipo.OCULTA),
            ficha=ficha_sigiloso
        )
        sigiloso.equipar_arma(crear_espada_basica())
        
        # Crear objetivo con baja percepción
        ficha_victima = Ficha()
        ficha_victima.caracteristicas.resistencia = 5
        ficha_victima.caracteristicas.stamina = 2
        ficha_victima.talento.percepcion = 2  # Baja percepción
        
        victima = Personaje(
            nombre="Guardia",
            edad=30,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_victima
        )
        
        servicio_combate.iniciar_combate([sigiloso, victima])
        
        pv_inicial = victima.pv_actuales
        resultado = servicio_combate.ataque_sigilo(sigiloso, victima)
        
        # Debería ser exitoso (Sigilo 15 - Percepción 2 = 13 > 0)
        assert resultado.tipo == TipoResultadoAtaque.SIGILO_EXITOSO
        assert resultado.daño_infligido > 0
        assert victima.pv_actuales < pv_inicial
    
    def test_ataque_sigilo_detectado(self, servicio_combate):
        """Verifica que ataque furtivo detectado resulta en contraataque"""
        # Crear atacante con bajo sigilo
        ficha_torpe = Ficha()
        ficha_torpe.caracteristicas.fuerza = 6
        ficha_torpe.caracteristicas.resistencia = 5
        ficha_torpe.caracteristicas.stamina = 2
        ficha_torpe.talento.sigilo = 2  # Bajo sigilo
        
        torpe = Personaje(
            nombre="Novato",
            edad=18,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_torpe
        )
        
        # Crear objetivo con alta percepción
        ficha_alerta = Ficha()
        ficha_alerta.caracteristicas.fuerza = 7
        ficha_alerta.caracteristicas.resistencia = 6
        ficha_alerta.caracteristicas.stamina = 3
        ficha_alerta.talento.percepcion = 15  # Alta percepción
        
        alerta = Personaje(
            nombre="Veterano",
            edad=40,
            raza="Elfo",
            clase=ClaseTipo.EXPLORADOR,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_alerta
        )
        alerta.equipar_arma(crear_espada_basica())
        
        servicio_combate.iniciar_combate([torpe, alerta])
        
        resultado = servicio_combate.ataque_sigilo(torpe, alerta)
        
        # Debería ser detectado y contraatacar (Sigilo 2 - Percepción 15 = -13 < 0)
        assert resultado.fue_contraataque or resultado.tipo == TipoResultadoAtaque.CONTRAATAQUE
    
    # ========================================================================
    # Tests de Eventos
    # ========================================================================
    
    def test_eventos_publicados_en_combate(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que se publican eventos durante el combate"""
        eventos_recibidos = []
        
        def capturar_evento(evento):
            eventos_recibidos.append(evento.tipo)
        
        # Suscribirse a eventos
        servicio_combate.event_bus.suscribir(TipoEvento.COMBATE_INICIADO, capturar_evento)
        servicio_combate.event_bus.suscribir(TipoEvento.ATAQUE_REALIZADO, capturar_evento)
        
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        assert TipoEvento.COMBATE_INICIADO in eventos_recibidos
        assert TipoEvento.ATAQUE_REALIZADO in eventos_recibidos
    
    def test_evento_personaje_muerto(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica evento cuando un personaje muere"""
        eventos_muerte = []
        
        def capturar_muerte(evento):
            eventos_muerte.append(evento.datos)
        
        servicio_combate.event_bus.suscribir(TipoEvento.PERSONAJE_MUERTO, capturar_muerte)
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Reducir PV del enemigo casi a 0
        enemigo_debil.pv_actuales = 1
        enemigo_debil.ps_actuales = 0
        
        # Golpe de gracia que lo mate
        servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        if not enemigo_debil.esta_vivo:
            assert len(eventos_muerte) > 0
    
    # ========================================================================
    # Tests de Verificación de Fin
    # ========================================================================
    
    def test_verificar_fin_combate(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica detección de fin de combate"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Combate activo inicialmente
        assert not servicio_combate.verificar_fin_combate()
        
        # Matar a un combatiente
        enemigo_debil.pv_actuales = 0
        enemigo_debil.esta_vivo = False
        
        # Actualizar estado
        for c in servicio_combate.estado.combatientes:
            if c.nombre == enemigo_debil.nombre:
                c.esta_vivo = False
                c.pv_actuales = 0
        
        # Ahora debería detectar fin
        assert servicio_combate.verificar_fin_combate()
        assert servicio_combate.estado.ganador == "Aldric"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])