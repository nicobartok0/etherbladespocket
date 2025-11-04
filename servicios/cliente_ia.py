"""
Cliente de IA - Wrapper para la API de OpenAI.
Implementa el patrón Singleton para una única instancia.
"""
from typing import Optional, List, Dict, Any
from patrones import SingletonMeta
import time
import os

# Intentar importar settings, con fallback
try:
    from config import settings
except ModuleNotFoundError:
    # Fallback para cuando se ejecuta desde tests u otros directorios
    import sys
    from pathlib import Path
    # Agregar la raíz del proyecto al path
    root_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(root_dir))
    from config import settings


class ClienteIA(metaclass=SingletonMeta):
    """
    Cliente singleton para la API de OpenAI.
    Maneja la comunicación con el modelo de lenguaje.
    """
    
    def __init__(self):
        """Inicializa el cliente de OpenAI"""
        self.api_key = settings.openai_api_key
        self.modelo = settings.openai_model
        self.max_tokens = settings.narrador_max_tokens
        self.temperature = settings.narrador_temperature
        
        # Cliente de OpenAI (solo si hay API key)
        self._cliente = None
        if self.api_key:
            try:
                from openai import OpenAI
                self._cliente = OpenAI(api_key=self.api_key)
            except ImportError:
                print("⚠️ Librería 'openai' no instalada. Instalar con: pip install openai")
        
        # Cache de respuestas (opcional)
        self._cache: Dict[str, str] = {}
        self._cache_habilitado = False
    
    def esta_disponible(self) -> bool:
        """Verifica si el cliente está disponible"""
        return self._cliente is not None
    
    def generar_texto(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_message: Optional[str] = None
    ) -> str:
        """
        Genera texto usando el modelo de lenguaje.
        
        Args:
            prompt: Prompt del usuario
            max_tokens: Máximo de tokens a generar (None = usar default)
            temperature: Temperatura del modelo (None = usar default)
            system_message: Mensaje de sistema opcional
        
        Returns:
            Texto generado por la IA
        
        Raises:
            RuntimeError: Si no hay API key configurada
            Exception: Si hay error en la llamada a la API
        """
        if not self.esta_disponible():
            raise RuntimeError(
                "Cliente de IA no disponible. "
                "Configura OPENAI_API_KEY en el archivo .env"
            )
        
        # Verificar cache
        cache_key = f"{prompt}:{system_message}"
        if self._cache_habilitado and cache_key in self._cache:
            return self._cache[cache_key]
        
        # Preparar mensajes
        mensajes = []
        if system_message:
            mensajes.append({"role": "system", "content": system_message})
        mensajes.append({"role": "user", "content": prompt})
        
        # Llamar a la API
        try:
            respuesta = self._cliente.chat.completions.create(
                model=self.modelo,
                messages=mensajes,
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature
            )
            
            texto_generado = respuesta.choices[0].message.content.strip()
            
            # Guardar en cache
            if self._cache_habilitado:
                self._cache[cache_key] = texto_generado
            
            return texto_generado
            
        except Exception as e:
            raise Exception(f"Error al generar texto: {e}")
    
    def generar_con_reintentos(
        self,
        prompt: str,
        max_reintentos: int = 3,
        **kwargs
    ) -> str:
        """
        Genera texto con reintentos automáticos en caso de error.
        
        Args:
            prompt: Prompt del usuario
            max_reintentos: Número máximo de reintentos
            **kwargs: Argumentos adicionales para generar_texto
        
        Returns:
            Texto generado
        """
        for intento in range(max_reintentos):
            try:
                return self.generar_texto(prompt, **kwargs)
            except Exception as e:
                if intento == max_reintentos - 1:
                    raise
                
                # Esperar antes de reintentar (backoff exponencial)
                tiempo_espera = 2 ** intento
                print(f"⚠️ Error en intento {intento + 1}/{max_reintentos}. "
                      f"Reintentando en {tiempo_espera}s...")
                time.sleep(tiempo_espera)
        
        raise RuntimeError("No se pudo generar texto después de varios intentos")
    
    def habilitar_cache(self, habilitar: bool = True):
        """Habilita o deshabilita el cache de respuestas"""
        self._cache_habilitado = habilitar
        if not habilitar:
            self._cache.clear()
    
    def limpiar_cache(self):
        """Limpia el cache de respuestas"""
        self._cache.clear()


class ClienteIAMock(ClienteIA):
    """
    Cliente mock para testing y desarrollo sin API key.
    Retorna respuestas predefinidas.
    """
    
    def __init__(self):
        """Inicializa el mock sin necesidad de API key"""
        self.api_key = "mock_key"
        self.modelo = "mock_model"
        self.max_tokens = 500
        self.temperature = 0.7
        self._cliente = "mock"  # Para que esta_disponible() retorne True
        self._cache = {}
        self._cache_habilitado = False
    
    def generar_texto(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_message: Optional[str] = None
    ) -> str:
        """
        Genera una respuesta mock basada en palabras clave del prompt.
        """
        prompt_lower = prompt.lower()
        
        # Respuestas basadas en palabras clave
        if "combate" in prompt_lower or "ataque" in prompt_lower:
            return (
                "El combate es feroz. Tu arma brilla bajo la luz mientras "
                "enfrentas al enemigo con valentía. Cada movimiento cuenta "
                "en esta batalla que pondrá a prueba tus habilidades."
            )
        
        elif "explorar" in prompt_lower or "descubrir" in prompt_lower:
            return (
                "Te adentras en lo desconocido. Las sombras danzan en las paredes "
                "mientras exploras cuidadosamente cada rincón. Algo importante "
                "aguarda ser descubierto en este lugar misterioso."
            )
        
        elif "diálogo" in prompt_lower or "hablar" in prompt_lower:
            return (
                "La conversación fluye naturalmente. Las palabras intercambiadas "
                "revelan información crucial para tu aventura. Este encuentro "
                "podría cambiar el rumbo de tu destino."
            )
        
        elif "descansar" in prompt_lower or "taberna" in prompt_lower:
            return (
                "Encuentras un momento de respiro. El cálido ambiente te reconforta "
                "mientras planeas tus próximos pasos. La aventura puede esperar "
                "mientras recuperas fuerzas."
            )
        
        else:
            # Respuesta genérica
            return (
                "Tu aventura continúa en el mundo de Ether Blades. "
                "Cada decisión que tomas moldea tu destino. ¿Qué harás ahora?"
            )


if __name__ == "__main__":
    print("=== Demo del Cliente de IA ===\n")
    
    # Intentar usar cliente real
    cliente = ClienteIA()
    
    if cliente.esta_disponible():
        print("✅ Cliente de OpenAI disponible")
        print(f"   Modelo: {cliente.modelo}")
        
        try:
            respuesta = cliente.generar_texto(
                "Narra brevemente el inicio de una aventura épica",
                max_tokens=100
            )
            print(f"\n📖 Respuesta:\n{respuesta}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    else:
        print("⚠️ Cliente de OpenAI no disponible")
        print("   Usando cliente mock para demostración...\n")
        
        cliente_mock = ClienteIAMock()
        
        respuesta = cliente_mock.generar_texto(
            "Describe un combate épico contra un dragón"
        )
        print(f"📖 Respuesta mock:\n{respuesta}")