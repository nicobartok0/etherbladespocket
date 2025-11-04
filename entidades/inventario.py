"""
Sistema de inventario para gestionar ítems, armas y objetos.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from .arma import Arma, Armadura
from .tipos import RarezaItem


class Item(BaseModel):
    """
    Representa un ítem genérico del inventario.
    """
    
    nombre: str
    descripcion: str = ""
    cantidad: int = Field(default=1, ge=1)
    es_apilable: bool = Field(default=True)
    valor: int = Field(default=0, ge=0, description="Valor en monedas")
    peso: float = Field(default=0.0, ge=0.0)
    rareza: RarezaItem = Field(default=RarezaItem.COMUN)
    
    def __str__(self) -> str:
        cantidad_str = f" x{self.cantidad}" if self.cantidad > 1 else ""
        return f"{self.nombre}{cantidad_str}"


class ItemConsumible(Item):
    """
    Ítem que se puede usar y se consume.
    Ejemplo: Pociones, vendajes, comida.
    """
    
    efecto: str = Field(default="", description="Descripción del efecto")
    valor_efecto: int = Field(default=0, description="Magnitud del efecto")
    
    # Para botiquines médicos
    es_botiquin: bool = Field(default=False)
    tipo_botiquin: Optional[str] = None  # "primeros_auxilios" o "atencion_medica"
    turnos_uso: int = Field(default=0)


class ItemDroga(Item):
    """
    Ítem especial que genera adicción.
    """
    
    bonificacion_temporal: int = Field(default=0)
    duracion_turnos: int = Field(default=0)
    puntos_adiccion: int = Field(default=5, description="Puntos de adicción que genera")
    
    es_apilable: bool = Field(default=True)


class Inventario(BaseModel):
    """
    Sistema de inventario con gestión de ítems, armas y equipamiento.
    """
    
    # Capacidad
    capacidad_maxima: int = Field(default=20, description="Slots de inventario")
    peso_maximo: Optional[float] = None
    
    # Almacenamiento
    items: List[Item] = Field(default_factory=list)
    armas: List[Arma] = Field(default_factory=list)
    armaduras: List[Armadura] = Field(default_factory=list)
    
    # Moneda
    monedas: int = Field(default=0, ge=0)
    
    def cantidad_items_totales(self) -> int:
        """Calcula el total de slots ocupados (incluyendo armas y armaduras)"""
        return len(self.items) + len(self.armas) + len(self.armaduras)
    
    def peso_total(self) -> float:
        """Calcula el peso total del inventario"""
        peso = sum(item.peso * item.cantidad for item in self.items)
        # Las armas y armaduras podrían tener peso (no implementado aún)
        return peso
    
    def tiene_espacio(self, slots_necesarios: int = 1) -> bool:
        """Verifica si hay espacio disponible"""
        return self.cantidad_items_totales() + slots_necesarios <= self.capacidad_maxima
    
    def agregar_item(self, item: Item) -> bool:
        """
        Agrega un ítem al inventario.
        Si es apilable y ya existe, incrementa la cantidad.
        
        Returns:
            True si se agregó exitosamente, False si no hay espacio
        """
        if item.es_apilable:
            # Buscar si ya existe
            for item_existente in self.items:
                if item_existente.nombre == item.nombre:
                    item_existente.cantidad += item.cantidad
                    return True
        
        # Verificar espacio
        if not self.tiene_espacio():
            return False
        
        self.items.append(item)
        return True
    
    def agregar_arma(self, arma: Arma) -> bool:
        """Agrega un arma al inventario"""
        if not self.tiene_espacio():
            return False
        
        self.armas.append(arma)
        return True
    
    def agregar_armadura(self, armadura: Armadura) -> bool:
        """Agrega una armadura al inventario"""
        if not self.tiene_espacio():
            return False
        
        self.armaduras.append(armadura)
        return True
    
    def remover_item(self, nombre: str, cantidad: int = 1) -> bool:
        """
        Remueve un ítem del inventario.
        
        Returns:
            True si se removió, False si no se encontró o no hay suficiente cantidad
        """
        for i, item in enumerate(self.items):
            if item.nombre == nombre:
                if item.cantidad >= cantidad:
                    item.cantidad -= cantidad
                    if item.cantidad == 0:
                        self.items.pop(i)
                    return True
                else:
                    return False
        return False
    
    def remover_arma(self, nombre: str) -> Optional[Arma]:
        """
        Remueve un arma del inventario.
        
        Returns:
            El arma removida o None si no se encontró
        """
        for i, arma in enumerate(self.armas):
            if arma.nombre == nombre:
                return self.armas.pop(i)
        return None
    
    def remover_armadura(self, nombre: str) -> Optional[Armadura]:
        """
        Remueve una armadura del inventario.
        
        Returns:
            La armadura removida o None si no se encontró
        """
        for i, armadura in enumerate(self.armaduras):
            if armadura.nombre == nombre:
                return self.armaduras.pop(i)
        return None
    
    def buscar_item(self, nombre: str) -> Optional[Item]:
        """Busca un ítem por nombre"""
        for item in self.items:
            if item.nombre.lower() == nombre.lower():
                return item
        return None
    
    def buscar_arma(self, nombre: str) -> Optional[Arma]:
        """Busca un arma por nombre"""
        for arma in self.armas:
            if arma.nombre.lower() == nombre.lower():
                return arma
        return None
    
    def buscar_armadura(self, nombre: str) -> Optional[Armadura]:
        """Busca una armadura por nombre"""
        for armadura in self.armaduras:
            if armadura.nombre.lower() == nombre.lower():
                return armadura
        return None
    
    def listar_consumibles(self) -> List[ItemConsumible]:
        """Lista todos los ítems consumibles"""
        return [item for item in self.items if isinstance(item, ItemConsumible)]
    
    def listar_botiquines(self) -> List[ItemConsumible]:
        """Lista todos los botiquines médicos"""
        return [item for item in self.items 
                if isinstance(item, ItemConsumible) and item.es_botiquin]
    
    def agregar_monedas(self, cantidad: int):
        """Agrega monedas al inventario"""
        self.monedas += cantidad
    
    def gastar_monedas(self, cantidad: int) -> bool:
        """
        Gasta monedas si hay suficientes.
        
        Returns:
            True si se gastaron, False si no hay suficientes
        """
        if self.monedas >= cantidad:
            self.monedas -= cantidad
            return True
        return False
    
    def resumen(self) -> str:
        """Genera un resumen del inventario"""
        lineas = [
            "=" * 50,
            f"INVENTARIO ({self.cantidad_items_totales()}/{self.capacidad_maxima} slots)",
            f"Monedas: {self.monedas}",
            ""
        ]
        
        if self.items:
            lineas.append("ÍTEMS:")
            for item in self.items:
                lineas.append(f"  • {item}")
        
        if self.armas:
            lineas.append("\nARMAS:")
            for arma in self.armas:
                lineas.append(f"  • {arma}")
        
        if self.armaduras:
            lineas.append("\nARMADURAS:")
            for armadura in self.armaduras:
                lineas.append(f"  • {armadura}")
        
        lineas.append("=" * 50)
        return "\n".join(lineas)


# Factory functions para crear ítems comunes
def crear_pocion_vida_menor() -> ItemConsumible:
    """Crea una poción de vida menor"""
    return ItemConsumible(
        nombre="Poción de Vida Menor",
        descripcion="Restaura 20 PV",
        cantidad=1,
        valor=50,
        peso=0.2,
        efecto="restaurar_pv",
        valor_efecto=20
    )


def crear_botiquin_primeros_auxilios() -> ItemConsumible:
    """Crea un botiquín de primeros auxilios"""
    return ItemConsumible(
        nombre="Botiquín de Primeros Auxilios",
        descripcion="Kit básico para curar heridas",
        cantidad=1,
        valor=30,
        peso=0.5,
        efecto="sanacion",
        valor_efecto=10,
        es_botiquin=True,
        tipo_botiquin="primeros_auxilios",
        turnos_uso=1
    )


def crear_kit_atencion_medica() -> ItemConsumible:
    """Crea un kit de atención médica"""
    return ItemConsumible(
        nombre="Kit de Atención Médica",
        descripcion="Kit completo para tratamiento médico",
        cantidad=1,
        valor=100,
        peso=1.5,
        efecto="sanacion",
        valor_efecto=30,
        es_botiquin=True,
        tipo_botiquin="atencion_medica",
        turnos_uso=2
    )


if __name__ == "__main__":
    from .arma import crear_espada_basica, crear_armadura_ligera
    
    print("=== Sistema de Inventario ===\n")
    
    # Crear inventario
    inv = Inventario(capacidad_maxima=10)
    
    # Agregar ítems
    inv.agregar_item(crear_pocion_vida_menor())
    inv.agregar_item(crear_botiquin_primeros_auxilios())
    inv.agregar_arma(crear_espada_basica())
    inv.agregar_armadura(crear_armadura_ligera())
    inv.agregar_monedas(150)
    
    print(inv.resumen())
    
    # Probar búsqueda
    print("\nBuscando 'Espada Corta':")
    arma = inv.buscar_arma("Espada Corta")
    if arma:
        print(f"  ✅ Encontrada: {arma}")