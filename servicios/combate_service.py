"""
Servicio de Combate - Motor de combate determinista.
Implementa todas las reglas de combate de Ether Blades.
"""
from typing import List, Optional
from entidades import (
    Personaje, tirar_dados, tirar_d10, Constantes,
    TipoAtaque
)
from patrones import EventBus, TipoEvento, RegistroEstrategiasAtaque
from .combate_estructuras import (
    ResultadoAtaque, TipoResultadoAtaque,
    EstadoCombate, EstadoCombatiente
)


class CombateService:
    """
    Servicio principal de combate.
    Implementa todas las mecánicas de combate del juego.
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Args:
            event_bus: Bus de eventos para notificaciones (opcional)
        """
        self.event_bus = event_bus or EventBus()
        self.estado: Optional[EstadoCombate] = None
    
    # ========================================================================
    # Inicialización de combate
    # ========================================================================
    
    def iniciar_combate(self, combatientes: List[Personaje]) -> EstadoCombate:
        """
        Inicia un nuevo combate entre los combatientes.
        
        Args:
            combatientes: Lista de personajes que participan
        
        Returns:
            Estado inicial del combate
        """
        if len(combatientes) < 2:
            raise ValueError("Se necesitan al menos 2 combatientes")
        
        # Restaurar stamina de todos
        for c in combatientes:
            c.restaurar_stamina_completa()
        
        # Calcular iniciativa (Sta + 1d10)
        iniciativas = []
        for combatiente in combatientes:
            tirada = tirar_d10()
            iniciativa_total = combatiente.ficha.stamina + tirada.total
            iniciativas.append((combatiente, iniciativa_total))
        
        # Ordenar por iniciativa (mayor primero)
        iniciativas.sort(key=lambda x: x[1], reverse=True)
        
        # Crear estado de combate
        self.estado = EstadoCombate()
        
        for combatiente, iniciativa in iniciativas:
            estado_comb = EstadoCombatiente(
                nombre=combatiente.nombre,
                pv_actuales=combatiente.pv_actuales,
                pv_maximos=combatiente.pv_maximos,
                ps_actuales=combatiente.ps_actuales,
                ps_maximos=combatiente.ps_maximos,
                esta_vivo=combatiente.esta_vivo,
                esta_inconsciente=combatiente.esta_inconsciente,
                iniciativa=iniciativa
            )
            self.estado.combatientes.append(estado_comb)
            self.estado.orden_turnos.append(combatiente.nombre)
        
        # Publicar evento
        self.event_bus.publicar(TipoEvento.COMBATE_INICIADO, {
            "combatientes": [c.nombre for c in combatientes],
            "orden_iniciativa": self.estado.orden_turnos
        })
        
        return self.estado
    
    # ========================================================================
    # Resolución de ataques
    # ========================================================================
    
    def resolver_ataque(self, atacante: Personaje, defensor: Personaje) -> ResultadoAtaque:
        """
        Resuelve un ataque completo entre dos personajes.
        Implementa las reglas de combate de Ether Blades.
        
        Args:
            atacante: Personaje que ataca
            defensor: Personaje que defiende
        
        Returns:
            Resultado detallado del ataque
        """
        # Verificar que ambos están en condiciones de combatir
        if not atacante.esta_en_condiciones_combate():
            raise ValueError(f"{atacante.nombre} no puede combatir")
        
        if not defensor.esta_en_condiciones_combate():
            raise ValueError(f"{defensor.nombre} no puede combatir")
        
        # Calcular coeficientes
        ca = self._calcular_coeficiente_ataque(atacante)
        cd = self._calcular_coeficiente_defensa(defensor)
        
        diferencia = ca - cd
        
        # Publicar evento de ataque realizado
        self.event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre,
            "ca": ca,
            "cd": cd,
            "diferencia": diferencia
        })
        
        # Determinar resultado según la diferencia
        if diferencia > 0:
            # Atacante gana: reduce stamina del defensor
            return self._aplicar_reduccion_stamina(atacante, defensor, diferencia)
        
        elif diferencia <= Constantes.UMBRAL_CONTRAATAQUE:
            # Defensor tiene derecho a contraataque (diferencia <= -3)
            return self._contraataque(atacante, defensor, diferencia)
        
        else:
            # Ataque bloqueado (diferencia entre -2 y 0)
            return self._ataque_bloqueado(atacante, defensor, ca, cd)
    
    def _calcular_coeficiente_ataque(self, atacante: Personaje) -> int:
        """
        Calcula el Coeficiente de Ataque (CA).
        Fórmula: Stat base + 3d6 + bonus_arma + bonus_habilidad
        """
        # Obtener estrategia según tipo de arma
        if atacante.arma_equipada:
            estrategia = RegistroEstrategiasAtaque.obtener(atacante.arma_equipada.tipo_ataque)
        else:
            # Pugilismo (sin arma)
            estrategia = RegistroEstrategiasAtaque.obtener(TipoAtaque.MELEE)
        
        # Tirar dados
        tirada = tirar_dados(Constantes.DADOS_ATAQUE, 6)
        
        # Calcular usando la estrategia
        ca = estrategia.calcular_coeficiente(atacante, atacante.arma_equipada, tirada.dados)
        
        return ca
    
    def _calcular_coeficiente_defensa(self, defensor: Personaje) -> int:
        """
        Calcula el Coeficiente de Defensa (CD).
        Fórmula: Reflejos + 2d6 + bonus_armadura
        """
        tirada = tirar_dados(Constantes.DADOS_DEFENSA, 6)
        cd = defensor.obtener_modificador_reflejos() + tirada.total
        
        return cd
    
    def _aplicar_reduccion_stamina(self, atacante: Personaje, 
                                   defensor: Personaje, 
                                   diferencia: int) -> ResultadoAtaque:
        """
        Aplica reducción de stamina cuando el atacante gana.
        Si la stamina llega a 0, permite golpe de gracia.
        """
        # Reducir stamina
        defensor.gastar_stamina(diferencia)
        
        resultado = ResultadoAtaque(
            tipo=TipoResultadoAtaque.EXITO,
            atacante_nombre=atacante.nombre,
            defensor_nombre=defensor.nombre,
            stamina_perdida=diferencia,
            defensor_pv_restantes=defensor.pv_actuales,
            defensor_stamina_restante=defensor.ps_actuales,
            arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
        )
        
        # Verificar si quedó sin stamina -> GOLPE DE GRACIA
        if defensor.esta_sin_stamina():
            resultado_gracia = self._golpe_de_gracia(atacante, defensor)
            resultado.fue_golpe_gracia = True
            resultado.tipo = TipoResultadoAtaque.CRITICO
            resultado.daño_infligido = resultado_gracia.daño_infligido
            resultado.defensor_pv_restantes = resultado_gracia.defensor_pv_restantes
            resultado.defensor_muerto = resultado_gracia.defensor_muerto
        
        return resultado
    
    def _golpe_de_gracia(self, atacante: Personaje, defensor: Personaje) -> ResultadoAtaque:
        """
        Ejecuta un golpe de gracia cuando el defensor no tiene stamina.
        El ataque no encuentra resistencia.
        """
        # Calcular CA sin resistencia
        ca = self._calcular_coeficiente_ataque(atacante)
        daño = ca  # Sin reducción por CD
        
        # Aplicar daño
        daño_real = defensor.recibir_daño(daño)
        
        resultado = ResultadoAtaque(
            tipo=TipoResultadoAtaque.CRITICO,
            atacante_nombre=atacante.nombre,
            defensor_nombre=defensor.nombre,
            coeficiente_ataque=ca,
            daño_infligido=daño_real,
            defensor_pv_restantes=defensor.pv_actuales,
            defensor_stamina_restante=0,
            defensor_muerto=not defensor.esta_vivo,
            fue_golpe_gracia=True,
            arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
        )
        
        # Publicar evento
        self.event_bus.publicar(TipoEvento.GOLPE_GRACIA, {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre,
            "daño": daño_real,
            "defensor_vivo": defensor.esta_vivo
        })
        
        if not defensor.esta_vivo:
            self.event_bus.publicar(TipoEvento.PERSONAJE_MUERTO, {
                "personaje": defensor.nombre
            })
        
        return resultado
    
    def _contraataque(self, atacante_original: Personaje, 
                     defensor_original: Personaje,
                     diferencia_original: int) -> ResultadoAtaque:
        """
        El defensor contraataca cuando la diferencia es <= -3.
        """
        self.event_bus.publicar(TipoEvento.CONTRAATAQUE, {
            "atacante": defensor_original.nombre,
            "defensor": atacante_original.nombre
        })
        
        # El defensor ahora ataca
        resultado_contra = self.resolver_ataque(defensor_original, atacante_original)
        resultado_contra.fue_contraataque = True
        resultado_contra.tipo = TipoResultadoAtaque.CONTRAATAQUE
        
        return resultado_contra
    
    def _ataque_bloqueado(self, atacante: Personaje, defensor: Personaje,
                         ca: int, cd: int) -> ResultadoAtaque:
        """Ataque bloqueado sin consecuencias"""
        resultado = ResultadoAtaque(
            tipo=TipoResultadoAtaque.BLOQUEADO,
            atacante_nombre=atacante.nombre,
            defensor_nombre=defensor.nombre,
            coeficiente_ataque=ca,
            coeficiente_defensa=cd,
            diferencia=ca - cd,
            defensor_pv_restantes=defensor.pv_actuales,
            defensor_stamina_restante=defensor.ps_actuales,
            arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
        )
        
        self.event_bus.publicar(TipoEvento.ATAQUE_BLOQUEADO, {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre
        })
        
        return resultado
    
    # ========================================================================
    # Ataques especiales
    # ========================================================================
    
    def ataque_sigilo(self, atacante: Personaje, defensor: Personaje) -> ResultadoAtaque:
        """
        Ataque desde las sombras.
        Daño extra = (Sigilo - Percepción) × 2
        """
        sigilo = atacante.ficha.talento.sigilo
        percepcion = defensor.ficha.talento.percepcion
        
        diferencia = sigilo - percepcion
        
        if diferencia > 0:
            # Ataque furtivo exitoso
            ca = self._calcular_coeficiente_ataque(atacante)
            daño_extra = diferencia * 2
            daño_total = ca + daño_extra
            
            daño_real = defensor.recibir_daño(daño_total)
            
            resultado = ResultadoAtaque(
                tipo=TipoResultadoAtaque.SIGILO_EXITOSO,
                atacante_nombre=atacante.nombre,
                defensor_nombre=defensor.nombre,
                coeficiente_ataque=ca,
                daño_infligido=daño_real,
                defensor_pv_restantes=defensor.pv_actuales,
                defensor_muerto=not defensor.esta_vivo,
                arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
            )
            
            self.event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
                "atacante": atacante.nombre,
                "defensor": defensor.nombre,
                "tipo": "sigilo",
                "daño": daño_real
            })
            
            return resultado
        else:
            # Detectado: el defensor contraataca
            return self._contraataque(atacante, defensor, diferencia)
    
    # ========================================================================
    # Utilidades
    # ========================================================================
    
    def verificar_fin_combate(self) -> bool:
        """
        Verifica si el combate ha terminado.
        Actualiza el estado.
        """
        if not self.estado:
            return True
        
        return self.estado.verificar_fin_combate()


if __name__ == "__main__":
    from entidades import Ficha, Hephix, HephixTipo, ClaseTipo, crear_espada_basica
    
    print("=== Demo del Motor de Combate ===\n")
    
    # Crear dos personajes para combate
    ficha1 = Ficha()
    ficha1.caracteristicas.fuerza = 8
    ficha1.caracteristicas.reflejos = 4
    ficha1.caracteristicas.resistencia = 7
    ficha1.caracteristicas.stamina = 3
    ficha1.combate.armas_cortantes = 10
    
    guerrero = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha1
    )
    guerrero.equipar_arma(crear_espada_basica())
    
    ficha2 = Ficha()
    ficha2.caracteristicas.fuerza = 5
    ficha2.caracteristicas.reflejos = 6
    ficha2.caracteristicas.resistencia = 4
    ficha2.caracteristicas.stamina = 2
    
    goblin = Personaje(
        nombre="Goblin",
        edad=10,
        raza="Goblin",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha2
    )
    
    # Iniciar combate
    servicio = CombateService()
    estado = servicio.iniciar_combate([guerrero, goblin])
    
    print(estado.resumen())
    print("\n--- Primer ataque ---")
    
    resultado = servicio.resolver_ataque(guerrero, goblin)
    print(resultado.descripcion_corta())