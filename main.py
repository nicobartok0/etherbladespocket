"""
Ether Blades - Punto de entrada principal del juego.
Sistema de rol digital con motor de combate determinista y narrador IA.

Ejecutar: python main.py
"""
import sys
from typing import Optional
from servicios import (
    CreacionPersonajeService,
    PersistenciaService,
    CombateService,
    NarradorService,
    ContextoNarrativo,
    EventoNarrativo,
    TipoEventoNarrativo
)
from entidades import Personaje
from patrones import EventBus


class EtherBladesGame:
    """
    Clase principal del juego.
    Gestiona el loop principal y la navegación entre menús.
    """
    
    def __init__(self):
        """Inicializa el juego y sus servicios"""
        self.running = True
        
        # Servicios principales
        self.creacion_service = CreacionPersonajeService()
        self.persistencia_service = PersistenciaService()
        self.event_bus = EventBus()
        
        # Estado del juego
        self.personaje: Optional[Personaje] = None
        self.contexto: Optional[ContextoNarrativo] = None
        self.narrador: Optional[NarradorService] = None
        
        # Determinar si usar IA real o mock
        self.usar_ia_real = self._configurar_narrador()
    
    def _configurar_narrador(self) -> bool:
        """
        Configura el narrador (real o mock).
        
        Returns:
            True si usa IA real, False si usa mock
        """
        from servicios.cliente_ia import ClienteIA
        
        cliente = ClienteIA()
        if cliente.esta_disponible():
            print("✅ Narrador IA activado (OpenAI)")
            return True
        else:
            print("⚠️  Narrador IA en modo simulación (sin API key)")
            print("   Configura OPENAI_API_KEY en .env para narraciones reales\n")
            return False
    
    # ========================================================================
    # Loop Principal
    # ========================================================================
    
    def run(self):
        """Loop principal del juego"""
        self._mostrar_bienvenida()
        
        while self.running:
            self._menu_principal()
    
    def _mostrar_bienvenida(self):
        """Muestra la pantalla de bienvenida"""
        print("\n" + "="*70)
        print("  ⚔️  ETHER BLADES - AFTERMATH")
        print("="*70)
        print("\n  Un juego de rol épico con magia, combate y decisiones.\n")
        print("  Desarrollado por: Nicolás Bartolomeo")
        print("  Universidad de Mendoza - Computación II")
        print("\n" + "="*70)
    
    def _menu_principal(self):
        """Menú principal del juego"""
        print("\n" + "─"*70)
        print("  MENÚ PRINCIPAL")
        print("─"*70)
        print("\n1. 🆕 Nueva Partida")
        print("2. 📂 Cargar Partida")
        print("3. 💾 Gestionar Guardados")
        print("4. ℹ️  Acerca de")
        print("0. 🚪 Salir")
        
        opcion = input("\n➤ Selecciona una opción: ").strip()
        
        if opcion == "1":
            self._nueva_partida()
        elif opcion == "2":
            self._cargar_partida()
        elif opcion == "3":
            self._gestionar_guardados()
        elif opcion == "4":
            self._acerca_de()
        elif opcion == "0":
            self._salir()
        else:
            print("❌ Opción inválida")
    
    # ========================================================================
    # Nueva Partida
    # ========================================================================
    
    def _nueva_partida(self):
        """Inicia una nueva partida"""
        print("\n" + "="*70)
        print("  🆕 NUEVA PARTIDA")
        print("="*70)
        
        # Crear personaje
        print("\nPrimero, vamos a crear tu personaje...\n")
        input("Presiona Enter para comenzar...")
        
        try:
            self.personaje = self.creacion_service.crear_personaje_interactivo()
        except KeyboardInterrupt:
            print("\n\n❌ Creación cancelada")
            return
        
        # Crear contexto inicial
        self.contexto = ContextoNarrativo(
            checkpoint_actual="amarth_inicio",
            ubicacion_actual="Ciudad de Amarth - Plaza Central"
        )
        
        # Agregar evento inicial
        self.contexto.agregar_evento(EventoNarrativo(
            tipo=TipoEventoNarrativo.CHECKPOINT,
            descripcion=f"{self.personaje.nombre} llega a la ciudad de Amarth",
            relevancia="alta"
        ))
        
        # Inicializar narrador
        self.narrador = NarradorService(
            self.event_bus,
            self.contexto,
            usar_mock=not self.usar_ia_real
        )
        
        # Iniciar sesión (para tracking de tiempo)
        self.persistencia_service.iniciar_sesion()
        
        # Escena inicial
        self._escena_inicial()
        
        # Loop de juego
        self._loop_juego()
    
    def _escena_inicial(self):
        """Muestra la escena inicial del juego"""
        print("\n" + "="*70)
        print("  📖 PRÓLOGO")
        print("="*70 + "\n")
        
        narracion = self.narrador.narrar_situacion(
            f"{self.personaje.nombre}, un {self.personaje.raza.lower()} "
            f"{self.personaje.clase.value}, llega a la ciudad de Amarth "
            f"con {self.personaje.objetivo.lower()}",
            self.personaje
        )
        
        print(narracion)
        print("\n" + "─"*70)
        input("\nPresiona Enter para continuar tu aventura...")
    
    # ========================================================================
    # Loop de Juego
    # ========================================================================
    
    def _loop_juego(self):
        """Loop principal del juego una vez iniciada la partida"""
        while self.running and self.personaje.esta_vivo:
            print("\n" + "="*70)
            print(f"  📍 {self.contexto.ubicacion_actual}")
            print("="*70)
            print(f"\n👤 {self.personaje.nombre} (Nivel {self.personaje.nivel})")
            print(f"   ❤️  PV: {self.personaje.pv_actuales}/{self.personaje.pv_maximos}")
            print(f"   💙 PM: {self.personaje.pm_actuales}/{self.personaje.pm_maximos}")
            print(f"   💰 Monedas: {self.personaje.inventario.monedas}")
            
            print("\n" + "─"*70)
            print("  ¿QUÉ DESEAS HACER?")
            print("─"*70)
            print("\n1. 🗺️  Explorar")
            print("2. ⚔️  Entrenar en Combate (Demo)")
            print("3. 🎒 Ver Inventario")
            print("4. 📊 Ver Ficha Completa")
            print("5. 💾 Guardar Partida")
            print("0. 🚪 Volver al Menú Principal")
            
            opcion = input("\n➤ Selecciona una opción: ").strip()
            
            if opcion == "1":
                self._explorar()
            elif opcion == "2":
                self._combate_demo()
            elif opcion == "3":
                self._ver_inventario()
            elif opcion == "4":
                self._ver_ficha()
            elif opcion == "5":
                self._guardar_partida_rapido()
            elif opcion == "0":
                if self._confirmar_salir_partida():
                    break
            else:
                print("❌ Opción inválida")
        
        if not self.personaje.esta_vivo:
            self._game_over()
    
    def _explorar(self):
        """Opción de exploración (placeholder)"""
        print("\n🗺️  Explorando los alrededores...")
        
        narracion = self.narrador.narrar_situacion(
            "El personaje explora la zona en busca de algo interesante",
            self.personaje
        )
        print(f"\n📖 {narracion}")
        
        # Agregar evento al contexto
        self.contexto.agregar_evento(EventoNarrativo(
            tipo=TipoEventoNarrativo.DESCUBRIMIENTO,
            descripcion="Exploró los alrededores",
            relevancia="baja"
        ))
        
        input("\nPresiona Enter para continuar...")
    
    def _combate_demo(self):
        """Demo de combate contra un enemigo generado"""
        print("\n⚔️  Preparándote para el combate...")
        
        # Crear enemigo simple
        from entidades import Ficha, Hephix, HephixTipo, ClaseTipo
        
        ficha_enemigo = Ficha()
        ficha_enemigo.caracteristicas.fuerza = 5
        ficha_enemigo.caracteristicas.reflejos = 4
        ficha_enemigo.caracteristicas.resistencia = 4
        ficha_enemigo.caracteristicas.stamina = 2
        
        enemigo = Personaje(
            nombre="Bandido",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_enemigo
        )
        
        # Iniciar combate
        combate_service = CombateService(self.event_bus)
        estado = combate_service.iniciar_combate([self.personaje, enemigo])
        
        print(f"\n💥 ¡Combate contra {enemigo.nombre}!")
        input("Presiona Enter para comenzar...")
        
        # Simulación simple de combate (solo primer turno)
        turno = 1
        max_turnos = 10
        
        while estado.combate_activo and turno <= max_turnos:
            print(f"\n--- Turno {turno} ---")
            
            # Turno del jugador
            if estado.orden_turnos[estado.indice_turno_actual] == self.personaje.nombre:
                resultado = combate_service.resolver_ataque(self.personaje, enemigo)
                print(f"➤ {resultado.descripcion_corta()}")
            else:
                resultado = combate_service.resolver_ataque(enemigo, self.personaje)
                print(f"➤ {resultado.descripcion_corta()}")
            
            # Verificar fin
            if combate_service.verificar_fin_combate():
                break
            
            estado.avanzar_turno()
            turno += 1
            
            input("\nPresiona Enter para continuar...")
        
        # Resultado
        if estado.ganador == self.personaje.nombre:
            print("\n✨ ¡Victoria!")
            xp = 100
            oro = 50
            self.personaje.ganar_experiencia(xp)
            self.personaje.inventario.agregar_monedas(oro)
            print(f"   Ganaste {xp} XP y {oro} monedas")
            
            # Agregar evento
            self.contexto.agregar_evento(EventoNarrativo(
                tipo=TipoEventoNarrativo.COMBATE,
                descripcion=f"Derrotaste a {enemigo.nombre}",
                relevancia="media"
            ))
        else:
            print("\n💀 Has sido derrotado...")
        
        input("\nPresiona Enter para continuar...")
    
    def _ver_inventario(self):
        """Muestra el inventario del personaje"""
        print("\n" + "="*70)
        print("  🎒 INVENTARIO")
        print("="*70)
        print(self.personaje.inventario.resumen())
        input("\nPresiona Enter para continuar...")
    
    def _ver_ficha(self):
        """Muestra la ficha completa del personaje"""
        print("\n" + "="*70)
        print("  📊 FICHA DE PERSONAJE")
        print("="*70)
        print(self.personaje.resumen_completo())
        input("\nPresiona Enter para continuar...")
    
    def _guardar_partida_rapido(self):
        """Guarda la partida en el slot 1"""
        print("\n💾 Guardando partida...")
        
        try:
            self.persistencia_service.guardar_partida(
                self.personaje,
                self.contexto,
                slot=1,
                nombre_partida=f"Aventura de {self.personaje.nombre}"
            )
            print("✅ Partida guardada exitosamente en el Slot 1")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _confirmar_salir_partida(self) -> bool:
        """Confirma si el jugador quiere salir sin guardar"""
        print("\n⚠️  ¿Deseas guardar antes de salir?")
        print("1. Sí, guardar y salir")
        print("2. No, salir sin guardar")
        print("3. Cancelar")
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            self._guardar_partida_rapido()
            return True
        elif opcion == "2":
            return True
        else:
            return False
    
    def _game_over(self):
        """Pantalla de game over"""
        print("\n" + "="*70)
        print("  💀 GAME OVER")
        print("="*70)
        print(f"\n{self.personaje.nombre} ha caído en combate.")
        print("Tu aventura ha llegado a su fin...")
        input("\nPresiona Enter para volver al menú principal...")
    
    # ========================================================================
    # Cargar Partida
    # ========================================================================
    
    def _cargar_partida(self):
        """Carga una partida guardada"""
        print("\n" + "="*70)
        print("  📂 CARGAR PARTIDA")
        print("="*70 + "\n")
        
        # Listar partidas
        slots = self.persistencia_service.listar_partidas()
        partidas_disponibles = [s for s in slots if s.existe]
        
        if not partidas_disponibles:
            print("No hay partidas guardadas.")
            input("\nPresiona Enter para continuar...")
            return
        
        print("Partidas disponibles:\n")
        for slot in partidas_disponibles:
            print(slot)
            print()
        
        # Seleccionar slot
        try:
            slot_num = int(input("➤ Selecciona el número de slot (0 para cancelar): "))
            
            if slot_num == 0:
                return
            
            if not 1 <= slot_num <= 10:
                print("❌ Slot inválido")
                return
            
            # Cargar
            print(f"\n📂 Cargando partida del slot {slot_num}...")
            
            self.personaje = self.persistencia_service.cargar_personaje(slot_num)
            self.contexto = self.persistencia_service.cargar_contexto(slot_num)
            
            # Reiniciar narrador con el contexto cargado
            self.narrador = NarradorService(
                self.event_bus,
                self.contexto,
                usar_mock=not self.usar_ia_real
            )
            
            # Reiniciar sesión
            self.persistencia_service.iniciar_sesion()
            
            print(f"✅ Partida cargada: {self.personaje.nombre}")
            print(f"   Ubicación: {self.contexto.ubicacion_actual}")
            
            input("\nPresiona Enter para continuar...")
            
            # Ir al loop de juego
            self._loop_juego()
            
        except ValueError:
            print("❌ Entrada inválida")
        except FileNotFoundError:
            print("❌ No hay partida en ese slot")
        except Exception as e:
            print(f"❌ Error al cargar: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    # ========================================================================
    # Gestión de Guardados
    # ========================================================================
    
    def _gestionar_guardados(self):
        """Menú de gestión de guardados"""
        while True:
            print("\n" + "="*70)
            print("  💾 GESTIÓN DE GUARDADOS")
            print("="*70 + "\n")
            
            slots = self.persistencia_service.listar_partidas()
            
            for slot in slots:
                if slot.existe:
                    print(slot)
                else:
                    print(f"Slot {slot.slot}: [VACÍO]")
                print()
            
            print("1. Ver detalles de un slot")
            print("2. Eliminar una partida")
            print("0. Volver")
            
            opcion = input("\n➤ Opción: ").strip()
            
            if opcion == "1":
                self._ver_detalles_slot()
            elif opcion == "2":
                self._eliminar_partida()
            elif opcion == "0":
                break
            else:
                print("❌ Opción inválida")
    
    def _ver_detalles_slot(self):
        """Muestra detalles de un slot"""
        try:
            slot_num = int(input("\n➤ Número de slot: "))
            
            if not 1 <= slot_num <= 10:
                print("❌ Slot inválido")
                return
            
            if not self.persistencia_service.existe_partida(slot_num):
                print("❌ Ese slot está vacío")
                return
            
            datos = self.persistencia_service.cargar_partida(slot_num)
            print("\n" + "─"*70)
            print(datos.resumen_corto())
            print("─"*70)
            
        except ValueError:
            print("❌ Entrada inválida")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _eliminar_partida(self):
        """Elimina una partida guardada"""
        try:
            slot_num = int(input("\n➤ Número de slot a eliminar: "))
            
            if not 1 <= slot_num <= 10:
                print("❌ Slot inválido")
                return
            
            confirmar = input(f"⚠️  ¿Confirmar eliminación del slot {slot_num}? (s/n): ")
            
            if confirmar.lower() == 's':
                if self.persistencia_service.eliminar_partida(slot_num):
                    print("✅ Partida eliminada")
                else:
                    print("❌ El slot ya estaba vacío")
        
        except ValueError:
            print("❌ Entrada inválida")
        
        input("\nPresiona Enter para continuar...")
    
    # ========================================================================
    # Acerca de
    # ========================================================================
    
    def _acerca_de(self):
        """Muestra información del juego"""
        print("\n" + "="*70)
        print("  ℹ️  ACERCA DE ETHER BLADES")
        print("="*70 + "\n")
        
        print("📖 Ether Blades - Aftermath")
        print("   Sistema de rol digital con motor de combate determinista\n")
        
        print("👨‍💻 Desarrollado por: Nicolás Bartolomeo")
        print("🏫 Universidad de Mendoza")
        print("📚 Materia: Diseño de Sistemas\n")
        
        print("🎮 Características:")
        print("   • Sistema de combate basado en reglas deterministas")
        print("   • Creación de personajes con 13 tipos de Hephix (magia)")
        print("   • 6 clases de personaje")
        print("   • Narrador IA con OpenAI (opcional)")
        print("   • Sistema de guardado/carga con contexto narrativo")
        print("   • Arquitectura con patrones de diseño (MVC, Singleton, etc.)\n")
        
        print(f"📌 Versión: {self.persistencia_service.directorio.parent.name}")
        
        input("\nPresiona Enter para continuar...")
    
    # ========================================================================
    # Salir
    # ========================================================================
    
    def _salir(self):
        """Sale del juego"""
        print("\n👋 ¡Gracias por jugar Ether Blades!")
        print("   Que los Hephix te acompañen...\n")
        self.running = False


def main():
    """Función principal"""
    try:
        game = EtherBladesGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n❌ Juego interrumpido por el usuario.")
        print("👋 ¡Hasta luego!\n")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        print("\nPor favor, reporta este error.\n")


if __name__ == "__main__":
    main()