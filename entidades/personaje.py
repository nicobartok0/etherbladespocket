"""
Clase Personaje - Entidad central del juego.
Integra todas las entidades: Ficha, Hephix, Inventario, etc.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict
from .ficha import Ficha
from .hephix import Hephix
from .tipos import ClaseTipo, HephixTipo, TipoArma
from .inventario import Inventario
from .arma import Arma, Armadura


class Personaje(BaseModel):
    """
    Representa un personaje jugador completo con todas sus estadísticas,
    equipamiento, progreso e historia.
    """
    
    # ========================================================================
    # Datos personales
    # ========================================================================
    nombre: str
    edad: int = Field(ge=1, le=200)
    raza: str
    nivel: int = Field(default=1, ge=1, le=30)
    experiencia: int = Field(default=0, ge=0)
    
    # ========================================================================
    # Sistema de juego
    # ========================================================================
    clase: ClaseTipo
    hephix: Hephix
    ficha: Ficha
    
    # ========================================================================
    # Estado dinámico (valores actuales en combate/juego)
    # ========================================================================
    pv_actuales: int = Field(default=0)
    pm_actuales: int = Field(default=0)
    pcf_actuales: int = Field(default=0)
    pct_actuales: int = Field(default=0)
    ps_actuales: int = Field(default=0)  # Puntos de Stamina en combate
    
    # ========================================================================
    # Equipamiento
    # ========================================================================
    inventario: Inventario = Field(default_factory=Inventario)
    arma_equipada: Optional[Arma] = None
    armadura_equipada: Optional[Armadura] = None
    
    # ========================================================================
    # Historia y progreso
    # ========================================================================
    historia: str = Field(default="", description="Trasfondo del personaje")
    objetivo: str = Field(default="", description="Objetivo del personaje")
    
    # Sistema de adicciones (drogas)
    adicciones: Dict[str, int] = Field(default_factory=dict, description="Droga: puntos de adicción")
    
    # Estado vital
    esta_vivo: bool = Field(default=True)
    esta_inconsciente: bool = Field(default=False)
    
    def model_post_init(self, __context):
        """Inicializa valores después de crear el modelo"""
        # Sincronizar hephix_tipo en ficha
        self.ficha.hephix_tipo = self.hephix.tipo
        
        # Inicializar stats actuales si están en 0
        if self.pv_actuales == 0:
            self.restaurar_stats_completos()
    
    # ========================================================================
    # Propiedades calculadas (delegadas a ficha)
    # ========================================================================
    
    @property
    def pv_maximos(self) -> int:
        return self.ficha.pv_maximos
    
    @property
    def pm_maximos(self) -> int:
        return self.ficha.pm_maximos
    
    @property
    def pcf_maximos(self) -> int:
        return self.ficha.pcf_maximos
    
    @property
    def pct_maximos(self) -> int:
        return self.ficha.pct_maximos
    
    @property
    def ps_maximos(self) -> int:
        return self.ficha.ps_maximos
    
    # ========================================================================
    # Gestión de vida y recursos
    # ========================================================================
    
    def restaurar_stats_completos(self):
        """Restaura todos los stats a sus valores máximos"""
        self.pv_actuales = self.pv_maximos
        self.pm_actuales = self.pm_maximos
        self.pcf_actuales = self.pcf_maximos
        self.pct_actuales = self.pct_maximos
        self.ps_actuales = self.ps_maximos
    
    def recibir_daño(self, cantidad: int) -> int:
        """
        Aplica daño al personaje.
        
        Args:
            cantidad: Cantidad de daño a recibir
        
        Returns:
            Daño efectivamente recibido (después de armadura)
        """
        # Reducción por armadura
        reduccion = 0
        if self.armadura_equipada:
            reduccion = self.armadura_equipada.reduccion_total()
        
        daño_final = max(0, cantidad - reduccion)
        self.pv_actuales = max(0, self.pv_actuales - daño_final)
        
        # Verificar muerte
        if self.pv_actuales == 0:
            self.esta_vivo = False
            self.esta_inconsciente = True
        
        return daño_final
    
    def curar(self, cantidad: int) -> int:
        """
        Cura al personaje.
        
        Args:
            cantidad: Cantidad de PV a restaurar
        
        Returns:
            PV efectivamente curados
        """
        pv_antes = self.pv_actuales
        self.pv_actuales = min(self.pv_maximos, self.pv_actuales + cantidad)
        return self.pv_actuales - pv_antes
    
    def gastar_pm(self, cantidad: int) -> bool:
        """
        Gasta puntos de magia.
        
        Returns:
            True si tenía suficiente, False si no
        """
        if self.pm_actuales >= cantidad:
            self.pm_actuales -= cantidad
            return True
        return False
    
    def gastar_stamina(self, cantidad: int):
        """Reduce stamina en combate"""
        self.ps_actuales = max(0, self.ps_actuales - cantidad)
    
    def esta_sin_stamina(self) -> bool:
        """Verifica si quedó sin stamina (vulnerable a golpe de gracia)"""
        return self.ps_actuales <= 0
    
    def restaurar_stamina_completa(self):
        """Restaura stamina al máximo (entre combates)"""
        self.ps_actuales = self.ps_maximos
    
    # ========================================================================
    # Sistema de equipamiento
    # ========================================================================
    
    def equipar_arma(self, arma: Arma) -> bool:
        """
        Equipa un arma si cumple requisitos.
        
        Returns:
            True si se equipó, False si no cumple requisitos
        """
        # Verificar nivel
        if self.nivel < arma.nivel_requerido:
            return False
        
        # Verificar habilidad mínima
        habilidad_nombre = arma.tipo_arma.value
        nivel_habilidad = getattr(self.ficha.combate, habilidad_nombre, 0)
        if nivel_habilidad < arma.habilidad_minima:
            return False
        
        # Si ya tiene arma equipada, devolverla al inventario
        if self.arma_equipada:
            self.inventario.agregar_arma(self.arma_equipada)
        
        self.arma_equipada = arma
        return True
    
    def desequipar_arma(self) -> bool:
        """
        Desequipa el arma actual y la devuelve al inventario.
        
        Returns:
            True si se desequipó, False si no había arma
        """
        if not self.arma_equipada:
            return False
        
        if self.inventario.agregar_arma(self.arma_equipada):
            self.arma_equipada = None
            return True
        return False
    
    def equipar_armadura(self, armadura: Armadura) -> bool:
        """Equipa una armadura si cumple requisitos"""
        if self.nivel < armadura.nivel_requerido:
            return False
        
        if self.ficha.resistencia < armadura.resistencia_minima:
            return False
        
        if self.armadura_equipada:
            self.inventario.agregar_armadura(self.armadura_equipada)
        
        self.armadura_equipada = armadura
        return True
    
    def desequipar_armadura(self) -> bool:
        """Desequipa la armadura actual"""
        if not self.armadura_equipada:
            return False
        
        if self.inventario.agregar_armadura(self.armadura_equipada):
            self.armadura_equipada = None
            return True
        return False
    
    # ========================================================================
    # Sistema de habilidades y bonificaciones
    # ========================================================================
    
    def obtener_bonus_habilidad_arma(self, arma: Optional[Arma]) -> int:
        """
        Obtiene el bonus de daño por nivel de habilidad con el arma.
        
        Returns:
            Bonus de daño (+1 cada 5 puntos de habilidad)
        """
        if not arma:
            # Pugilismo para combate sin armas
            return self.ficha.obtener_bonus_habilidad("pugilismo")
        
        return self.ficha.obtener_bonus_habilidad(arma.tipo_arma.value)
    
    def obtener_modificador_reflejos(self) -> int:
        """Obtiene el modificador total de reflejos (base + armadura)"""
        base = self.ficha.reflejos
        bonus_armadura = 0
        if self.armadura_equipada:
            bonus_armadura = self.armadura_equipada.bonus_reflejos
        
        return base + bonus_armadura
    
    # ========================================================================
    # Sistema de nivel y experiencia
    # ========================================================================
    
    def ganar_experiencia(self, cantidad: int):
        """
        Otorga experiencia y verifica si sube de nivel.
        
        Args:
            cantidad: Cantidad de XP a otorgar
        """
        self.experiencia += cantidad
        
        # Sistema simple: cada 1000 XP = 1 nivel
        xp_necesaria = self.nivel * 1000
        
        while self.experiencia >= xp_necesaria and self.nivel < 30:
            self.subir_nivel()
            xp_necesaria = self.nivel * 1000
    
    def subir_nivel(self):
        """Sube el nivel del personaje"""
        if self.nivel >= 30:
            return
        
        self.nivel += 1
        self.hephix.subir_nivel()
        
        # Restaurar stats al subir de nivel
        self.restaurar_stats_completos()
    
    # ========================================================================
    # Sistema de adicciones
    # ========================================================================
    
    def consumir_droga(self, nombre_droga: str, puntos_adiccion: int):
        """Registra consumo de droga y aumenta adicción"""
        if nombre_droga not in self.adicciones:
            self.adicciones[nombre_droga] = 0
        
        self.adicciones[nombre_droga] += puntos_adiccion
    
    def obtener_nivel_adiccion(self, nombre_droga: str) -> int:
        """
        Obtiene el nivel de adicción a una droga.
        Cada 20 puntos = 1 nivel
        """
        puntos = self.adicciones.get(nombre_droga, 0)
        return puntos // 20
    
    # ========================================================================
    # Métodos de utilidad
    # ========================================================================
    
    def esta_en_condiciones_combate(self) -> bool:
        """Verifica si puede combatir"""
        return self.esta_vivo and not self.esta_inconsciente and self.pv_actuales > 0
    
    def resumen_completo(self) -> str:
        """Genera un resumen completo del personaje"""
        lineas = [
            "=" * 60,
            f"PERSONAJE: {self.nombre}",
            f"Raza: {self.raza} | Edad: {self.edad} | Nivel: {self.nivel}",
            f"Clase: {self.clase.value.title()}",
            f"Hephix: {self.hephix.tipo.value.title()} (Nivel {self.hephix.nivel})",
            f"Experiencia: {self.experiencia} XP",
            "",
            "ESTADO ACTUAL",
            f"  PV: {self.pv_actuales}/{self.pv_maximos}",
            f"  PM: {self.pm_actuales}/{self.pm_maximos}",
            f"  PCF: {self.pcf_actuales}/{self.pcf_maximos}",
            f"  PCT: {self.pct_actuales}/{self.pct_maximos}",
            f"  PS: {self.ps_actuales}/{self.ps_maximos}",
            "",
            "EQUIPAMIENTO",
            f"  Arma: {self.arma_equipada if self.arma_equipada else 'Sin equipar'}",
            f"  Armadura: {self.armadura_equipada if self.armadura_equipada else 'Sin equipar'}",
            "",
        ]
        
        # Agregar resumen de ficha
        lineas.append(self.ficha.resumen())
        
        return "\n".join(lineas)
    
    def to_dict_guardado(self) -> dict:
        """Serializa el personaje para guardado (compatible con JSON)"""
        return self.model_dump(mode='json')
    
    @classmethod
    def from_dict_guardado(cls, data: dict) -> "Personaje":
        """Deserializa el personaje desde un guardado"""
        return cls.model_validate(data)


if __name__ == "__main__":
    from .arma import crear_espada_basica
    
    print("=== Sistema de Personaje ===\n")
    
    # Crear personaje de ejemplo
    ficha = Ficha()
    ficha.caracteristicas.fuerza = 8
    ficha.caracteristicas.reflejos = 4
    ficha.caracteristicas.resistencia = 7
    ficha.caracteristicas.voluntad = 0
    ficha.caracteristicas.punteria = 0
    ficha.caracteristicas.stamina = 1
    
    ficha.combate.armas_cortantes = 10
    ficha.educacion.medicina = 5
    ficha.talento.percepcion = 5
    
    hephix = Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL)
    
    personaje = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=hephix,
        ficha=ficha,
        historia="Un guerrero de las montañas del norte"
    )
    
    # Equipar arma
    espada = crear_espada_basica()
    personaje.inventario.agregar_arma(espada)
    personaje.equipar_arma(espada)
    
    print(personaje.resumen_completo())
    
    # Simular combate
    print("\n=== Simulación de Combate ===")
    print(f"Recibiendo 25 de daño...")
    daño = personaje.recibir_daño(25)
    print(f"  Daño recibido: {daño}")
    print(f"  PV restantes: {personaje.pv_actuales}/{personaje.pv_maximos}")