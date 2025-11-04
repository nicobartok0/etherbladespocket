"""
Módulo de patrones de diseño para Ether Blades.
Exporta las clases principales de cada patrón.
"""

from .singleton import SingletonMeta
from .factory_method import Factory, FactoryConRegistro, FactoryDesdeJSON
from .observer import EventBus, Evento, TipoEvento, EventCallback
from .strategy import (
    EstrategiaAtaque,
    EstrategiaAtaqueMelee,
    EstrategiaAtaqueDistancia,
    EstrategiaAtaqueMagico,
    RegistroEstrategiasAtaque,
    TipoAtaque,
    ComportamientoIA,
    IAAgresiva,
    IADefensiva,
    IATactica,
    RegistroComportamientosIA
)

__all__ = [
    # Singleton
    'SingletonMeta',
    
    # Factory
    'Factory',
    'FactoryConRegistro',
    'FactoryDesdeJSON',
    
    # Observer
    'EventBus',
    'Evento',
    'TipoEvento',
    'EventCallback',
    
    # Strategy - Ataque
    'EstrategiaAtaque',
    'EstrategiaAtaqueMelee',
    'EstrategiaAtaqueDistancia',
    'EstrategiaAtaqueMagico',
    'RegistroEstrategiasAtaque',
    'TipoAtaque',
    
    # Strategy - IA
    'ComportamientoIA',
    'IAAgresiva',
    'IADefensiva',
    'IATactica',
    'RegistroComportamientosIA',
]