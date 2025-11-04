"""
Clase Ficha - Representa las estadísticas completas de un personaje.
Incluye características, habilidades y cálculos derivados.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .tipos import Constantes, NombresHabilidades, HephixTipo


class Caracteristicas(BaseModel):
    """
    Las 6 características principales del personaje.
    Total de puntos iniciales: 20
    """
    fuerza: int = Field(default=0, ge=0, le=20, description="Capacidad física y daño cuerpo a cuerpo")
    reflejos: int = Field(default=0, ge=0, le=20, description="Capacidad de esquivar ataques")
    resistencia: int = Field(default=0, ge=0, le=20, description="Puntos de vida y aguante")
    voluntad: int = Field(default=0, ge=0, le=20, description="Poder mágico del Hephix")
    punteria: int = Field(default=0, ge=0, le=20, description="Precisión con armas a distancia")
    stamina: int = Field(default=0, ge=0, le=20, description="Resistencia al cansancio en combate")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return (self.fuerza + self.reflejos + self.resistencia + 
                self.voluntad + self.punteria + self.stamina)
    
    def validar_distribucion(self, puntos_maximos: int = Constantes.PUNTOS_CARACTERISTICAS) -> bool:
        """Valida que no se excedan los puntos disponibles"""
        return self.total_puntos() <= puntos_maximos


class HabilidadesCombate(BaseModel):
    """
    Habilidades de combate.
    Total de puntos iniciales: 10
    """
    armas_cortantes: int = Field(default=0, ge=0, description="Espadas, dagas, lanzas")
    armas_contundentes: int = Field(default=0, ge=0, description="Mazas, martillos")
    armas_magicas: int = Field(default=0, ge=0, description="Bastones, varas mágicas")
    armas_distancia: int = Field(default=0, ge=0, description="Arcos, ballestas")
    pugilismo: int = Field(default=0, ge=0, description="Combate sin armas")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return (self.armas_cortantes + self.armas_contundentes + 
                self.armas_magicas + self.armas_distancia + self.pugilismo)


class HabilidadesEducacion(BaseModel):
    """
    Habilidades de educación.
    Total de puntos iniciales: 10
    """
    medicina: int = Field(default=0, ge=0, description="Sanación y primeros auxilios")
    elocuencia: int = Field(default=0, ge=0, description="Persuasión, mentira, intimidación")
    manual: int = Field(default=0, ge=0, description="Artesanía y mejora mecánica")
    arcanismo: int = Field(default=0, ge=0, description="Encantamientos y mejora mágica")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return self.medicina + self.elocuencia + self.manual + self.arcanismo


class HabilidadesTalento(BaseModel):
    """
    Habilidades de talento.
    Total de puntos iniciales: 10
    """
    sigilo: int = Field(default=0, ge=0, description="Ocultamiento y ataques sorpresa")
    percepcion: int = Field(default=0, ge=0, description="Detectar cambios y objetos")
    mentalidad: int = Field(default=0, ge=0, description="Estrategia y estudio")
    astralidad: int = Field(default=0, ge=0, description="Conexión con lo divino")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return self.sigilo + self.percepcion + self.mentalidad + self.astralidad


class Ficha(BaseModel):
    """
    Ficha completa de un personaje con todas sus estadísticas.
    Incluye características, habilidades y cálculos derivados.
    """
    
    # Características principales (20 puntos)
    caracteristicas: Caracteristicas = Field(default_factory=Caracteristicas)
    
    # Habilidades (10 puntos cada categoría)
    combate: HabilidadesCombate = Field(default_factory=HabilidadesCombate)
    educacion: HabilidadesEducacion = Field(default_factory=HabilidadesEducacion)
    talento: HabilidadesTalento = Field(default_factory=HabilidadesTalento)
    
    # Tipo de Hephix (necesario para cálculos)
    hephix_tipo: Optional[HephixTipo] = None
    
    # ========================================================================
    # Propiedades calculadas (Stats derivados)
    # ========================================================================
    
    @property
    def fuerza(self) -> int:
        return self.caracteristicas.fuerza
    
    @property
    def reflejos(self) -> int:
        return self.caracteristicas.reflejos
    
    @property
    def resistencia(self) -> int:
        return self.caracteristicas.resistencia
    
    @property
    def voluntad(self) -> int:
        return self.caracteristicas.voluntad
    
    @property
    def punteria(self) -> int:
        return self.caracteristicas.punteria
    
    @property
    def stamina(self) -> int:
        return self.caracteristicas.stamina
    
    @property
    def pv_maximos(self) -> int:
        """
        Puntos de Vida máximos.
        Fórmula: Res × 10
        Bonus: +Vol × 5 si tiene Hephix Sangriento
        """
        pv_base = self.resistencia * Constantes.MULTIPLICADOR_PV
        
        # Bonus Hephix Sangriento
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            pv_base += self.voluntad * Constantes.MULTIPLICADOR_PV_SANGRIENTO
        
        return pv_base
    
    @property
    def pm_maximos(self) -> int:
        """
        Puntos de Magia máximos.
        Fórmula: Vol × 5
        Excepción: 0 si tiene Hephix Sangriento
        """
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            return 0
        return self.voluntad * Constantes.MULTIPLICADOR_PM
    
    @property
    def pcf_maximos(self) -> int:
        """
        Puntos de Conexión Física máximos.
        Fórmula: Fue × 5
        Excepción: 0 si tiene Hephix Sangriento
        """
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            return 0
        return self.fuerza * Constantes.MULTIPLICADOR_PCF
    
    @property
    def pct_maximos(self) -> int:
        """
        Puntos de Conexión Tenaz máximos.
        Fórmula: Pun × 5
        Excepción: 0 si tiene Hephix Sangriento
        """
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            return 0
        return self.punteria * Constantes.MULTIPLICADOR_PCT
    
    @property
    def ps_maximos(self) -> int:
        """
        Puntos de Stamina (para combate).
        Fórmula: Sta × 5
        """
        return self.stamina * Constantes.MULTIPLICADOR_STAMINA
    
    # ========================================================================
    # Métodos de validación
    # ========================================================================
    
    def validar_distribucion_completa(self) -> dict[str, bool]:
        """
        Valida que todas las categorías tengan distribución correcta.
        
        Returns:
            Dict con validación de cada categoría
        """
        return {
            "caracteristicas": self.caracteristicas.validar_distribucion(),
            "combate": self.combate.total_puntos() <= Constantes.PUNTOS_COMBATE,
            "educacion": self.educacion.total_puntos() <= Constantes.PUNTOS_EDUCACION,
            "talento": self.talento.total_puntos() <= Constantes.PUNTOS_TALENTO
        }
    
    def es_valida(self) -> bool:
        """Verifica que toda la ficha sea válida"""
        validacion = self.validar_distribucion_completa()
        return all(validacion.values())
    
    # ========================================================================
    # Métodos de bonificación
    # ========================================================================
    
    def obtener_bonus_habilidad(self, habilidad: str) -> int:
        """
        Calcula el bonus de daño por nivel de habilidad.
        Fórmula: +1 de daño cada 5 puntos de habilidad
        
        Args:
            habilidad: Nombre de la habilidad
        
        Returns:
            Bonus de daño
        """
        # Buscar la habilidad en las categorías
        if hasattr(self.combate, habilidad):
            nivel = getattr(self.combate, habilidad)
        elif hasattr(self.educacion, habilidad):
            nivel = getattr(self.educacion, habilidad)
        elif hasattr(self.talento, habilidad):
            nivel = getattr(self.talento, habilidad)
        else:
            return 0
        
        return nivel // Constantes.BONUS_HABILIDAD_POR_NIVEL
    
    def calcular_habilidades_extra_mentalidad(self) -> int:
        """
        Cada 10 puntos de mentalidad = +1 punto de habilidad extra.
        
        Returns:
            Cantidad de puntos extra disponibles
        """
        return self.talento.mentalidad // Constantes.PUNTOS_MENTALIDAD_POR_HABILIDAD_EXTRA
    
    # ========================================================================
    # Métodos de utilidad
    # ========================================================================
    
    def resumen(self) -> str:
        """Genera un resumen legible de la ficha"""
        lineas = [
            "=" * 50,
            "CARACTERÍSTICAS",
            f"  Fuerza: {self.fuerza}",
            f"  Reflejos: {self.reflejos}",
            f"  Resistencia: {self.resistencia}",
            f"  Voluntad: {self.voluntad}",
            f"  Puntería: {self.punteria}",
            f"  Stamina: {self.stamina}",
            "",
            "STATS DERIVADOS",
            f"  PV Máximos: {self.pv_maximos}",
            f"  PM Máximos: {self.pm_maximos}",
            f"  PCF Máximos: {self.pcf_maximos}",
            f"  PCT Máximos: {self.pct_maximos}",
            f"  PS Máximos: {self.ps_maximos}",
            "=" * 50
        ]
        return "\n".join(lineas)
    
    def aplicar_bonificaciones_clase(self, bonificaciones: dict[str, int]):
        """
        Aplica las bonificaciones de una clase a la ficha.
        
        Args:
            bonificaciones: Dict con habilidad: puntos_bonus
        """
        for habilidad, puntos in bonificaciones.items():
            # Buscar en qué categoría está la habilidad
            if hasattr(self.combate, habilidad):
                valor_actual = getattr(self.combate, habilidad)
                setattr(self.combate, habilidad, valor_actual + puntos)
            elif hasattr(self.educacion, habilidad):
                valor_actual = getattr(self.educacion, habilidad)
                setattr(self.educacion, habilidad, valor_actual + puntos)
            elif hasattr(self.talento, habilidad):
                valor_actual = getattr(self.talento, habilidad)
                setattr(self.talento, habilidad, valor_actual + puntos)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Sistema de Ficha ===\n")
    
    # Crear ficha básica
    ficha = Ficha()
    
    # Distribuir características (20 puntos)
    ficha.caracteristicas.fuerza = 8
    ficha.caracteristicas.reflejos = 4
    ficha.caracteristicas.resistencia = 7
    ficha.caracteristicas.voluntad = 0
    ficha.caracteristicas.punteria = 0
    ficha.caracteristicas.stamina = 1
    
    # Distribuir habilidades (10 puntos cada categoría)
    ficha.combate.armas_cortantes = 10
    ficha.educacion.medicina = 5
    ficha.educacion.elocuencia = 5
    ficha.talento.percepcion = 10
    
    print(ficha.resumen())
    
    print(f"\n¿Ficha válida? {ficha.es_valida()}")
    print(f"Bonus con armas cortantes: +{ficha.obtener_bonus_habilidad('armas_cortantes')}")