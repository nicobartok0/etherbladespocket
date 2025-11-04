"""
Patrón Singleton - Garantiza una única instancia de una clase.
Thread-safe para entornos concurrentes.
"""
import threading
from typing import Any, Dict


class SingletonMeta(type):
    """
    Metaclase que implementa el patrón Singleton de forma thread-safe.
    
    Uso:
        class MiClase(metaclass=SingletonMeta):
            pass
    """
    
    _instances: Dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        """
        Sobrescribe la creación de instancias.
        Si la instancia no existe, la crea. Si existe, la retorna.
        """
        # Verificación rápida sin lock (optimización)
        if cls not in cls._instances:
            # Lock solo cuando necesitamos crear la instancia
            with cls._lock:
                # Double-check: otro thread podría haberla creado
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    @classmethod
    def reset_instances(cls):
        """
        Método útil para testing: resetea todas las instancias singleton.
        ⚠️ NO usar en producción.
        """
        with cls._lock:
            cls._instances.clear()


# Ejemplo de uso y testing
if __name__ == "__main__":
    class ConfiguracionGlobal(metaclass=SingletonMeta):
        def __init__(self):
            self.version = "1.0.0"
            self.debug = True
    
    # Prueba: Ambas variables apuntan a la misma instancia
    config1 = ConfiguracionGlobal()
    config2 = ConfiguracionGlobal()
    
    print(f"¿Son la misma instancia? {config1 is config2}")  # True
    print(f"ID config1: {id(config1)}")
    print(f"ID config2: {id(config2)}")
    
    config1.version = "2.0.0"
    print(f"Version en config2: {config2.version}")  # 2.0.0