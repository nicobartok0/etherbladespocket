"""
Estructuras de datos para el sistema de combate.
Define los resultados y estados del combate.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class TipoResultadoAtaque(str, Enum):
    """Tipos de resultado de ataque"""
    EXITO = "exito"
    BLOQUEADO = "bloqueado"
    CRITICO = "critico"  # Golpe de gracia
    CONTRAATAQUE = "contraataque"
    SIGILO_EXITOSO = "sigilo_exitoso"
    FALLO = "fallo"


class ResultadoAtaque(BaseModel):
    """
    Resultado detallado de un ataque.
    Contiene toda la información del intercambio.
    """
    tipo: TipoResultadoAtaque
    
    # Participantes
    atacante_nombre: str
    defensor_nombre: str
    
    # Coeficientes
    coeficiente_ataque: int = 0
    coeficiente_defensa: int = 0
    diferencia: int = 0
    
    # Daños y efectos
    daño_infligido: int = 0
    stamina_perdida: int = 0
    
    # Estado resultante
    defensor_pv_restantes: int = 0
    defensor_stamina_restante: int = 0
    defensor_muerto: bool = False
    defensor_sin_stamina: bool = False
    
    # Información adicional
    fue_golpe_gracia: bool = False
    fue_contraataque: bool = False
    arma_usada: Optional[str] = None
    
    # Dados (para logging/debugging)
    dados_ataque: List[int] = Field(default_factory=list)
    dados_defensa: List[int] = Field(default_factory=list)
    
    def descripcion_corta(self) -> str:
        """Genera una descripción corta del resultado"""
        if self.tipo == TipoResultadoAtaque.CRITICO:
            return f"💥 ¡GOLPE DE GRACIA! {self.atacante_nombre} inflige {self.daño_infligido} de daño"
        elif self.tipo == TipoResultadoAtaque.CONTRAATAQUE:
            return f"🔄 ¡CONTRAATAQUE! {self.defensor_nombre} contraataca"
        elif self.tipo == TipoResultadoAtaque.BLOQUEADO:
            return f"🛡️ {self.defensor_nombre} bloquea el ataque"
        elif self.tipo == TipoResultadoAtaque.EXITO:
            return f"⚔️ {self.atacante_nombre} reduce stamina de {self.defensor_nombre} en {self.stamina_perdida}"
        elif self.tipo == TipoResultadoAtaque.SIGILO_EXITOSO:
            return f"🗡️ ¡ATAQUE FURTIVO! {self.atacante_nombre} inflige {self.daño_infligido} de daño"
        else:
            return f"❌ Ataque fallido"


class EstadoCombatiente(BaseModel):
    """Estado actual de un combatiente en el combate"""
    nombre: str
    pv_actuales: int
    pv_maximos: int
    ps_actuales: int
    ps_maximos: int
    esta_vivo: bool
    esta_inconsciente: bool
    iniciativa: int = 0
    
    def porcentaje_vida(self) -> float:
        """Retorna el porcentaje de vida actual"""
        if self.pv_maximos == 0:
            return 0.0
        return (self.pv_actuales / self.pv_maximos) * 100
    
    def porcentaje_stamina(self) -> float:
        """Retorna el porcentaje de stamina actual"""
        if self.ps_maximos == 0:
            return 0.0
        return (self.ps_actuales / self.ps_maximos) * 100


class EstadoCombate(BaseModel):
    """
    Estado completo de un combate en curso.
    Mantiene el registro de todo lo que ocurre.
    """
    turno_actual: int = 0
    combatientes: List[EstadoCombatiente] = Field(default_factory=list)
    orden_turnos: List[str] = Field(default_factory=list)  # Nombres en orden de iniciativa
    indice_turno_actual: int = 0
    combate_activo: bool = True
    ganador: Optional[str] = None
    
    # Historial
    historial_ataques: List[ResultadoAtaque] = Field(default_factory=list)
    
    def obtener_combatiente_actual(self) -> Optional[EstadoCombatiente]:
        """Obtiene el combatiente del turno actual"""
        if not self.orden_turnos:
            return None
        
        nombre = self.orden_turnos[self.indice_turno_actual]
        for combatiente in self.combatientes:
            if combatiente.nombre == nombre:
                return combatiente
        return None
    
    def avanzar_turno(self):
        """Avanza al siguiente turno"""
        self.indice_turno_actual = (self.indice_turno_actual + 1) % len(self.orden_turnos)
        if self.indice_turno_actual == 0:
            self.turno_actual += 1
    
    def agregar_resultado_ataque(self, resultado: ResultadoAtaque):
        """Agrega un resultado al historial"""
        self.historial_ataques.append(resultado)
    
    def obtener_combatiente_por_nombre(self, nombre: str) -> Optional[EstadoCombatiente]:
        """Busca un combatiente por nombre"""
        for combatiente in self.combatientes:
            if combatiente.nombre == nombre:
                return combatiente
        return None
    
    def verificar_fin_combate(self) -> bool:
        """
        Verifica si el combate ha terminado.
        Actualiza el estado y determina el ganador.
        """
        vivos = [c for c in self.combatientes if c.esta_vivo]
        
        if len(vivos) <= 1:
            self.combate_activo = False
            if vivos:
                self.ganador = vivos[0].nombre
            return True
        
        return False
    
    def resumen(self) -> str:
        """Genera un resumen del estado del combate"""
        lineas = [
            f"=== COMBATE - Turno {self.turno_actual} ===",
            f"Turno de: {self.orden_turnos[self.indice_turno_actual] if self.orden_turnos else 'N/A'}",
            "",
            "Combatientes:"
        ]
        
        for c in self.combatientes:
            estado = "💀 MUERTO" if not c.esta_vivo else f"❤️ {c.pv_actuales}/{c.pv_maximos} PV"
            stamina = f"⚡ {c.ps_actuales}/{c.ps_maximos} PS"
            lineas.append(f"  {c.nombre}: {estado} | {stamina}")
        
        return "\n".join(lineas)


if __name__ == "__main__":
    # Ejemplo de uso
    print("=== Sistema de Estructuras de Combate ===\n")
    
    # Crear resultado de ataque
    resultado = ResultadoAtaque(
        tipo=TipoResultadoAtaque.EXITO,
        atacante_nombre="Aldric",
        defensor_nombre="Goblin",
        coeficiente_ataque=18,
        coeficiente_defensa=10,
        diferencia=8,
        stamina_perdida=8,
        defensor_pv_restantes=25,
        defensor_stamina_restante=2,
        dados_ataque=[5, 6, 4],
        dados_defensa=[4, 6]
    )
    
    print(resultado.descripcion_corta())
    print()
    
    # Crear estado de combate
    estado = EstadoCombate(turno_actual=1)
    estado.combatientes.append(
        EstadoCombatiente(
            nombre="Aldric",
            pv_actuales=70,
            pv_maximos=70,
            ps_actuales=30,
            ps_maximos=30,
            esta_vivo=True,
            esta_inconsciente=False,
            iniciativa=15
        )
    )
    estado.orden_turnos = ["Aldric"]
    
    print(estado.resumen())