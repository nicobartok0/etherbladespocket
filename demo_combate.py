"""
Demo del sistema de combate.
Ejecutar: python demo_combate.py
"""
from servicios import CombateService, CreacionPersonajeService
from entidades import HephixTipo, ClaseTipo, crear_espada_basica
from patrones import EventBus, TipoEvento
import time


def imprimir_barra_vida(nombre: str, pv_actual: int, pv_max: int, ps_actual: int, ps_max: int):
    """Imprime una barra de vida y stamina visual"""
    porcentaje_pv = (pv_actual / pv_max) * 100 if pv_max > 0 else 0
    porcentaje_ps = (ps_actual / ps_max) * 100 if ps_max > 0 else 0
    
    barra_pv = "█" * int(porcentaje_pv / 5) + "░" * (20 - int(porcentaje_pv / 5))
    barra_ps = "█" * int(porcentaje_ps / 5) + "░" * (20 - int(porcentaje_ps / 5))
    
    print(f"\n{nombre}:")
    print(f"  ❤️  PV: [{barra_pv}] {pv_actual}/{pv_max}")
    print(f"  ⚡ PS: [{barra_ps}] {ps_actual}/{ps_max}")


def main():
    """Ejecuta una demo completa de combate"""
    print("\n" + "="*70)
    print("  ⚔️  ETHER BLADES - DEMO DE COMBATE")
    print("="*70 + "\n")
    
    # Crear servicio de creación
    creacion = CreacionPersonajeService()
    
    # Crear guerrero
    print("Creando combatientes...\n")
    guerrero = creacion.crear_personaje(
        nombre="Aldric el Valiente",
        edad=28,
        raza="Humano",
        historia="Un guerrero experimentado",
        objetivo="Proteger a los inocentes",
        hephix_tipo=HephixTipo.ELEMENTAL,
        clase=ClaseTipo.GUERRERO,
        caracteristicas={"fuerza": 9, "reflejos": 5, "resistencia": 8, 
                        "voluntad": 0, "punteria": 0, "stamina": 3},
        habilidades_combate={"armas_cortantes": 15, "armas_contundentes": 0,
                            "armas_magicas": 0, "armas_distancia": 0, "pugilismo": 0},
        habilidades_educacion={"medicina": 5, "elocuencia": 0,
                              "manual": 0, "arcanismo": 0},
        habilidades_talento={"sigilo": 0, "percepcion": 5,
                            "mentalidad": 5, "astralidad": 0}
    )
    
    # Crear enemigo
    enemigo = creacion.crear_personaje(
        nombre="Goblin Salvaje",
        edad=15,
        raza="Goblin",
        historia="Un goblin agresivo de las cavernas",
        objetivo="Sobrevivir y saquear",
        hephix_tipo=HephixTipo.OCULTA,
        clase=ClaseTipo.EXPLORADOR,
        caracteristicas={"fuerza": 5, "reflejos": 7, "resistencia": 4,
                        "voluntad": 0, "punteria": 3, "stamina": 2},
        habilidades_combate={"armas_cortantes": 8, "armas_contundentes": 0,
                            "armas_magicas": 0, "armas_distancia": 5, "pugilismo": 0},
        habilidades_educacion={"medicina": 0, "elocuencia": 0,
                              "manual": 0, "arcanismo": 0},
        habilidades_talento={"sigilo": 10, "percepcion": 5,
                            "mentalidad": 0, "astralidad": 0}
    )
    
    print(f"✅ {guerrero.nombre} (Guerrero, Nivel {guerrero.nivel})")
    print(f"   PV: {guerrero.pv_maximos} | PM: {guerrero.pm_maximos}")
    print(f"   Arma: {guerrero.arma_equipada.nombre if guerrero.arma_equipada else 'Ninguna'}")
    
    print(f"\n✅ {enemigo.nombre} (Explorador, Nivel {enemigo.nivel})")
    print(f"   PV: {enemigo.pv_maximos} | PM: {enemigo.pm_maximos}")
    
    # Configurar event bus con logger
    event_bus = EventBus()
    
    def logger_combate(evento):
        """Log de eventos importantes"""
        if evento.tipo == TipoEvento.GOLPE_GRACIA:
            print(f"\n💥 ¡GOLPE DE GRACIA!")
        elif evento.tipo == TipoEvento.CONTRAATAQUE:
            print(f"\n🔄 ¡CONTRAATAQUE!")
        elif evento.tipo == TipoEvento.PERSONAJE_MUERTO:
            print(f"\n💀 {evento.datos['personaje']} ha caído!")
    
    event_bus.suscribir(TipoEvento.GOLPE_GRACIA, logger_combate)
    event_bus.suscribir(TipoEvento.CONTRAATAQUE, logger_combate)
    event_bus.suscribir(TipoEvento.PERSONAJE_MUERTO, logger_combate)
    
    # Iniciar combate
    servicio = CombateService(event_bus)
    
    print("\n" + "="*70)
    print("  ⚔️  ¡COMIENZA EL COMBATE!")
    print("="*70)
    
    estado = servicio.iniciar_combate([guerrero, enemigo])
    
    print(f"\n🎲 Orden de iniciativa:")
    for i, nombre in enumerate(estado.orden_turnos, 1):
        comb = estado.obtener_combatiente_por_nombre(nombre)
        print(f"  {i}. {nombre} (Iniciativa: {comb.iniciativa})")
    
    time.sleep(1)
    
    # Simulación de turnos
    turno = 1
    max_turnos = 20  # Límite de seguridad
    
    while estado.combate_activo and turno <= max_turnos:
        print("\n" + "-"*70)
        print(f"  TURNO {turno}")
        print("-"*70)
        
        # Mostrar estado actual
        imprimir_barra_vida(guerrero.nombre, guerrero.pv_actuales, guerrero.pv_maximos,
                           guerrero.ps_actuales, guerrero.ps_maximos)
        imprimir_barra_vida(enemigo.nombre, enemigo.pv_actuales, enemigo.pv_maximos,
                           enemigo.ps_actuales, enemigo.ps_maximos)
        
        time.sleep(1)
        
        # Determinar atacante y defensor
        nombre_atacante = estado.orden_turnos[estado.indice_turno_actual]
        
        if nombre_atacante == guerrero.nombre:
            atacante, defensor = guerrero, enemigo
        else:
            atacante, defensor = enemigo, guerrero
        
        if not atacante.esta_en_condiciones_combate() or not defensor.esta_en_condiciones_combate():
            break
        
        print(f"\n⚔️  {atacante.nombre} ataca a {defensor.nombre}...")
        time.sleep(0.5)
        
        # Resolver ataque
        resultado = servicio.resolver_ataque(atacante, defensor)
        
        print(f"\n{resultado.descripcion_corta()}")
        
        if resultado.tipo.value in ["exito", "critico"]:
            print(f"   CA: {resultado.coeficiente_ataque} | CD: {resultado.coeficiente_defensa}")
            if resultado.daño_infligido > 0:
                print(f"   💔 Daño: {resultado.daño_infligido}")
            if resultado.stamina_perdida > 0:
                print(f"   ⚡ Stamina perdida: {resultado.stamina_perdida}")
        
        # Verificar fin de combate
        if servicio.verificar_fin_combate():
            break
        
        # Avanzar turno
        estado.avanzar_turno()
        turno += 1
        
        time.sleep(1)
    
    # Resultado final
    print("\n" + "="*70)
    print("  🏆 FIN DEL COMBATE")
    print("="*70)
    
    if estado.ganador:
        print(f"\n✨ ¡{estado.ganador} es el VICTORIOSO!")
    else:
        print("\n⚠️  Combate inconcluso (límite de turnos alcanzado)")
    
    print(f"\n📊 Estadísticas finales:")
    imprimir_barra_vida(guerrero.nombre, guerrero.pv_actuales, guerrero.pv_maximos,
                       guerrero.ps_actuales, guerrero.ps_maximos)
    imprimir_barra_vida(enemigo.nombre, enemigo.pv_actuales, enemigo.pv_maximos,
                       enemigo.ps_actuales, enemigo.ps_maximos)
    
    print(f"\n📜 Total de intercambios: {len(estado.historial_ataques)}")
    print(f"🎲 Turnos totales: {turno}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()