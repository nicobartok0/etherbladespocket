"""
Demo del sistema de narrador con IA.
Ejecutar: python demo_narrador.py
"""
from servicios import (
    CreacionPersonajeService, 
    CombateService, 
    NarradorService,
    ContextoNarrativo,
    EventoNarrativo,
    TipoEventoNarrativo
)
from entidades import HephixTipo, ClaseTipo
from patrones import EventBus
import time


def imprimir_separador(titulo: str = ""):
    """Imprime un separador visual"""
    if titulo:
        print(f"\n{'='*70}")
        print(f"  {titulo}")
        print(f"{'='*70}\n")
    else:
        print("-" * 70)


def demo_narracion_situaciones():
    """Demuestra narraciones de diferentes situaciones"""
    imprimir_separador("📖 NARRACIÓN DE SITUACIONES")
    
    # Crear contexto
    contexto = ContextoNarrativo(
        ubicacion_actual="Ruinas Antiguas de Kal'Theron",
        checkpoint_actual="entrada_ruinas"
    )
    
    # Crear narrador
    event_bus = EventBus()
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    
    print("El narrador generará descripciones de diferentes situaciones...\n")
    
    # Situación 1: Exploración
    print("📍 Situación: Explorando las ruinas")
    print("-" * 70)
    narracion = narrador.narrar_situacion(
        "El personaje encuentra una sala con inscripciones antiguas brillando débilmente"
    )
    print(f"📖 {narracion}\n")
    time.sleep(2)
    
    # Situación 2: Encuentro
    print("👤 Situación: Encuentro inesperado")
    print("-" * 70)
    narracion = narrador.narrar_situacion(
        "Un anciano misterioso aparece entre las sombras del pasillo"
    )
    print(f"📖 {narracion}\n")
    time.sleep(2)
    
    # Situación 3: Peligro
    print("⚠️ Situación: Peligro inminente")
    print("-" * 70)
    narracion = narrador.narrar_situacion(
        "El suelo comienza a temblar y piedras caen del techo"
    )
    print(f"📖 {narracion}\n")
    time.sleep(2)


def demo_narracion_decisiones():
    """Demuestra narraciones de decisiones"""
    imprimir_separador("🤔 NARRACIÓN DE DECISIONES")
    
    event_bus = EventBus()
    contexto = ContextoNarrativo(ubicacion_actual="Bifurcación del Camino")
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    
    # Decisión 1
    print("Decisión: ¿Qué camino tomar?")
    print("-" * 70)
    narracion = narrador.narrar_decision(
        "Dos caminos se abren ante ti. Uno iluminado por antorchas, otro en completa oscuridad",
        ["Camino iluminado", "Camino oscuro"]
    )
    print(f"📖 {narracion}")
    print("\nOpciones disponibles:")
    print("  1. Tomar el camino iluminado")
    print("  2. Adentrarse en la oscuridad\n")
    time.sleep(2)
    
    # Decisión 2
    print("Decisión: ¿Confiar o desconfiar?")
    print("-" * 70)
    narracion = narrador.narrar_decision(
        "El comerciante te ofrece un objeto mágico a un precio sospechosamente bajo",
        ["Aceptar el trato", "Rechazar con desconfianza"]
    )
    print(f"📖 {narracion}")
    print("\nOpciones disponibles:")
    print("  1. Comprar el objeto")
    print("  2. Rechazar la oferta\n")


def demo_combate_narrado():
    """Demuestra un combate completo con narración"""
    imprimir_separador("⚔️ COMBATE NARRADO")
    
    print("Preparando combate épico con narración en tiempo real...\n")
    time.sleep(1)
    
    # Crear personajes
    creacion = CreacionPersonajeService()
    
    heroe = creacion.crear_personaje(
        nombre="Sir Aldric",
        edad=28,
        raza="Humano",
        historia="Un caballero valiente",
        objetivo="Proteger al reino",
        hephix_tipo=HephixTipo.LUMINICA,
        clase=ClaseTipo.GUERRERO,
        caracteristicas={"fuerza": 9, "reflejos": 5, "resistencia": 8,
                        "voluntad": 3, "punteria": 0, "stamina": 3},
        habilidades_combate={"armas_cortantes": 15, "armas_contundentes": 0,
                            "armas_magicas": 0, "armas_distancia": 0, "pugilismo": 0},
        habilidades_educacion={"medicina": 5, "elocuencia": 0,
                              "manual": 0, "arcanismo": 0},
        habilidades_talento={"sigilo": 0, "percepcion": 5,
                            "mentalidad": 5, "astralidad": 5}
    )
    
    villano = creacion.crear_personaje(
        nombre="Zarak el Oscuro",
        edad=150,
        raza="Elfo Oscuro",
        historia="Un hechicero corrupto",
        objetivo="Dominar el reino",
        hephix_tipo=HephixTipo.OSCURA,
        clase=ClaseTipo.MAGO,
        caracteristicas={"fuerza": 4, "reflejos": 7, "resistencia": 5,
                        "voluntad": 10, "punteria": 0, "stamina": 2},
        habilidades_combate={"armas_cortantes": 0, "armas_contundentes": 0,
                            "armas_magicas": 15, "armas_distancia": 0, "pugilismo": 0},
        habilidades_educacion={"medicina": 0, "elocuencia": 5,
                              "manual": 0, "arcanismo": 10},
        habilidades_talento={"sigilo": 5, "percepcion": 5,
                            "mentalidad": 5, "astralidad": 0}
    )
    
    print(f"⚔️ {heroe.nombre} vs {villano.nombre}")
    print(f"   {heroe.nombre}: PV {heroe.pv_maximos} | {heroe.hephix.tipo.value.title()}")
    print(f"   {villano.nombre}: PV {villano.pv_maximos} | {villano.hephix.tipo.value.title()}\n")
    
    time.sleep(2)
    
    # Crear servicios
    event_bus = EventBus()
    contexto = ContextoNarrativo(
        ubicacion_actual="Torre Oscura - Sala del Trono",
        checkpoint_actual="confrontacion_final"
    )
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    combate = CombateService(event_bus)
    
    # Iniciar combate
    print("🎬 Iniciando combate...\n")
    estado = combate.iniciar_combate([heroe, villano])
    time.sleep(3)
    
    # Realizar algunos ataques
    print("\n🎲 Primer intercambio:")
    resultado = combate.resolver_ataque(heroe, villano)
    print(f"   Resultado: {resultado.descripcion_corta()}")
    time.sleep(3)
    
    if villano.esta_en_condiciones_combate():
        print("\n🎲 Segundo intercambio:")
        resultado = combate.resolver_ataque(villano, heroe)
        print(f"   Resultado: {resultado.descripcion_corta()}")
        time.sleep(3)
    
    print("\n" + "="*70)
    print("  Combate pausado para demostración")
    print("="*70)


def demo_contexto_narrativo():
    """Demuestra el uso del contexto narrativo"""
    imprimir_separador("📚 CONTEXTO NARRATIVO")
    
    # Crear contexto rico
    contexto = ContextoNarrativo(
        checkpoint_actual="ciudad_amarth_mercado",
        ubicacion_actual="Mercado de Amarth"
    )
    
    # Agregar NPCs
    contexto.npcs_conocidos.extend([
        "Marcus el Herrero",
        "Elara la Sanadora",
        "Thief Guildmaster",
        "Capitán de la Guardia"
    ])
    
    # Agregar reputación
    contexto.reputacion["Guardia de Amarth"] = 25
    contexto.reputacion["Gremio de Ladrones"] = -15
    contexto.reputacion["Templo de la Luz"] = 30
    
    # Agregar eventos
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEventoNarrativo.COMBATE,
        descripcion="Derrotaste a bandidos en las afueras",
        relevancia="alta"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEventoNarrativo.DIALOGO,
        descripcion="Hablaste con Marcus sobre armas legendarias",
        relevancia="media"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEventoNarrativo.DESCUBRIMIENTO,
        descripcion="Encontraste un mapa antiguo en el mercado",
        relevancia="alta"
    ))
    
    # Misiones
    contexto.misiones_activas.append("Investigar las ruinas antiguas")
    contexto.misiones_completadas.append("Limpiar el camino de bandidos")
    
    print("Contexto narrativo acumulado:\n")
    print(contexto.obtener_resumen_para_ia())
    
    print("\n💡 Este contexto permite al narrador IA generar historias")
    print("   coherentes con todo lo que ha ocurrido anteriormente.")


def menu_principal():
    """Menú interactivo"""
    while True:
        imprimir_separador("🎭 DEMO - SISTEMA DE NARRADOR IA")
        
        print("1. Narración de situaciones variadas")
        print("2. Narración de decisiones importantes")
        print("3. Combate completo con narración")
        print("4. Ver ejemplo de contexto narrativo")
        print("0. Salir")
        
        print()
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            demo_narracion_situaciones()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "2":
            demo_narracion_decisiones()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "3":
            demo_combate_narrado()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "4":
            demo_contexto_narrativo()
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
    print("  🎭 ETHER BLADES - DEMO DE NARRADOR IA")
    print("="*70)
    print("\nEste demo muestra el sistema de narración dinámica.")
    print("Usa un narrador MOCK que simula respuestas de IA.")
    print("\n💡 Para usar OpenAI real, configura OPENAI_API_KEY en .env")
    
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