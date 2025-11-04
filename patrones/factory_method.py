"""
Patrón Factory Method - Creación de objetos sin acoplar al código cliente.
Permite crear diferentes tipos de entidades desde definiciones JSON.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar, Generic
import json
from pathlib import Path


T = TypeVar('T')


class Factory(ABC, Generic[T]):
    """
    Clase base abstracta para todas las fábricas.
    Define la interfaz común para crear objetos.
    """
    
    @abstractmethod
    def crear(self, tipo: str, **kwargs) -> T:
        """
        Método factory: crea un objeto del tipo especificado.
        
        Args:
            tipo: Identificador del tipo de objeto a crear
            **kwargs: Parámetros específicos del objeto
            
        Returns:
            Instancia del objeto creado
            
        Raises:
            ValueError: Si el tipo no es reconocido
        """
        pass
    
    @abstractmethod
    def obtener_tipos_disponibles(self) -> list[str]:
        """Retorna lista de tipos que esta fábrica puede crear"""
        pass


class FactoryConRegistro(Factory[T]):
    """
    Fábrica con registro dinámico de tipos.
    Permite registrar nuevas clases en tiempo de ejecución.
    """
    
    def __init__(self):
        self._registro: Dict[str, Type[T]] = {}
    
    def registrar(self, tipo: str, clase: Type[T]):
        """
        Registra un nuevo tipo de objeto que la fábrica puede crear.
        
        Args:
            tipo: Identificador único del tipo
            clase: Clase que se instanciará para este tipo
        """
        self._registro[tipo] = clase
    
    def crear(self, tipo: str, **kwargs) -> T:
        """Crea una instancia del tipo registrado"""
        if tipo not in self._registro:
            tipos_validos = ', '.join(self._registro.keys())
            raise ValueError(
                f"Tipo '{tipo}' no reconocido. "
                f"Tipos válidos: {tipos_validos}"
            )
        
        clase = self._registro[tipo]
        return clase(**kwargs)
    
    def obtener_tipos_disponibles(self) -> list[str]:
        """Retorna todos los tipos registrados"""
        return list(self._registro.keys())


class FactoryDesdeJSON(Factory[T]):
    """
    Fábrica que carga definiciones desde archivos JSON.
    Útil para cargar configuraciones de armas, habilidades, etc.
    """
    
    def __init__(self, ruta_json: str, factory_base: FactoryConRegistro[T]):
        """
        Args:
            ruta_json: Ruta al archivo JSON con definiciones
            factory_base: Fábrica con las clases registradas
        """
        self.ruta_json = Path(ruta_json)
        self.factory_base = factory_base
        self._definiciones: Dict[str, Dict[str, Any]] = {}
        self._cargar_definiciones()
    
    def _cargar_definiciones(self):
        """Carga las definiciones desde el archivo JSON"""
        if not self.ruta_json.exists():
            raise FileNotFoundError(
                f"No se encontró el archivo: {self.ruta_json}"
            )
        
        with open(self.ruta_json, 'r', encoding='utf-8') as f:
            self._definiciones = json.load(f)
    
    def crear(self, tipo: str, **kwargs_extra) -> T:
        """
        Crea un objeto combinando definición JSON con parámetros extra.
        
        Args:
            tipo: ID del objeto en el JSON
            **kwargs_extra: Parámetros adicionales que sobrescriben el JSON
        """
        if tipo not in self._definiciones:
            tipos_validos = ', '.join(self._definiciones.keys())
            raise ValueError(
                f"Tipo '{tipo}' no encontrado en {self.ruta_json}. "
                f"Tipos válidos: {tipos_validos}"
            )
        
        # Combinar definición JSON con parámetros extra
        definicion = self._definiciones[tipo].copy()
        definicion.update(kwargs_extra)
        
        # Delegar creación a la factory base
        tipo_clase = definicion.pop('tipo_clase', tipo)
        return self.factory_base.crear(tipo_clase, **definicion)
    
    def obtener_tipos_disponibles(self) -> list[str]:
        """Retorna todos los IDs definidos en el JSON"""
        return list(self._definiciones.keys())
    
    def obtener_definicion(self, tipo: str) -> Dict[str, Any]:
        """Obtiene la definición completa de un tipo sin instanciar"""
        if tipo not in self._definiciones:
            raise ValueError(f"Tipo '{tipo}' no encontrado")
        return self._definiciones[tipo].copy()
    
    def recargar(self):
        """Recarga las definiciones desde el archivo JSON"""
        self._cargar_definiciones()


# Ejemplo de uso
if __name__ == "__main__":
    # Ejemplo: Factory de armas
    
    class Arma:
        def __init__(self, nombre: str, daño: int):
            self.nombre = nombre
            self.daño = daño
        
        def __repr__(self):
            return f"{self.nombre} (daño: {self.daño})"
    
    class Espada(Arma):
        def __init__(self, nombre: str, daño: int, filo: str = "simple"):
            super().__init__(nombre, daño)
            self.filo = filo
    
    class Hacha(Arma):
        def __init__(self, nombre: str, daño: int, peso: str = "medio"):
            super().__init__(nombre, daño)
            self.peso = peso
    
    # Crear factory con registro
    factory_armas = FactoryConRegistro[Arma]()
    factory_armas.registrar("espada", Espada)
    factory_armas.registrar("hacha", Hacha)
    
    # Crear armas directamente
    espada1 = factory_armas.crear("espada", nombre="Excalibur", daño=50, filo="doble")
    print(f"Creada: {espada1}")
    
    # Tipos disponibles
    print(f"Tipos disponibles: {factory_armas.obtener_tipos_disponibles()}")