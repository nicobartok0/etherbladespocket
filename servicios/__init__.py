"""
Módulo de servicios de aplicación.
Contiene la lógica de negocio del juego.
"""

from .creacion_personaje_service import CreacionPersonajeService
from .combate_service import CombateService
from .combate_estructuras import (
    ResultadoAtaque,
    TipoResultadoAtaque,
    EstadoCombate,
    EstadoCombatiente
)
from .persistencia_service import PersistenciaService
from .persistencia_estructuras import (
    ContextoNarrativo,
    EventoNarrativo,
    TipoEvento as TipoEventoNarrativo,
    DatosPartida,
    InfoSlot
)
from .narrador_service import NarradorService
from .cliente_ia import ClienteIA, ClienteIAMock

__all__ = [
    'CreacionPersonajeService',
    'CombateService',
    'ResultadoAtaque',
    'TipoResultadoAtaque',
    'EstadoCombate',
    'EstadoCombatiente',
    'PersistenciaService',
    'ContextoNarrativo',
    'EventoNarrativo',
    'TipoEventoNarrativo',
    'DatosPartida',
    'InfoSlot',
    'NarradorService',
    'ClienteIA',
    'ClienteIAMock',
]