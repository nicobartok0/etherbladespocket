"""
Clase Hephix - Representa el tipo de magia del personaje.
"""
from pydantic import BaseModel, Field
from typing import Optional
from .tipos import HephixTipo, Constantes


class Hephix(BaseModel):
    """
    Representa el Hephix (marca de nacimiento mágica) del personaje.
    Define qué tipo de magia puede usar.
    """
    
    tipo: HephixTipo
    nivel: int = Field(default=1, ge=1, le=30)
    descripcion: str = ""
    
    # Habilidades mágicas desbloqueadas por nivel
    habilidades_desbloqueadas: list[str] = Field(default_factory=list)
    
    def es_sangriento(self) -> bool:
        """
        Verifica si es el hephix especial 'Sangriento'.
        Este hephix tiene mecánicas únicas (sin PM/PCF/PCT, más PV).
        """
        return self.tipo == HephixTipo.SANGRIENTA
    
    def es_kairenista(self) -> bool:
        """Verifica si pertenece a la rama Kairenista (luz)"""
        return self.tipo in [
            HephixTipo.SANADORA,
            HephixTipo.EXORCISTA,
            HephixTipo.LUMINICA
        ]
    
    def es_vadhenista(self) -> bool:
        """Verifica si pertenece a la rama Vadhenista (oscuridad)"""
        return self.tipo in [
            HephixTipo.CAOTICA,
            HephixTipo.NIGROMANTE,
            HephixTipo.OSCURA
        ]
    
    def calcular_modificador_pv(self, voluntad: int) -> int:
        """
        Calcula el modificador de PV según el hephix.
        Solo el Hephix Sangriento da bonus de PV.
        
        Args:
            voluntad: Stat de Voluntad del personaje
        
        Returns:
            Puntos de vida adicionales
        """
        if self.es_sangriento():
            return voluntad * Constantes.MULTIPLICADOR_PV_SANGRIENTO
        return 0
    
    def puede_usar_pm(self) -> bool:
        """Verifica si puede usar Puntos de Magia"""
        return not self.es_sangriento()
    
    def puede_usar_pcf(self) -> bool:
        """Verifica si puede usar Puntos de Conexión Física"""
        return not self.es_sangriento()
    
    def puede_usar_pct(self) -> bool:
        """Verifica si puede usar Puntos de Conexión Tenaz"""
        return not self.es_sangriento()
    
    def obtener_nivel_siguiente_habilidad(self) -> Optional[int]:
        """
        Obtiene el nivel en el que se desbloqueará la próxima habilidad.
        Las habilidades se desbloquean cada 3 niveles: 3, 6, 9, ..., 30
        
        Returns:
            Nivel de la próxima habilidad o None si ya tiene todas
        """
        niveles_habilidad = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
        
        for nivel in niveles_habilidad:
            if self.nivel < nivel:
                return nivel
        
        return None  # Ya tiene todas las habilidades
    
    def desbloquear_habilidad(self, nombre_habilidad: str):
        """
        Desbloquea una nueva habilidad mágica.
        
        Args:
            nombre_habilidad: Nombre de la habilidad a desbloquear
        """
        if nombre_habilidad not in self.habilidades_desbloqueadas:
            self.habilidades_desbloqueadas.append(nombre_habilidad)
    
    def subir_nivel(self):
        """Incrementa el nivel del hephix"""
        if self.nivel < 30:
            self.nivel += 1
    
    @classmethod
    def crear_desde_tipo(cls, tipo: HephixTipo, descripcion: str = "") -> "Hephix":
        """
        Factory method para crear un Hephix desde su tipo.
        
        Args:
            tipo: Tipo de hephix
            descripcion: Descripción del hephix (opcional)
        
        Returns:
            Nueva instancia de Hephix
        """
        return cls(
            tipo=tipo,
            nivel=1,
            descripcion=descripcion
        )
    
    def __str__(self) -> str:
        especialidad = ""
        if self.es_kairenista():
            especialidad = " (Kairenista)"
        elif self.es_vadhenista():
            especialidad = " (Vadhenista)"
        elif self.es_sangriento():
            especialidad = " (⚠️ ESPECIAL)"
        
        return f"Hephix {self.tipo.value.title()}{especialidad} - Nivel {self.nivel}"
    
    model_config = {"use_enum_values": False}  # Mantener enums como objetos


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Sistema de Hephix ===\n")
    
    # Hephix normal
    hephix_elemental = Hephix.crear_desde_tipo(
        HephixTipo.ELEMENTAL,
        "Control sobre fuego, agua, tierra y aire"
    )
    print(f"{hephix_elemental}")
    print(f"  ¿Puede usar PM? {hephix_elemental.puede_usar_pm()}")
    print(f"  Modificador PV: +{hephix_elemental.calcular_modificador_pv(5)}\n")
    
    # Hephix Sangriento (especial)
    hephix_sangriento = Hephix.crear_desde_tipo(
        HephixTipo.SANGRIENTA,
        "Sacrifica integridad corporal por poder"
    )
    print(f"{hephix_sangriento}")
    print(f"  ¿Puede usar PM? {hephix_sangriento.puede_usar_pm()}")
    print(f"  Modificador PV (Vol=8): +{hephix_sangriento.calcular_modificador_pv(8)}")
    print(f"  ⚠️ Sin PM/PCF/PCT\n")
    
    # Hephix Kairenista
    hephix_sanadora = Hephix.crear_desde_tipo(HephixTipo.SANADORA)
    print(f"{hephix_sanadora}")
    print(f"  Es Kairenista: {hephix_sanadora.es_kairenista()}")
    print(f"  Próxima habilidad en nivel: {hephix_sanadora.obtener_nivel_siguiente_habilidad()}")