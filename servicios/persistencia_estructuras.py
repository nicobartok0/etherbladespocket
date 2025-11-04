"""
Estructuras de datos para el sistema de persistencia.
Define el formato de guardado completo.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TipoEvento(str, Enum):
    """Tipos de eventos para el log narrativo"""
    COMBATE = "combate"
    DECISION = "decision"
    DIALOGO = "dialogo"
    CHECKPOINT = "checkpoint"
    DESCUBRIMIENTO = "descubrimiento"
    MISION = "mision"
    OTRO = "otro"


class EventoNarrativo(BaseModel):
    """
    Representa un evento importante en la historia.
    Se usa para dar contexto a la IA.
    """
    timestamp: datetime = Field(default_factory=datetime.now)
    tipo: TipoEvento
    descripcion: str
    relevancia: str = Field(default="media", pattern="^(baja|media|alta)$")
    datos_adicionales: Dict[str, Any] = Field(default_factory=dict)
    
    def resumen(self) -> str:
        """Genera un resumen del evento"""
        iconos = {
            TipoEvento.COMBATE: "⚔️",
            TipoEvento.DECISION: "🤔",
            TipoEvento.DIALOGO: "💬",
            TipoEvento.CHECKPOINT: "📍",
            TipoEvento.DESCUBRIMIENTO: "🔍",
            TipoEvento.MISION: "📜",
            TipoEvento.OTRO: "📝"
        }
        icono = iconos.get(self.tipo, "📝")
        return f"{icono} [{self.tipo.value}] {self.descripcion}"


class ContextoNarrativo(BaseModel):
    """
    Contexto narrativo completo de la partida.
    Crucial para que la IA pueda continuar la historia.
    """
    checkpoint_actual: str = Field(
        default="inicio",
        description="ID del checkpoint narrativo actual"
    )
    ubicacion_actual: str = Field(
        default="Ciudad de Amarth",
        description="Ubicación actual del personaje"
    )
    
    # Historia y progreso
    eventos_completados: List[str] = Field(
        default_factory=list,
        description="IDs de eventos/misiones completadas"
    )
    decisiones_importantes: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Decisiones clave tomadas por el jugador"
    )
    
    # NPCs y relaciones
    npcs_conocidos: List[str] = Field(
        default_factory=list,
        description="Nombres de NPCs con los que ha interactuado"
    )
    reputacion: Dict[str, int] = Field(
        default_factory=dict,
        description="Reputación con diferentes facciones"
    )
    
    # Misiones
    misiones_activas: List[str] = Field(
        default_factory=list,
        description="Misiones en curso"
    )
    misiones_completadas: List[str] = Field(
        default_factory=list,
        description="Misiones finalizadas"
    )
    
    # Log narrativo (últimos 50 eventos para contexto de IA)
    log_narrativo: List[EventoNarrativo] = Field(
        default_factory=list,
        description="Historial de eventos importantes"
    )
    
    def agregar_evento(self, evento: EventoNarrativo):
        """Agrega un evento al log (mantiene solo últimos 50)"""
        self.log_narrativo.append(evento)
        if len(self.log_narrativo) > 50:
            self.log_narrativo.pop(0)
    
    def obtener_resumen_para_ia(self) -> str:
        """
        Genera un resumen del contexto para enviar a la IA.
        Incluye los eventos más relevantes.
        """
        lineas = [
            f"Ubicación actual: {self.ubicacion_actual}",
            f"Checkpoint: {self.checkpoint_actual}",
            ""
        ]
        
        if self.npcs_conocidos:
            lineas.append(f"NPCs conocidos: {', '.join(self.npcs_conocidos)}")
        
        if self.reputacion:
            lineas.append("Reputación:")
            for faccion, rep in self.reputacion.items():
                lineas.append(f"  - {faccion}: {rep}")
        
        if self.misiones_activas:
            lineas.append(f"\nMisiones activas: {', '.join(self.misiones_activas)}")
        
        # Eventos recientes (últimos 10)
        if self.log_narrativo:
            lineas.append("\nEventos recientes:")
            for evento in self.log_narrativo[-10:]:
                lineas.append(f"  - {evento.resumen()}")
        
        return "\n".join(lineas)


class EstadoCombateGuardado(BaseModel):
    """Estado de combate para persistir"""
    en_combate: bool = False
    enemigos_vivos: List[str] = Field(default_factory=list)
    turno_actual: int = 0
    orden_turnos: List[str] = Field(default_factory=list)


class DatosPartida(BaseModel):
    """
    Estructura completa de una partida guardada.
    Contiene toda la información necesaria para restaurar el juego.
    """
    # Metadata
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
    slot: int = Field(ge=1, le=10, description="Slot de guardado (1-10)")
    
    # Info general
    nombre_partida: str
    tiempo_jugado: str = "0h 0m"
    
    # Personaje completo (serializado)
    personaje: Dict[str, Any]
    
    # Contexto narrativo
    contexto: ContextoNarrativo
    
    # Estado de combate (si aplica)
    combate: EstadoCombateGuardado
    
    # Datos adicionales
    configuracion: Dict[str, Any] = Field(default_factory=dict)
    
    def nombre_archivo(self) -> str:
        """Genera el nombre del archivo de guardado"""
        fecha = self.timestamp.strftime("%Y%m%d_%H%M%S")
        return f"partida_slot{self.slot}_{fecha}.json"
    
    def resumen_corto(self) -> str:
        """Resumen corto para mostrar en menú de carga"""
        personaje_nombre = self.personaje.get('nombre', 'Desconocido')
        nivel = self.personaje.get('nivel', 1)
        ubicacion = self.contexto.ubicacion_actual
        
        return (
            f"Slot {self.slot}: {personaje_nombre} (Nivel {nivel})\n"
            f"  Ubicación: {ubicacion}\n"
            f"  Tiempo jugado: {self.tiempo_jugado}\n"
            f"  Guardado: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class InfoSlot(BaseModel):
    """Información resumida de un slot de guardado"""
    slot: int
    existe: bool
    nombre_personaje: Optional[str] = None
    nivel: Optional[int] = None
    ubicacion: Optional[str] = None
    timestamp: Optional[datetime] = None
    tiempo_jugado: Optional[str] = None
    
    def __str__(self) -> str:
        if not self.existe:
            return f"Slot {self.slot}: [VACÍO]"
        
        return (
            f"Slot {self.slot}: {self.nombre_personaje} (Nivel {self.nivel})\n"
            f"  📍 {self.ubicacion}\n"
            f"  ⏱️  {self.tiempo_jugado}\n"
            f"  📅 {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
        )


if __name__ == "__main__":
    print("=== Sistema de Estructuras de Persistencia ===\n")
    
    # Ejemplo de contexto narrativo
    contexto = ContextoNarrativo(
        checkpoint_actual="ciudad_amarth_taberna",
        ubicacion_actual="Taberna 'El Dragón Dorado'"
    )
    
    contexto.npcs_conocidos.extend(["Marcus el Herrero", "Elara la Sanadora"])
    contexto.reputacion["Guardia de Amarth"] = 15
    contexto.reputacion["Gremio de Mercenarios"] = -5
    
    # Agregar eventos
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.COMBATE,
        descripcion="Derrotaste a un bandido en las afueras de Amarth",
        relevancia="alta"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.DIALOGO,
        descripcion="Conversación con Marcus sobre armas mejoradas",
        relevancia="media"
    ))
    
    print(contexto.obtener_resumen_para_ia())