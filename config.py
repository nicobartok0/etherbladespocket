"""
Configuración global del sistema Ether Blades.
Usa Pydantic Settings para cargar desde .env
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Configuración global del sistema"""
    
    # Configuración de OpenAI (opcional)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    narrador_max_tokens: int = 500
    narrador_temperature: float = 0.7
    
    # Configuración del sistema
    debug_mode: bool = True
    log_level: str = "INFO"
    
    # Rutas del proyecto
    data_dir: str = "data"
    guardados_dir: str = "guardados"
    
    # Versión del sistema (para compatibilidad de guardados)
    version: str = "1.0.0"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"  # Ignorar variables extra del .env
    )


# Instancia global de configuración
settings = Settings()