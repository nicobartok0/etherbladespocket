"""
Patrón Observer - Sistema de eventos para desacoplar componentes.
Permite que múltiples objetos reaccionen a eventos sin conocerse entre sí.
"""
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# Tipos de eventos del sistema
class TipoEvento(str, Enum):
    """Enum con todos los tipos de eventos del juego"""
    # Eventos de combate
    COMBATE_INICIADO = "combate_iniciado"
    TURNO_INICIADO = "turno_iniciado"
    ATAQUE_REALIZADO = "ataque_realizado"
    ATAQUE_BLOQUEADO = "ataque_bloqueado"
    CONTRAATAQUE = "contraataque"
    GOLPE_GRACIA = "golpe_gracia"
    DAÑO_RECIBIDO = "daño_recibido"
    STAMINA_AGOTADA = "stamina_agotada"
    
    # Eventos de personaje
    PERSONAJE_HERIDO = "personaje_herido"
    PERSONAJE_CURADO = "personaje_curado"
    PERSONAJE_MUERTO = "personaje_muerto"
    NIVEL_SUBIDO = "nivel_subido"
    HABILIDAD_DESBLOQUEADA = "habilidad_desbloqueada"
    
    # Eventos de magia
    HECHIZO_LANZADO = "hechizo_lanzado"
    MANA_AGOTADO = "mana_agotado"
    
    # Eventos narrativos
    DECISION_TOMADA = "decision_tomada"
    CHECKPOINT_ALCANZADO = "checkpoint_alcanzado"
    MISION_COMPLETADA = "mision_completada"
    
    # Eventos de sistema
    PARTIDA_GUARDADA = "partida_guardada"
    PARTIDA_CARGADA = "partida_cargada"
    ERROR_SISTEMA = "error_sistema"


@dataclass
class Evento:
    """
    Representa un evento del sistema con su información asociada.
    """
    tipo: TipoEvento
    datos: Dict[str, Any]
    timestamp: datetime
    prioridad: int = 0  # Mayor número = mayor prioridad
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


# Tipo para callbacks
EventCallback = Callable[[Evento], None]


class EventBus:
    """
    Bus de eventos central del sistema.
    Implementa el patrón Observer/Pub-Sub.
    """
    
    def __init__(self):
        self._subscriptores: Dict[TipoEvento, List[EventCallback]] = {}
        self._historial: List[Evento] = []
        self._max_historial = 100  # Mantener últimos 100 eventos
        self._activo = True
    
    def suscribir(self, tipo_evento: TipoEvento, callback: EventCallback) -> None:
        """
        Suscribe un callback a un tipo de evento específico.
        
        Args:
            tipo_evento: Tipo de evento al que suscribirse
            callback: Función que se llamará cuando ocurra el evento
                     Debe aceptar un parámetro de tipo Evento
        
        Ejemplo:
            def manejador(evento: Evento):
                print(f"Recibido: {evento.tipo}")
            
            bus.suscribir(TipoEvento.ATAQUE_REALIZADO, manejador)
        """
        if tipo_evento not in self._subscriptores:
            self._subscriptores[tipo_evento] = []
        
        if callback not in self._subscriptores[tipo_evento]:
            self._subscriptores[tipo_evento].append(callback)
    
    def desuscribir(self, tipo_evento: TipoEvento, callback: EventCallback) -> None:
        """
        Remueve un callback de la lista de subscriptores.
        
        Args:
            tipo_evento: Tipo de evento
            callback: Callback a remover
        """
        if tipo_evento in self._subscriptores:
            try:
                self._subscriptores[tipo_evento].remove(callback)
            except ValueError:
                pass  # El callback no estaba suscrito
    
    def publicar(self, tipo_evento: TipoEvento, datos: Dict[str, Any] = None, 
                 prioridad: int = 0) -> None:
        """
        Publica un evento, notificando a todos los subscriptores.
        
        Args:
            tipo_evento: Tipo de evento a publicar
            datos: Información asociada al evento
            prioridad: Prioridad del evento (mayor = más importante)
        
        Ejemplo:
            bus.publicar(
                TipoEvento.DAÑO_RECIBIDO,
                {"personaje": "Aldric", "daño": 25, "pv_restantes": 45}
            )
        """
        if not self._activo:
            return
        
        # Crear evento
        evento = Evento(
            tipo=tipo_evento,
            datos=datos or {},
            timestamp=datetime.now(),
            prioridad=prioridad
        )
        
        # Agregar al historial
        self._historial.append(evento)
        if len(self._historial) > self._max_historial:
            self._historial.pop(0)
        
        # Notificar subscriptores
        if tipo_evento in self._subscriptores:
            for callback in self._subscriptores[tipo_evento]:
                try:
                    callback(evento)
                except Exception as e:
                    # Log del error pero continuar notificando otros subscriptores
                    print(f"Error en callback de {tipo_evento}: {e}")
    
    def obtener_historial(self, tipo_evento: TipoEvento = None, 
                          limite: int = None) -> List[Evento]:
        """
        Obtiene el historial de eventos.
        
        Args:
            tipo_evento: Filtrar por tipo (None = todos)
            limite: Cantidad máxima de eventos a retornar
        
        Returns:
            Lista de eventos (más recientes primero)
        """
        eventos = self._historial[::-1]  # Invertir (más recientes primero)
        
        if tipo_evento:
            eventos = [e for e in eventos if e.tipo == tipo_evento]
        
        if limite:
            eventos = eventos[:limite]
        
        return eventos
    
    def limpiar_historial(self) -> None:
        """Limpia el historial de eventos"""
        self._historial.clear()
    
    def pausar(self) -> None:
        """Pausa la publicación de eventos (útil para debugging)"""
        self._activo = False
    
    def reanudar(self) -> None:
        """Reanuda la publicación de eventos"""
        self._activo = True
    
    def contar_subscriptores(self, tipo_evento: TipoEvento = None) -> int:
        """
        Cuenta subscriptores de un evento específico o en total.
        
        Args:
            tipo_evento: Tipo específico (None = todos)
        
        Returns:
            Cantidad de subscriptores
        """
        if tipo_evento:
            return len(self._subscriptores.get(tipo_evento, []))
        else:
            return sum(len(subs) for subs in self._subscriptores.values())


# Ejemplo de uso
if __name__ == "__main__":
    # Crear bus de eventos
    bus = EventBus()
    
    # Definir manejadores
    def logger(evento: Evento):
        print(f"[LOG] {evento.tipo}: {evento.datos}")
    
    def contador_daño(evento: Evento):
        if "daño" in evento.datos:
            print(f"[CONTADOR] Daño total acumulado: {evento.datos['daño']}")
    
    # Suscribir manejadores
    bus.suscribir(TipoEvento.ATAQUE_REALIZADO, logger)
    bus.suscribir(TipoEvento.DAÑO_RECIBIDO, logger)
    bus.suscribir(TipoEvento.DAÑO_RECIBIDO, contador_daño)
    
    # Publicar eventos
    bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
        "atacante": "Aldric",
        "defensor": "Goblin",
        "resultado": "éxito"
    })
    
    bus.publicar(TipoEvento.DAÑO_RECIBIDO, {
        "personaje": "Goblin",
        "daño": 25,
        "pv_restantes": 15
    })
    
    # Ver historial
    print(f"\n[HISTORIAL] Eventos registrados: {len(bus.obtener_historial())}")
    print(f"[STATS] Subscriptores totales: {bus.contar_subscriptores()}")