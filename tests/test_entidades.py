"""
Tests unitarios para las entidades del dominio.
Ejecutar con: pytest tests/test_entidades.py -v
"""
import pytest
from entidades import (
    Personaje, Ficha, Hephix, HephixTipo, ClaseTipo,
    Arma, Armadura, Inventario, TipoArma, TipoAtaque,
    tirar_dados, establecer_semilla, Constantes,
    crear_espada_basica, crear_pocion_vida_menor
)


# ============================================================================
# Tests de Dados
# ============================================================================

class TestDados:
    """Tests para el sistema de tiradas de dados"""
    
    def test_tirar_dados_rango(self):
        """Verifica que los dados estén en rango válido"""
        for _ in range(100):
            resultado = tirar_dados(3, 6)
            assert 3 <= resultado.total <= 18
            assert len(resultado.dados) == 3
            for dado in resultado.dados:
                assert 1 <= dado <= 6
    
    def test_tirar_dados_semilla(self):
        """Verifica que con misma semilla da mismos resultados"""
        establecer_semilla(42)
        resultado1 = tirar_dados(2, 10)
        
        establecer_semilla(42)
        resultado2 = tirar_dados(2, 10)
        
        assert resultado1.total == resultado2.total
        assert resultado1.dados == resultado2.dados


# ============================================================================
# Tests de Hephix
# ============================================================================

class TestHephix:
    """Tests para la clase Hephix"""
    
    def test_crear_hephix_normal(self):
        """Verifica creación de hephix normal"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL)
        
        assert hephix.tipo == HephixTipo.ELEMENTAL
        assert hephix.nivel == 1
        assert hephix.puede_usar_pm()
        assert hephix.puede_usar_pcf()
        assert hephix.puede_usar_pct()
    
    def test_hephix_sangriento_especial(self):
        """Verifica mecánicas especiales del Hephix Sangriento"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.SANGRIENTA)
        
        assert hephix.es_sangriento()
        assert not hephix.puede_usar_pm()
        assert not hephix.puede_usar_pcf()
        assert not hephix.puede_usar_pct()
        
        # Verifica bonus de PV
        bonus_pv = hephix.calcular_modificador_pv(voluntad=8)
        assert bonus_pv == 8 * 5  # Vol × 5
    
    def test_hephix_kairenista(self):
        """Verifica identificación de hephix Kairenista"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.SANADORA)
        assert hephix.es_kairenista()
        assert not hephix.es_vadhenista()
    
    def test_hephix_vadhenista(self):
        """Verifica identificación de hephix Vadhenista"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.NIGROMANTE)
        assert hephix.es_vadhenista()
        assert not hephix.es_kairenista()


# ============================================================================
# Tests de Ficha
# ============================================================================

class TestFicha:
    """Tests para la clase Ficha"""
    
    def test_calculos_stats_derivados(self):
        """Verifica cálculos de PV, PM, PCF, PCT, PS"""
        ficha = Ficha()
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.voluntad = 5
        ficha.caracteristicas.fuerza = 6
        ficha.caracteristicas.punteria = 4
        ficha.caracteristicas.stamina = 3
        
        assert ficha.pv_maximos == 7 * 10  # 70
        assert ficha.pm_maximos == 5 * 5   # 25
        assert ficha.pcf_maximos == 6 * 5  # 30
        assert ficha.pct_maximos == 4 * 5  # 20
        assert ficha.ps_maximos == 3 * 5   # 15
    
    def test_ficha_hephix_sangriento(self):
        """Verifica cálculos con Hephix Sangriento"""
        ficha = Ficha(hephix_tipo=HephixTipo.SANGRIENTA)
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.voluntad = 8
        
        # PV base + bonus sangriento
        assert ficha.pv_maximos == (7 * 10) + (8 * 5)  # 70 + 40 = 110
        assert ficha.pm_maximos == 0
        assert ficha.pcf_maximos == 0
        assert ficha.pct_maximos == 0
    
    def test_validacion_distribucion(self):
        """Verifica validación de puntos"""
        ficha = Ficha()
        
        # Distribuir exactamente 20 puntos
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.reflejos = 4
        ficha.caracteristicas.resistencia = 6
        ficha.caracteristicas.voluntad = 0
        ficha.caracteristicas.punteria = 0
        ficha.caracteristicas.stamina = 2
        
        assert ficha.caracteristicas.total_puntos() == 20
        assert ficha.caracteristicas.validar_distribucion()
    
    def test_bonus_habilidad(self):
        """Verifica cálculo de bonus por habilidad"""
        ficha = Ficha()
        ficha.combate.armas_cortantes = 15
        
        # Cada 5 puntos = +1 bonus
        assert ficha.obtener_bonus_habilidad('armas_cortantes') == 3


# ============================================================================
# Tests de Arma
# ============================================================================

class TestArma:
    """Tests para armas y armaduras"""
    
    def test_crear_arma_basica(self):
        """Verifica creación de arma básica"""
        espada = crear_espada_basica()
        
        assert espada.nombre == "Espada Corta"
        assert espada.tipo_arma == TipoArma.CORTANTE_PUNZANTE
        assert espada.tipo_ataque == TipoAtaque.MELEE
        assert espada.bonus >= 0
    
    def test_mejora_mecanica(self):
        """Verifica sistema de mejora mecánica"""
        espada = crear_espada_basica()
        bonus_inicial = espada.bonus_total()
        
        # Aplicar mejora con Manual nivel 15
        espada.aplicar_mejora_mecanica(15)
        
        assert espada.mejora_mecanica == 3
        assert espada.bonus_total() == bonus_inicial + 3
    
    def test_mejora_magica_exclusiva(self):
        """Verifica que mejoras mecánica y mágica no coexistan"""
        espada = crear_espada_basica()
        
        espada.aplicar_mejora_mecanica(15)
        assert not espada.puede_mejorar_magicamente()
        
        # Intentar mejora mágica debería fallar
        resultado = espada.aplicar_mejora_magica(15)
        assert not resultado


# ============================================================================
# Tests de Inventario
# ============================================================================

class TestInventario:
    """Tests para el sistema de inventario"""
    
    def test_agregar_item(self):
        """Verifica agregar ítems al inventario"""
        inv = Inventario(capacidad_maxima=10)
        pocion = crear_pocion_vida_menor()
        
        assert inv.agregar_item(pocion)
        assert len(inv.items) == 1
    
    def test_items_apilables(self):
        """Verifica que ítems apilables se acumulan"""
        inv = Inventario()
        
        pocion1 = crear_pocion_vida_menor()
        pocion2 = crear_pocion_vida_menor()
        
        inv.agregar_item(pocion1)
        inv.agregar_item(pocion2)
        
        # Debería haber solo 1 entrada con cantidad 2
        assert len(inv.items) == 1
        assert inv.items[0].cantidad == 2
    
    def test_capacidad_maxima(self):
        """Verifica límite de capacidad"""
        inv = Inventario(capacidad_maxima=2)
        
        inv.agregar_arma(crear_espada_basica())
        inv.agregar_item(crear_pocion_vida_menor())
        
        # Ya está lleno (2 slots ocupados)
        assert not inv.tiene_espacio()
        
        # Pero ítems apilables NO consumen slot adicional
        # Agregar otra poción debería funcionar (se apila)
        assert inv.agregar_item(crear_pocion_vida_menor())
        assert inv.items[0].cantidad == 2  # Se apiló
        
        # Pero un ítem DIFERENTE no debería poder agregarse
        from entidades.inventario import Item
        item_nuevo = Item(nombre="Otro Item", es_apilable=False)
        assert not inv.agregar_item(item_nuevo)
    
    def test_buscar_item(self):
        """Verifica búsqueda de ítems"""
        inv = Inventario()
        pocion = crear_pocion_vida_menor()
        inv.agregar_item(pocion)
        
        encontrada = inv.buscar_item("Poción de Vida Menor")
        assert encontrada is not None
        assert encontrada.nombre == pocion.nombre


# ============================================================================
# Tests de Personaje
# ============================================================================

class TestPersonaje:
    """Tests para la clase Personaje"""
    
    @pytest.fixture
    def personaje_basico(self):
        """Crea un personaje de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.reflejos = 4
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.stamina = 1
        
        hephix = Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL)
        
        return Personaje(
            nombre="Test",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=hephix,
            ficha=ficha
        )
    
    def test_crear_personaje(self, personaje_basico):
        """Verifica creación de personaje"""
        assert personaje_basico.nombre == "Test"
        assert personaje_basico.nivel == 1
        assert personaje_basico.esta_vivo
    
    def test_stats_inicializados(self, personaje_basico):
        """Verifica que stats se inicializan correctamente"""
        assert personaje_basico.pv_actuales == personaje_basico.pv_maximos
        assert personaje_basico.pm_actuales == personaje_basico.pm_maximos
        assert personaje_basico.ps_actuales == personaje_basico.ps_maximos
    
    def test_recibir_daño(self, personaje_basico):
        """Verifica sistema de daño"""
        pv_iniciales = personaje_basico.pv_actuales
        daño = personaje_basico.recibir_daño(25)
        
        assert daño == 25
        assert personaje_basico.pv_actuales == pv_iniciales - 25
    
    def test_curar(self, personaje_basico):
        """Verifica sistema de curación"""
        personaje_basico.recibir_daño(30)
        pv_antes = personaje_basico.pv_actuales
        
        curado = personaje_basico.curar(20)
        
        assert curado == 20
        assert personaje_basico.pv_actuales == pv_antes + 20
    
    def test_muerte(self, personaje_basico):
        """Verifica que personaje muere al llegar a 0 PV"""
        personaje_basico.recibir_daño(1000)
        
        assert personaje_basico.pv_actuales == 0
        assert not personaje_basico.esta_vivo
        assert personaje_basico.esta_inconsciente
    
    def test_equipar_arma(self, personaje_basico):
        """Verifica equipamiento de arma"""
        espada = crear_espada_basica()
        personaje_basico.ficha.combate.armas_cortantes = 5
        
        assert personaje_basico.equipar_arma(espada)
        assert personaje_basico.arma_equipada == espada
    
    def test_ganar_experiencia(self, personaje_basico):
        """Verifica sistema de experiencia y nivel"""
        nivel_inicial = personaje_basico.nivel
        
        # Dar suficiente XP para subir de nivel
        personaje_basico.ganar_experiencia(1000)
        
        assert personaje_basico.nivel == nivel_inicial + 1
        assert personaje_basico.hephix.nivel == 2
    
    def test_serialización(self, personaje_basico):
        """Verifica que se puede serializar/deserializar"""
        data = personaje_basico.to_dict_guardado()
        
        personaje_cargado = Personaje.from_dict_guardado(data)
        
        assert personaje_cargado.nombre == personaje_basico.nombre
        assert personaje_cargado.nivel == personaje_basico.nivel
        assert personaje_cargado.pv_actuales == personaje_basico.pv_actuales


if __name__ == "__main__":
    pytest.main([__file__, "-v"])