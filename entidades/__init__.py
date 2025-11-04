"""
Módulo de entidades del dominio.
Exporta todas las clases principales del juego.
"""

# Tipos y enums
from .tipos import (
    HephixTipo,
    ClaseTipo,
    TipoArma,
    TipoAtaque,
    TipoArmadura,
    RarezaItem,
    EstadoCombate,
    TipoAccion,
    Constantes,
    NombresHabilidades
)

# Sistema de dados
from .dados import (
    ResultadoTirada,
    tirar_dados,
    tirar_d6,
    tirar_d10,
    tirar_d12,
    tirar_d20,
    tirar_d100,
    tirar_ataque,
    tirar_defensa,
    establecer_semilla
)

# Hephix
from .hephix import Hephix

# Ficha
from .ficha import (
    Caracteristicas,
    HabilidadesCombate,
    HabilidadesEducacion,
    HabilidadesTalento,
    Ficha
)

# Armas y armaduras
from .arma import (
    Arma,
    Armadura,
    crear_espada_basica,
    crear_arco_basico,
    crear_baston_basico,
    crear_armadura_ligera
)

# Inventario
from .inventario import (
    Item,
    ItemConsumible,
    ItemDroga,
    Inventario,
    crear_pocion_vida_menor,
    crear_botiquin_primeros_auxilios,
    crear_kit_atencion_medica
)

# Personaje
from .personaje import Personaje

__all__ = [
    # Tipos
    'HephixTipo',
    'ClaseTipo',
    'TipoArma',
    'TipoAtaque',
    'TipoArmadura',
    'RarezaItem',
    'EstadoCombate',
    'TipoAccion',
    'Constantes',
    'NombresHabilidades',
    
    # Dados
    'ResultadoTirada',
    'tirar_dados',
    'tirar_d6',
    'tirar_d10',
    'tirar_d12',
    'tirar_d20',
    'tirar_d100',
    'tirar_ataque',
    'tirar_defensa',
    'establecer_semilla',
    
    # Hephix
    'Hephix',
    
    # Ficha
    'Caracteristicas',
    'HabilidadesCombate',
    'HabilidadesEducacion',
    'HabilidadesTalento',
    'Ficha',
    
    # Armas
    'Arma',
    'Armadura',
    'crear_espada_basica',
    'crear_arco_basico',
    'crear_baston_basico',
    'crear_armadura_ligera',
    
    # Inventario
    'Item',
    'ItemConsumible',
    'ItemDroga',
    'Inventario',
    'crear_pocion_vida_menor',
    'crear_botiquin_primeros_auxilios',
    'crear_kit_atencion_medica',
    
    # Personaje
    'Personaje',
]