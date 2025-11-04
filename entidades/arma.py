"""
Clases de Arma y Armadura para el sistema de combate.
"""
from pydantic import BaseModel, Field
from typing import Optional
from .tipos import TipoArma, TipoAtaque, TipoArmadura, RarezaItem


class Arma(BaseModel):
    """
    Clase base para todas las armas del juego.
    """
    
    nombre: str
    descripcion: str = ""
    
    # Clasificación
    tipo_arma: TipoArma  # armas_cortantes, contundentes, etc.
    tipo_ataque: TipoAtaque  # melee, distancia, magico
    
    # Stats de combate
    daño_base: int = Field(default=0, ge=0)
    bonus: int = Field(default=0, description="Bonus al coeficiente de ataque")
    
    # Requisitos
    nivel_requerido: int = Field(default=1, ge=1)
    habilidad_minima: int = Field(default=0, ge=0, description="Nivel mínimo en la habilidad del arma")
    
    # Propiedades
    rareza: RarezaItem = Field(default=RarezaItem.COMUN)
    es_magica: bool = Field(default=False)
    mejora_mecanica: int = Field(default=0, ge=0, le=10, description="Mejora de Manual")
    mejora_magica: int = Field(default=0, ge=0, le=10, description="Mejora de Arcanismo")
    
    # Durabilidad (opcional para futuro)
    durabilidad_actual: Optional[int] = None
    durabilidad_maxima: Optional[int] = None
    
    def bonus_total(self) -> int:
        """
        Calcula el bonus total del arma.
        Incluye: bonus base + mejora mecánica + mejora mágica
        NOTA: Las mejoras mecánicas y mágicas no pueden coexistir
        """
        if self.mejora_mecanica > 0 and self.mejora_magica > 0:
            # Solo debería tener una, usar la mayor
            mejora = max(self.mejora_mecanica, self.mejora_magica)
        else:
            mejora = self.mejora_mecanica + self.mejora_magica
        
        return self.bonus + mejora
    
    def puede_mejorar_mecanicamente(self) -> bool:
        """Verifica si puede recibir mejora mecánica"""
        return self.mejora_magica == 0 and self.mejora_mecanica < 10
    
    def puede_mejorar_magicamente(self) -> bool:
        """Verifica si puede recibir mejora mágica"""
        return self.mejora_mecanica == 0 and self.mejora_magica < 10
    
    def aplicar_mejora_mecanica(self, nivel_manual: int) -> bool:
        """
        Aplica mejora mecánica según nivel de habilidad Manual.
        
        Args:
            nivel_manual: Nivel de la habilidad Manual del personaje
        
        Returns:
            True si se aplicó la mejora, False si no cumple requisitos
        """
        # Tabla de mejoras (nivel_requerido: bonus)
        tabla_mejoras = {
            9: 1, 12: 2, 15: 3, 18: 4, 21: 5,
            24: 6, 27: 8, 30: 10
        }
        
        if not self.puede_mejorar_mecanicamente():
            return False
        
        # Buscar la mejora más alta que puede aplicar
        for nivel_req, bonus in sorted(tabla_mejoras.items(), reverse=True):
            if nivel_manual >= nivel_req:
                self.mejora_mecanica = bonus
                return True
        
        return False
    
    def aplicar_mejora_magica(self, nivel_arcanismo: int) -> bool:
        """
        Aplica mejora mágica según nivel de habilidad Arcanismo.
        
        Args:
            nivel_arcanismo: Nivel de la habilidad Arcanismo del personaje
        
        Returns:
            True si se aplicó la mejora, False si no cumple requisitos
        """
        # Tabla de mejoras (igual que mecánica)
        tabla_mejoras = {
            9: 1, 12: 2, 15: 3, 18: 4, 21: 5,
            24: 6, 27: 8, 30: 10
        }
        
        if not self.puede_mejorar_magicamente():
            return False
        
        for nivel_req, bonus in sorted(tabla_mejoras.items(), reverse=True):
            if nivel_arcanismo >= nivel_req:
                self.mejora_magica = bonus
                self.es_magica = True
                return True
        
        return False
    
    def __str__(self) -> str:
        mejora_str = ""
        if self.mejora_mecanica > 0:
            mejora_str = f" +{self.mejora_mecanica} (Mecánica)"
        elif self.mejora_magica > 0:
            mejora_str = f" +{self.mejora_magica} (Mágica)"
        
        return f"{self.nombre}{mejora_str} (Bonus: +{self.bonus_total()})"


class Armadura(BaseModel):
    """
    Representa una armadura equipable.
    """
    
    nombre: str
    descripcion: str = ""
    
    # Clasificación
    tipo: TipoArmadura
    
    # Stats de defensa
    reduccion_daño: int = Field(default=0, ge=0, description="Reduce daño recibido")
    bonus_reflejos: int = Field(default=0, description="Modificador a Reflejos")
    
    # Requisitos
    nivel_requerido: int = Field(default=1, ge=1)
    resistencia_minima: int = Field(default=0, ge=0)
    
    # Propiedades
    rareza: RarezaItem = Field(default=RarezaItem.COMUN)
    es_magica: bool = Field(default=False)
    
    # Durabilidad
    durabilidad_actual: Optional[int] = None
    durabilidad_maxima: Optional[int] = None
    
    def reduccion_total(self) -> int:
        """Calcula la reducción total de daño"""
        return self.reduccion_daño
    
    def __str__(self) -> str:
        return f"{self.nombre} (Reducción: {self.reduccion_daño}, Bonus Reflejos: {self.bonus_reflejos:+d})"


# Ejemplos y factory helpers
def crear_espada_basica() -> Arma:
    """Crea una espada básica de inicio"""
    return Arma(
        nombre="Espada Corta",
        descripcion="Una espada de hierro común",
        tipo_arma=TipoArma.CORTANTE_PUNZANTE,
        tipo_ataque=TipoAtaque.MELEE,
        daño_base=0,
        bonus=2,
        nivel_requerido=1,
        habilidad_minima=0
    )


def crear_arco_basico() -> Arma:
    """Crea un arco básico de inicio"""
    return Arma(
        nombre="Arco Corto",
        descripcion="Un arco de madera simple",
        tipo_arma=TipoArma.DISTANCIA,
        tipo_ataque=TipoAtaque.DISTANCIA,
        daño_base=0,
        bonus=2,
        nivel_requerido=1,
        habilidad_minima=0
    )


def crear_baston_basico() -> Arma:
    """Crea un bastón mágico básico"""
    return Arma(
        nombre="Bastón de Madera",
        descripcion="Un bastón tallado con runas básicas",
        tipo_arma=TipoArma.MAGICA,
        tipo_ataque=TipoAtaque.MAGICO,
        daño_base=0,
        bonus=2,
        nivel_requerido=1,
        habilidad_minima=0,
        es_magica=True
    )


def crear_armadura_ligera() -> Armadura:
    """Crea una armadura ligera básica"""
    return Armadura(
        nombre="Armadura de Cuero",
        descripcion="Protección ligera de cuero curtido",
        tipo=TipoArmadura.LIGERA,
        reduccion_daño=2,
        bonus_reflejos=0,
        nivel_requerido=1
    )


if __name__ == "__main__":
    print("=== Sistema de Armas y Armaduras ===\n")
    
    # Crear arma
    espada = crear_espada_basica()
    print(f"Arma creada: {espada}")
    print(f"  Tipo: {espada.tipo_arma.value}")
    print(f"  Bonus total: +{espada.bonus_total()}\n")
    
    # Probar mejora
    print("Aplicando mejora mecánica (Manual nivel 15):")
    if espada.aplicar_mejora_mecanica(15):
        print(f"  ✅ {espada}")
    
    # Crear armadura
    print("\nArmadura creada:")
    armadura = crear_armadura_ligera()
    print(f"  {armadura}")