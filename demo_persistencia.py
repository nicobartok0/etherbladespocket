"""
Demo del sistema de persistencia.
Ejecutar: python demo_persistencia.py
"""
from servicios import CreacionPersonajeService, PersistenciaService
from servicios.persistencia_estructuras import ContextoNarrativo, EventoNarrativo, TipoEvento
from entidades import HephixTipo, ClaseTipo


def imprimir_separador(titulo: str = ""):
    """Imprime un separador visual"""
    if titulo:
        print(f"\n{'='*70}")
        print(f"  {titulo}")
        print(f"{'='*70}\n")
    else:
        print("-" * 70)


def demo_guardar_partida():
    """Demuestra el guardado de una partida"""
    imprimir_separador("💾 GUARDADO DE PARTIDA")
    
    # Crear servicio de creación
    creacion = CreacionPersonajeService()
    
    # Crear personaje
    print("Creando personaje de prueba...")
    personaje = creacion.crear_personaje(
        nombre="Theron el Explorador",
        edad=30,
        raza="Elfo",
        historia="Un explorador veterano que busca artefactos antiguos",
        objetivo="Descubrir los secretos de las ruinas antiguas",
        hephix_tipo=HephixTipo.ESPIRITUAL,
        clase=ClaseTipo.EXPLORADOR,
        caracteristicas={
            "fuerza": 6,
            "reflejos": 8,
            "resistencia": 5,
            "voluntad": 5,
            "punteria": 8,
            "stamina": 3
        },
        habilidades_combate={
            "armas_cortantes": 5,
            "armas_contundentes": 0,
            "armas_magicas": 0,
            "armas_distancia": 15,
            "pugilismo": 0
        },
        habilidades_educacion={
            "medicina": 3,
            "elocuencia": 5,
            "manual": 0,
            "arcanismo": 2
        },
        habilidades_talento={
            "sigilo": 8,
            "percepcion": 10,
            "mentalidad": 0,
            "astralidad": 2
        }
    )
    
    print(f"✅ Personaje creado: {personaje.nombre}")
    print(f"   Clase: {personaje.clase.value.title()}")
    print(f"   Hephix: {personaje.hephix.tipo.value.title()}")
    print(f"   Nivel: {personaje.nivel}")
    print(f"   PV: {personaje.pv_maximos} | PM: {personaje.pm_maximos}")
    
    # Simular progreso
    print("\nSimulando progreso en la aventura...")
    personaje.ganar_experiencia(500)
    personaje.inventario.agregar_monedas(350)
    
    # Crear contexto narrativo
    contexto = ContextoNarrativo(
        checkpoint_actual="ruinas_antiguas_entrada",
        ubicacion_actual="Ruinas de Kal'Theron"
    )
    
    # Agregar eventos narrativos
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.DESCUBRIMIENTO,
        descripcion="Descubriste la entrada a las ruinas antiguas",
        relevancia="alta"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.COMBATE,
        descripcion="Derrotaste a dos guardianes de piedra",
        relevancia="media"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.DIALOGO,
        descripcion="Hablaste con el espíritu del guardián caído",
        relevancia="alta"
    ))
    
    contexto.npcs_conocidos.extend([
        "Guardián Espectral",
        "Anciano de la Aldea",
        "Comerciante Errante"
    ])
    
    contexto.reputacion["Exploradores de Amarth"] = 20
    contexto.reputacion["Guardia de las Ruinas"] = -10
    
    contexto.misiones_activas.append("Explorar las profundidades de Kal'Theron")
    contexto.misiones_completadas.append("Encontrar la entrada a las ruinas")
    
    print("\n📖 Contexto narrativo configurado:")
    print(f"   Ubicación: {contexto.ubicacion_actual}")
    print(f"   Checkpoint: {contexto.checkpoint_actual}")
    print(f"   NPCs conocidos: {len(contexto.npcs_conocidos)}")
    print(f"   Eventos registrados: {len(contexto.log_narrativo)}")
    
    # Guardar partida
    print("\n💾 Guardando partida...")
    servicio = PersistenciaService()
    servicio.iniciar_sesion()
    
    archivo = servicio.guardar_partida(
        personaje,
        contexto,
        slot=1,
        nombre_partida="Aventura en las Ruinas"
    )
    
    print(f"✅ Partida guardada en: {archivo}")
    print(f"   Slot: 1")
    print(f"   Tiempo jugado: {servicio._formatear_tiempo_jugado()}")
    
    return personaje, contexto


def demo_listar_partidas():
    """Demuestra el listado de partidas guardadas"""
    imprimir_separador("📋 LISTADO DE PARTIDAS GUARDADAS")
    
    servicio = PersistenciaService()
    slots = servicio.listar_partidas()
    
    partidas_encontradas = 0
    
    for slot in slots:
        if slot.existe:
            partidas_encontradas += 1
            print(slot)
            print()
    
    if partidas_encontradas == 0:
        print("No hay partidas guardadas.")
    else:
        print(f"Total de partidas: {partidas_encontradas}/10")


def demo_cargar_partida():
    """Demuestra la carga de una partida"""
    imprimir_separador("📂 CARGA DE PARTIDA")
    
    servicio = PersistenciaService()
    
    # Verificar que existe
    if not servicio.existe_partida(1):
        print("❌ No hay partida en el slot 1")
        return
    
    print("Cargando partida del slot 1...")
    
    # Cargar datos completos
    datos = servicio.cargar_partida(1)
    
    print(f"\n✅ Partida cargada: {datos.nombre_partida}")
    print(f"   Versión: {datos.version}")
    print(f"   Guardado: {datos.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Tiempo jugado: {datos.tiempo_jugado}")
    
    # Restaurar personaje
    personaje = servicio.cargar_personaje(1)
    
    print(f"\n👤 Personaje restaurado:")
    print(f"   Nombre: {personaje.nombre}")
    print(f"   Nivel: {personaje.nivel}")
    print(f"   XP: {personaje.experiencia}")
    print(f"   PV: {personaje.pv_actuales}/{personaje.pv_maximos}")
    print(f"   PM: {personaje.pm_actuales}/{personaje.pm_maximos}")
    print(f"   Monedas: {personaje.inventario.monedas}")
    
    # Restaurar contexto
    contexto = servicio.cargar_contexto(1)
    
    print(f"\n📍 Contexto narrativo:")
    print(f"   Ubicación: {contexto.ubicacion_actual}")
    print(f"   Checkpoint: {contexto.checkpoint_actual}")
    
    if contexto.npcs_conocidos:
        print(f"\n👥 NPCs conocidos:")
        for npc in contexto.npcs_conocidos:
            print(f"   • {npc}")
    
    if contexto.reputacion:
        print(f"\n⭐ Reputación:")
        for faccion, rep in contexto.reputacion.items():
            signo = "+" if rep >= 0 else ""
            print(f"   • {faccion}: {signo}{rep}")
    
    if contexto.misiones_activas:
        print(f"\n📜 Misiones activas:")
        for mision in contexto.misiones_activas:
            print(f"   • {mision}")
    
    if contexto.log_narrativo:
        print(f"\n📖 Eventos recientes:")
        for evento in contexto.log_narrativo[-5:]:  # Últimos 5
            print(f"   {evento.resumen()}")
    
    return personaje, contexto


def demo_contexto_para_ia():
    """Demuestra el resumen para IA"""
    imprimir_separador("🤖 CONTEXTO PARA IA")
    
    servicio = PersistenciaService()
    
    if not servicio.existe_partida(1):
        print("❌ No hay partida para mostrar")
        return
    
    contexto = servicio.cargar_contexto(1)
    
    print("Generando resumen del contexto para la IA...\n")
    print("─" * 70)
    print(contexto.obtener_resumen_para_ia())
    print("─" * 70)
    
    print("\n💡 Este resumen se enviará al narrador IA para que pueda")
    print("   continuar la historia de forma coherente con lo ya ocurrido.")


def demo_verificar_integridad():
    """Demuestra la verificación de integridad"""
    imprimir_separador("🔍 VERIFICACIÓN DE INTEGRIDAD")
    
    servicio = PersistenciaService()
    
    print("Verificando integridad de todos los slots...\n")
    
    for slot in range(1, 11):
        valido, error = servicio.verificar_integridad(slot)
        
        if valido:
            print(f"Slot {slot:2d}: ✅ OK")
        else:
            print(f"Slot {slot:2d}: ❌ {error}")


def menu_principal():
    """Menú interactivo"""
    while True:
        imprimir_separador("💾 DEMO - SISTEMA DE PERSISTENCIA")
        
        print("1. Crear y guardar nueva partida")
        print("2. Listar partidas guardadas")
        print("3. Cargar partida (Slot 1)")
        print("4. Ver contexto para IA")
        print("5. Verificar integridad de guardados")
        print("6. Eliminar partida (Slot 1)")
        print("0. Salir")
        
        print()
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            demo_guardar_partida()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "2":
            demo_listar_partidas()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "3":
            demo_cargar_partida()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "4":
            demo_contexto_para_ia()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "5":
            demo_verificar_integridad()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "6":
            servicio = PersistenciaService()
            if servicio.eliminar_partida(1):
                print("\n✅ Partida del slot 1 eliminada")
            else:
                print("\n⚠️ No había partida en el slot 1")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción inválida")
            input("\nPresiona Enter para continuar...")


def main():
    """Ejecuta el demo completo"""
    print("\n" + "="*70)
    print("  💾 ETHER BLADES - DEMO DE PERSISTENCIA")
    print("="*70)
    print("\nEste demo muestra el sistema completo de guardado y carga.")
    print("Incluye serialización de personajes y contexto narrativo para IA.")
    
    input("\nPresiona Enter para comenzar...")
    
    menu_principal()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()