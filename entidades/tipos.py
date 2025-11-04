"""
Tipos, enums y constantes del sistema Ether Blades.
Define todas las enumeraciones usadas en el juego.
"""
from enum import Enum


class HephixTipo(str, Enum):
    """Tipos de Hephix (magia)"""
    # Generales
    ELEMENTAL = "elemental"
    PSIQUICA = "psiquica"
    OCULTA = "oculta"
    MORPHICA = "morphica"
    ESPIRITUAL = "espiritual"
    CRISTALINA = "cristalina"
    SANGRIENTA = "sangrienta"  # Caso especial: sin PM/PCF/PCT
    
    # Kairenistas (luz)
    SANADORA = "sanadora"
    EXORCISTA = "exorcista"
    LUMINICA = "luminica"
    
    # Vadhenistas (oscuridad)
    CAOTICA = "caotica"
    NIGROMANTE = "nigromante"
    OSCURA = "oscura"


class ClaseTipo(str, Enum):
    """Clases de personaje"""
    CURANDERO = "curandero"
    GUERRERO = "guerrero"
    MAGO = "mago"
    EXPLORADOR = "explorador"
    ARTESANO = "artesano"
    DIPLOMATICO = "diplomatico"


class TipoArma(str, Enum):
    """Categorías de armas"""
    CORTANTE_PUNZANTE = "armas_cortantes"
    CONTUNDENTE = "armas_contundentes"
    MAGICA = "armas_magicas"
    DISTANCIA = "armas_distancia"
    PUGILISMO = "pugilismo"


class TipoAtaque(str, Enum):
    """Tipos de ataque según mecánica"""
    MELEE = "melee"
    DISTANCIA = "distancia"
    MAGICO = "magico"


class TipoArmadura(str, Enum):
    """Tipos de armadura"""
    LIGERA = "ligera"
    MEDIA = "media"
    PESADA = "pesada"
    MAGICA = "magica"


class RarezaItem(str, Enum):
    """Rareza de ítems y equipamiento"""
    COMUN = "comun"
    POCO_COMUN = "poco_comun"
    RARO = "raro"
    EPICO = "epico"
    LEGENDARIO = "legendario"


class EstadoCombate(str, Enum):
    """Estados posibles en combate"""
    FUERA_COMBATE = "fuera_combate"
    EN_COMBATE = "en_combate"
    TURNO_JUGADOR = "turno_jugador"
    TURNO_ENEMIGO = "turno_enemigo"
    COMBATE_FINALIZADO = "combate_finalizado"


class TipoAccion(str, Enum):
    """Acciones posibles en combate"""
    ATACAR = "atacar"
    DEFENDER = "defender"
    USAR_HABILIDAD = "usar_habilidad"
    USAR_ITEM = "usar_item"
    HUIR = "huir"


# Constantes del sistema
class Constantes:
    """Constantes globales del juego"""
    
    # Puntos iniciales para distribución
    PUNTOS_CARACTERISTICAS = 20
    PUNTOS_COMBATE = 10
    PUNTOS_EDUCACION = 10
    PUNTOS_TALENTO = 10
    
    # Fórmulas de stats derivados
    MULTIPLICADOR_PV = 10  # PV = Res × 10
    MULTIPLICADOR_PM = 5   # PM = Vol × 5
    MULTIPLICADOR_PCF = 5  # PCF = Fue × 5
    MULTIPLICADOR_PCT = 5  # PCT = Pun × 5
    MULTIPLICADOR_STAMINA = 5  # Coef. Stamina = Sta × 5
    
    # Bonus Hephix Sangriento
    MULTIPLICADOR_PV_SANGRIENTO = 5  # +Vol × 5 PV
    
    # Combate
    DADOS_ATAQUE = 3  # 3d6 para ataque
    DADOS_DEFENSA = 2  # 2d6 para defensa
    DADOS_INICIATIVA = 1  # 1d10 para iniciativa
    UMBRAL_CONTRAATAQUE = -3  # Si diferencia ≤ -3, hay contraataque
    
    # Habilidades
    BONUS_HABILIDAD_POR_NIVEL = 5  # Cada 5 puntos de habilidad = +1 daño
    PUNTOS_MENTALIDAD_POR_HABILIDAD_EXTRA = 10  # Cada 10 mentalidad = +1 habilidad
    
    # Sanación
    BONUS_SANACION_POR_MEDICINA = 5  # Cada 5 medicina = +bonus
    TURNOS_PRIMEROS_AUXILIOS = 1
    TURNOS_KIT_ATENCION = 2
    BASE_PRIMEROS_AUXILIOS = 10
    BASE_KIT_ATENCION = 30
    
    # Adicción (drogas)
    PUNTOS_POR_NIVEL_ADICCION = 20  # Cada 20 puntos = 1 nivel
    
    # Sistema de comprensión
    PUNTOS_COMPRENSION_MAX = 100


# Nombres de habilidades (para validación)
class NombresHabilidades:
    """Nombres estándar de habilidades"""
    
    # Combate
    ARMAS_CORTANTES = "armas_cortantes"
    ARMAS_CONTUNDENTES = "armas_contundentes"
    ARMAS_MAGICAS = "armas_magicas"
    ARMAS_DISTANCIA = "armas_distancia"
    PUGILISMO = "pugilismo"
    
    # Educación
    MEDICINA = "medicina"
    ELOCUENCIA = "elocuencia"
    MANUAL = "manual"
    ARCANISMO = "arcanismo"
    
    # Talento
    SIGILO = "sigilo"
    PERCEPCION = "percepcion"
    MENTALIDAD = "mentalidad"
    ASTRALIDAD = "astralidad"
    
    @classmethod
    def todas_combate(cls) -> list[str]:
        return [
            cls.ARMAS_CORTANTES,
            cls.ARMAS_CONTUNDENTES,
            cls.ARMAS_MAGICAS,
            cls.ARMAS_DISTANCIA,
            cls.PUGILISMO
        ]
    
    @classmethod
    def todas_educacion(cls) -> list[str]:
        return [
            cls.MEDICINA,
            cls.ELOCUENCIA,
            cls.MANUAL,
            cls.ARCANISMO
        ]
    
    @classmethod
    def todas_talento(cls) -> list[str]:
        return [
            cls.SIGILO,
            cls.PERCEPCION,
            cls.MENTALIDAD,
            cls.ASTRALIDAD
        ]


if __name__ == "__main__":
    print("=== Tipos y Constantes de Ether Blades ===\n")
    
    print(f"Tipos de Hephix disponibles: {len(HephixTipo)}")
    for h in HephixTipo:
        print(f"  - {h.value}")
    
    print(f"\nClases disponibles: {len(ClaseTipo)}")
    for c in ClaseTipo:
        print(f"  - {c.value}")
    
    print(f"\nConstantes del sistema:")
    print(f"  Puntos iniciales características: {Constantes.PUNTOS_CARACTERISTICAS}")
    print(f"  Fórmula PV: Res × {Constantes.MULTIPLICADOR_PV}")
    print(f"  Fórmula PM: Vol × {Constantes.MULTIPLICADOR_PM}")