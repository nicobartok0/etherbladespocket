"""
Patrón Strategy - Permite intercambiar algoritmos en tiempo de ejecución.
Se usa para cálculos de ataque, comportamiento de IA, etc.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from entidades.personaje import Personaje
    from entidades.arma import Arma


class TipoAtaque(str, Enum):
    """Tipos de ataque según el arma"""
    MELEE = "melee"
    DISTANCIA = "distancia"
    MAGICO = "magico"


class EstrategiaAtaque(ABC):
    """
    Estrategia base para calcular ataques.
    Define la interfaz común para todos los tipos de ataque.
    """
    
    @abstractmethod
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """
        Calcula el coeficiente de ataque.
        
        Args:
            atacante: Personaje que ataca
            arma: Arma utilizada
            dados: Resultado de las tiradas de dados
        
        Returns:
            Coeficiente de ataque total
        """
        pass
    
    @abstractmethod
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        """
        Obtiene el stat base para este tipo de ataque.
        
        Returns:
            Valor de la característica relevante (Fue/Pun/Vol)
        """
        pass


class EstrategiaAtaqueMelee(EstrategiaAtaque):
    """Estrategia para ataques cuerpo a cuerpo (usa Fuerza)"""
    
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """CA = Fuerza + 3d6 + bonus_arma"""
        stat = self.obtener_stat_base(atacante)
        suma_dados = sum(dados)
        bonus_arma = arma.bonus if arma else 0
        bonus_habilidad = atacante.obtener_bonus_habilidad_arma(arma)
        
        return stat + suma_dados + bonus_arma + bonus_habilidad
    
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        return atacante.ficha.fuerza


class EstrategiaAtaqueDistancia(EstrategiaAtaque):
    """Estrategia para ataques a distancia (usa Puntería)"""
    
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """CA = Puntería + 3d6 + bonus_arma"""
        stat = self.obtener_stat_base(atacante)
        suma_dados = sum(dados)
        bonus_arma = arma.bonus if arma else 0
        bonus_habilidad = atacante.obtener_bonus_habilidad_arma(arma)
        
        return stat + suma_dados + bonus_arma + bonus_habilidad
    
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        return atacante.ficha.punteria


class EstrategiaAtaqueMagico(EstrategiaAtaque):
    """Estrategia para ataques mágicos (usa Voluntad)"""
    
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """CA = Voluntad + 3d6 + bonus_arma"""
        stat = self.obtener_stat_base(atacante)
        suma_dados = sum(dados)
        bonus_arma = arma.bonus if arma else 0
        bonus_habilidad = atacante.obtener_bonus_habilidad_arma(arma)
        
        return stat + suma_dados + bonus_arma + bonus_habilidad
    
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        return atacante.ficha.voluntad


class RegistroEstrategiasAtaque:
    """
    Registro centralizado de estrategias de ataque.
    Permite obtener la estrategia correcta según el tipo de arma.
    """
    
    _estrategias: Dict[TipoAtaque, EstrategiaAtaque] = {
        TipoAtaque.MELEE: EstrategiaAtaqueMelee(),
        TipoAtaque.DISTANCIA: EstrategiaAtaqueDistancia(),
        TipoAtaque.MAGICO: EstrategiaAtaqueMagico()
    }
    
    @classmethod
    def obtener(cls, tipo: TipoAtaque) -> EstrategiaAtaque:
        """Obtiene la estrategia correspondiente al tipo de ataque"""
        return cls._estrategias[tipo]
    
    @classmethod
    def registrar(cls, tipo: TipoAtaque, estrategia: EstrategiaAtaque):
        """Permite registrar estrategias personalizadas"""
        cls._estrategias[tipo] = estrategia


# ============================================================================
# Estrategias de IA para enemigos
# ============================================================================

class ComportamientoIA(ABC):
    """
    Estrategia base para el comportamiento de enemigos.
    Define cómo un enemigo decide sus acciones en combate.
    """
    
    @abstractmethod
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide qué acción tomará el enemigo.
        
        Args:
            enemigo: El enemigo que decide
            objetivos: Lista de posibles objetivos (jugadores)
            estado_combate: Estado actual del combate
        
        Returns:
            Dict con la acción decidida:
            {
                "tipo": "atacar" | "defender" | "habilidad",
                "objetivo": Personaje | None,
                "habilidad": Habilidad | None
            }
        """
        pass


class IAAgresiva(ComportamientoIA):
    """IA que siempre ataca al objetivo con menos PV"""
    
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        # Buscar objetivo con menos PV
        objetivo = min(objetivos, key=lambda p: p.pv_actuales)
        
        return {
            "tipo": "atacar",
            "objetivo": objetivo,
            "habilidad": None
        }


class IADefensiva(ComportamientoIA):
    """IA que defiende cuando tiene poca vida y ataca cuando está saludable"""
    
    def __init__(self, umbral_defensa: float = 0.3):
        """
        Args:
            umbral_defensa: % de vida bajo el cual defiende (0.3 = 30%)
        """
        self.umbral_defensa = umbral_defensa
    
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        # Calcular porcentaje de vida
        porcentaje_vida = enemigo.pv_actuales / enemigo.ficha.pv_maximos
        
        if porcentaje_vida < self.umbral_defensa:
            return {
                "tipo": "defender",
                "objetivo": None,
                "habilidad": None
            }
        else:
            # Atacar al más peligroso (mayor ataque)
            objetivo = max(objetivos, key=lambda p: p.ficha.fuerza)
            return {
                "tipo": "atacar",
                "objetivo": objetivo,
                "habilidad": None
            }


class IATactica(ComportamientoIA):
    """IA que usa habilidades cuando es apropiado"""
    
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        # Si hay múltiples objetivos y tiene habilidad de área
        if len(objetivos) > 2 and enemigo.pm_actuales > 20:
            # TODO: Buscar habilidad de área
            pass
        
        # Si alguien está muy dañado, rematar
        objetivo_debil = min(objetivos, key=lambda p: p.pv_actuales)
        if objetivo_debil.pv_actuales < 20:
            return {
                "tipo": "atacar",
                "objetivo": objetivo_debil,
                "habilidad": None
            }
        
        # Caso por defecto: atacar al que más daño hace
        objetivo = max(objetivos, key=lambda p: p.ficha.fuerza)
        return {
            "tipo": "atacar",
            "objetivo": objetivo,
            "habilidad": None
        }


class RegistroComportamientosIA:
    """Registro de comportamientos de IA disponibles"""
    
    _comportamientos: Dict[str, ComportamientoIA] = {
        "agresiva": IAAgresiva(),
        "defensiva": IADefensiva(),
        "tactica": IATactica()
    }
    
    @classmethod
    def obtener(cls, tipo: str) -> ComportamientoIA:
        """Obtiene un comportamiento por nombre"""
        if tipo not in cls._comportamientos:
            raise ValueError(f"Comportamiento '{tipo}' no encontrado")
        return cls._comportamientos[tipo]
    
    @classmethod
    def registrar(cls, nombre: str, comportamiento: ComportamientoIA):
        """Registra un nuevo comportamiento de IA"""
        cls._comportamientos[nombre] = comportamiento
    
    @classmethod
    def listar_disponibles(cls) -> list[str]:
        """Lista todos los comportamientos disponibles"""
        return list(cls._comportamientos.keys())


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Estrategias de Ataque ===")
    print(f"Tipos disponibles: {[t.value for t in TipoAtaque]}")
    
    print("\n=== Comportamientos de IA ===")
    print(f"Comportamientos: {RegistroComportamientosIA.listar_disponibles()}")
    
    # Ejemplo de uso de estrategia
    estrategia_melee = RegistroEstrategiasAtaque.obtener(TipoAtaque.MELEE)
    print(f"\nEstrategia Melee: {estrategia_melee.__class__.__name__}")