"""
Servicio de Narrador - Genera narraciones dinámicas con IA.
Se suscribe a eventos del juego y genera descripciones contextuales.
"""
from typing import Optional, Dict, Any
from patrones import EventBus, TipoEvento, Evento
from .cliente_ia import ClienteIA, ClienteIAMock
from .persistencia_estructuras import ContextoNarrativo
from entidades import Personaje


class NarradorService:
    """
    Servicio de narrador con IA.
    Genera descripciones dinámicas basadas en eventos y contexto.
    """
    
    def __init__(
        self,
        event_bus: EventBus,
        contexto: Optional[ContextoNarrativo] = None,
        usar_mock: bool = False
    ):
        """
        Args:
            event_bus: Bus de eventos del juego
            contexto: Contexto narrativo actual
            usar_mock: Si True, usa el cliente mock (sin API)
        """
        self.event_bus = event_bus
        self.contexto = contexto or ContextoNarrativo()
        
        # Cliente de IA
        if usar_mock:
            self.cliente = ClienteIAMock()
        else:
            self.cliente = ClienteIA()
            # Si no está disponible, usar mock automáticamente
            if not self.cliente.esta_disponible():
                print("⚠️ API de OpenAI no disponible, usando narrador mock")
                self.cliente = ClienteIAMock()
        
        # Personalidad del narrador
        self.system_message = self._crear_system_message()
        
        # Suscribirse a eventos relevantes
        self._suscribir_eventos()
    
    def _crear_system_message(self) -> str:
        """Crea el mensaje de sistema que define la personalidad del narrador"""
        return """Eres el narrador de "Ether Blades", un juego de rol épico y oscuro.

Tu rol es:
- Narrar los eventos del juego de forma inmersiva y cinematográfica
- Usar un tono dramático pero no excesivamente florido
- Mantener coherencia con el mundo de Ether Blades (magia, combate, intriga)
- Ser conciso: narraciones de 2-4 oraciones máximo
- Nunca alterar mecánicas: solo describes, no decides resultados
- Adaptar el tono según el evento (épico en combate, misterioso en exploración)

Mundo de Ether Blades:
- Mundo medieval-fantástico con magia (Hephix)
- La ciudad principal es Amarth en Nerosia
- Existen facciones: Kairenistas (luz) y Vadhenistas (oscuridad)
- El combate es brutal y estratégico
- La magia tiene un costo (PM, stamina, o vida en caso de Hephix Sangriento)

Responde SOLO con la narración, sin comentarios meta."""
    
    def _suscribir_eventos(self):
        """Suscribe el narrador a eventos relevantes del juego"""
        # Eventos de combate
        self.event_bus.suscribir(TipoEvento.COMBATE_INICIADO, self._narrar_inicio_combate)
        self.event_bus.suscribir(TipoEvento.ATAQUE_REALIZADO, self._narrar_ataque)
        self.event_bus.suscribir(TipoEvento.GOLPE_GRACIA, self._narrar_golpe_gracia)
        self.event_bus.suscribir(TipoEvento.CONTRAATAQUE, self._narrar_contraataque)
        self.event_bus.suscribir(TipoEvento.PERSONAJE_MUERTO, self._narrar_muerte)
        
        # Eventos narrativos
        self.event_bus.suscribir(TipoEvento.CHECKPOINT_ALCANZADO, self._narrar_checkpoint)
    
    # ========================================================================
    # Generación de prompts
    # ========================================================================
    
    def _construir_prompt_base(self, evento_tipo: str, datos: Dict[str, Any]) -> str:
        """
        Construye un prompt base con contexto.
        
        Args:
            evento_tipo: Tipo de evento
            datos: Datos del evento
        
        Returns:
            Prompt con contexto completo
        """
        partes = []
        
        # Contexto general
        if self.contexto:
            partes.append(f"Ubicación: {self.contexto.ubicacion_actual}")
            if self.contexto.log_narrativo:
                ultimo_evento = self.contexto.log_narrativo[-1]
                partes.append(f"Evento previo: {ultimo_evento.descripcion}")
        
        # Datos del evento actual
        partes.append(f"\nEvento: {evento_tipo}")
        for clave, valor in datos.items():
            partes.append(f"{clave}: {valor}")
        
        return "\n".join(partes)
    
    # ========================================================================
    # Narradores de eventos específicos
    # ========================================================================
    
    def _narrar_inicio_combate(self, evento: Evento):
        """Narra el inicio de un combate"""
        datos = evento.datos
        combatientes = datos.get('combatientes', [])
        
        prompt = f"""Narra el momento épico justo antes de que comience un combate entre:
{', '.join(combatientes)}

El ambiente está tenso, las armas están desenvainadas.
Describe la escena en 2-3 oraciones dramáticas."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=150
            )
            self._mostrar_narracion("⚔️ INICIO DE COMBATE", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_ataque(self, evento: Evento):
        """Narra un ataque"""
        datos = evento.datos
        atacante = datos.get('atacante', 'Alguien')
        defensor = datos.get('defensor', 'el enemigo')
        
        prompt = f"""Narra brevemente cómo {atacante} ataca a {defensor}.
Menciona el movimiento, la tensión del momento.
Máximo 2 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=100
            )
            self._mostrar_narracion("⚔️", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_golpe_gracia(self, evento: Evento):
        """Narra un golpe de gracia"""
        datos = evento.datos
        atacante = datos.get('atacante', 'El guerrero')
        defensor = datos.get('defensor', 'el enemigo')
        
        prompt = f"""Narra de forma ÉPICA y DRAMÁTICA el golpe de gracia definitivo.
{atacante} está a punto de asestar el golpe final a {defensor}, que está agotado.
Describe el momento decisivo en 2 oraciones impactantes."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=120
            )
            self._mostrar_narracion("💥 GOLPE DE GRACIA", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_contraataque(self, evento: Evento):
        """Narra un contraataque"""
        datos = evento.datos
        atacante = datos.get('atacante', 'El defensor')
        defensor = datos.get('defensor', 'el atacante')
        
        prompt = f"""Narra cómo {atacante} aprovecha una apertura y contraataca a {defensor}.
Describe el giro inesperado del combate en 2 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=100
            )
            self._mostrar_narracion("🔄 CONTRAATAQUE", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_muerte(self, evento: Evento):
        """Narra la muerte de un personaje"""
        datos = evento.datos
        personaje = datos.get('personaje', 'El combatiente')
        
        prompt = f"""Narra la caída final de {personaje} en combate.
Describe el momento solemne de su derrota en 2 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=100
            )
            self._mostrar_narracion("💀", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_checkpoint(self, evento: Evento):
        """Narra alcanzar un checkpoint"""
        datos = evento.datos
        checkpoint = datos.get('checkpoint', 'un lugar importante')
        
        prompt = f"""Narra el momento en que el personaje llega a {checkpoint}.
Describe la escena y el ambiente del lugar en 3 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=150
            )
            self._mostrar_narracion("📍 CHECKPOINT", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    # ========================================================================
    # Narración libre
    # ========================================================================
    
    def narrar_situacion(
        self,
        situacion: str,
        personaje: Optional[Personaje] = None
    ) -> str:
        """
        Genera una narración libre de una situación.
        
        Args:
            situacion: Descripción de la situación a narrar
            personaje: Personaje involucrado (opcional)
        
        Returns:
            Narración generada
        """
        # Construir contexto
        contexto_partes = []
        
        if personaje:
            contexto_partes.append(f"Personaje: {personaje.nombre}, {personaje.clase.value}")
            contexto_partes.append(f"Hephix: {personaje.hephix.tipo.value}")
        
        if self.contexto:
            contexto_partes.append(f"Ubicación: {self.contexto.ubicacion_actual}")
        
        contexto_str = "\n".join(contexto_partes)
        
        prompt = f"""{contexto_str}

Situación: {situacion}

Narra esta situación de forma inmersiva en 3-4 oraciones."""
        
        try:
            return self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=200
            )
        except Exception as e:
            return f"[Error al generar narración: {e}]"
    
    def narrar_decision(
        self,
        decision: str,
        opciones: list[str],
        personaje: Optional[Personaje] = None
    ) -> str:
        """
        Narra una situación de decisión y presenta las opciones.
        
        Args:
            decision: Descripción de la decisión a tomar
            opciones: Lista de opciones disponibles
            personaje: Personaje que decide
        
        Returns:
            Narración de la situación
        """
        prompt = f"""El personaje se enfrenta a una decisión importante:
{decision}

Narra la situación que lleva a esta decisión en 2-3 oraciones.
NO menciones las opciones, solo describe el dilema."""
        
        try:
            return self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=150
            )
        except Exception as e:
            return f"[Error al generar narración: {e}]"
    
    # ========================================================================
    # Utilidades
    # ========================================================================
    
    def _mostrar_narracion(self, titulo: str, narracion: str):
        """Muestra una narración formateada"""
        print(f"\n{titulo}")
        print("─" * 70)
        print(f"📖 {narracion}")
        print("─" * 70)
    
    def actualizar_contexto(self, contexto: ContextoNarrativo):
        """Actualiza el contexto narrativo"""
        self.contexto = contexto


if __name__ == "__main__":
    from entidades import Ficha, Hephix, HephixTipo, ClaseTipo
    
    print("=== Demo del Narrador ===\n")
    
    # Crear personaje
    ficha = Ficha()
    ficha.caracteristicas.fuerza = 8
    personaje = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha
    )
    
    # Crear contexto
    contexto = ContextoNarrativo(
        ubicacion_actual="Bosque Oscuro",
        checkpoint_actual="entrada_cueva"
    )
    
    # Crear narrador (con mock)
    event_bus = EventBus()
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    
    print("Generando narración de situación...\n")
    narracion = narrador.narrar_situacion(
        "El personaje encuentra una cueva misteriosa con runas brillantes",
        personaje
    )
    print(f"📖 {narracion}")