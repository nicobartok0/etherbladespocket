"""
Servicio de Persistencia - Gestión de guardado y carga de partidas.
Implementa el patrón Singleton para garantizar un único gestor.
"""
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime, timedelta
from entidades import Personaje
from patrones import SingletonMeta
from .persistencia_estructuras import (
    DatosPartida, ContextoNarrativo, InfoSlot,
    EstadoCombateGuardado
)


class PersistenciaService(metaclass=SingletonMeta):
    """
    Servicio de persistencia con patrón Singleton.
    Gestiona guardado y carga de partidas en formato JSON.
    """
    
    def __init__(self, directorio_guardados: str = "guardados"):
        """
        Args:
            directorio_guardados: Directorio donde se almacenan las partidas
        """
        self.directorio = Path(directorio_guardados)
        self.directorio.mkdir(exist_ok=True)
        
        # Tracking de tiempo de juego
        self._tiempo_inicio: Optional[datetime] = None
        self._tiempo_acumulado: timedelta = timedelta()
    
    # ========================================================================
    # Guardado de partidas
    # ========================================================================
    
    def guardar_partida(
        self,
        personaje: Personaje,
        contexto: ContextoNarrativo,
        slot: int = 1,
        nombre_partida: Optional[str] = None
    ) -> Path:
        """
        Guarda una partida completa en un slot.
        
        Args:
            personaje: Personaje a guardar
            contexto: Contexto narrativo
            slot: Número de slot (1-10)
            nombre_partida: Nombre descriptivo de la partida
        
        Returns:
            Path del archivo guardado
        
        Raises:
            ValueError: Si el slot es inválido
        """
        if not 1 <= slot <= 10:
            raise ValueError("El slot debe estar entre 1 y 10")
        
        # Preparar datos de partida
        datos = DatosPartida(
            slot=slot,
            nombre_partida=nombre_partida or f"Partida de {personaje.nombre}",
            tiempo_jugado=self._formatear_tiempo_jugado(),
            personaje=personaje.to_dict_guardado(),
            contexto=contexto,
            combate=EstadoCombateGuardado()  # TODO: Integrar con CombateService
        )
        
        # Determinar nombre de archivo
        archivo = self._obtener_ruta_slot(slot)
        
        # Guardar como JSON
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(
                datos.model_dump(mode='json'),
                f,
                ensure_ascii=False,
                indent=2,
                default=str  # Para datetime
            )
        
        return archivo
    
    def autoguardar(
        self,
        personaje: Personaje,
        contexto: ContextoNarrativo,
        slot: int = 1
    ) -> Path:
        """
        Realiza un guardado automático.
        Alias de guardar_partida con logging.
        """
        archivo = self.guardar_partida(personaje, contexto, slot)
        print(f"💾 Autoguardado en slot {slot}")
        return archivo
    
    # ========================================================================
    # Carga de partidas
    # ========================================================================
    
    def cargar_partida(self, slot: int) -> DatosPartida:
        """
        Carga una partida desde un slot.
        
        Args:
            slot: Número de slot a cargar
        
        Returns:
            Datos completos de la partida
        
        Raises:
            FileNotFoundError: Si el slot está vacío
            ValueError: Si el slot es inválido o los datos están corruptos
        """
        if not 1 <= slot <= 10:
            raise ValueError("El slot debe estar entre 1 y 10")
        
        archivo = self._obtener_ruta_slot(slot)
        
        if not archivo.exists():
            raise FileNotFoundError(f"El slot {slot} está vacío")
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos_raw = json.load(f)
            
            # Validar y parsear con Pydantic
            datos = DatosPartida.model_validate(datos_raw)
            
            return datos
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Archivo corrupto en slot {slot}: {e}")
        except Exception as e:
            raise ValueError(f"Error al cargar slot {slot}: {e}")
    
    def cargar_personaje(self, slot: int) -> Personaje:
        """
        Carga solo el personaje desde un slot.
        
        Args:
            slot: Número de slot
        
        Returns:
            Personaje restaurado
        """
        datos = self.cargar_partida(slot)
        personaje = Personaje.from_dict_guardado(datos.personaje)
        return personaje
    
    def cargar_contexto(self, slot: int) -> ContextoNarrativo:
        """
        Carga solo el contexto narrativo desde un slot.
        
        Args:
            slot: Número de slot
        
        Returns:
            Contexto narrativo restaurado
        """
        datos = self.cargar_partida(slot)
        return datos.contexto
    
    # ========================================================================
    # Gestión de slots
    # ========================================================================
    
    def listar_partidas(self) -> List[InfoSlot]:
        """
        Lista información de todos los slots de guardado.
        
        Returns:
            Lista con información de cada slot (vacíos y ocupados)
        """
        slots = []
        
        for slot_num in range(1, 11):
            archivo = self._obtener_ruta_slot(slot_num)
            
            if archivo.exists():
                try:
                    datos = self.cargar_partida(slot_num)
                    info = InfoSlot(
                        slot=slot_num,
                        existe=True,
                        nombre_personaje=datos.personaje.get('nombre'),
                        nivel=datos.personaje.get('nivel'),
                        ubicacion=datos.contexto.ubicacion_actual,
                        timestamp=datos.timestamp,
                        tiempo_jugado=datos.tiempo_jugado
                    )
                except Exception:
                    # Slot corrupto, marcarlo como vacío
                    info = InfoSlot(slot=slot_num, existe=False)
            else:
                info = InfoSlot(slot=slot_num, existe=False)
            
            slots.append(info)
        
        return slots
    
    def existe_partida(self, slot: int) -> bool:
        """Verifica si existe una partida en el slot"""
        archivo = self._obtener_ruta_slot(slot)
        return archivo.exists()
    
    def eliminar_partida(self, slot: int) -> bool:
        """
        Elimina una partida guardada.
        
        Args:
            slot: Número de slot a eliminar
        
        Returns:
            True si se eliminó, False si no existía
        """
        archivo = self._obtener_ruta_slot(slot)
        
        if archivo.exists():
            archivo.unlink()
            return True
        
        return False
    
    # ========================================================================
    # Gestión de tiempo de juego
    # ========================================================================
    
    def iniciar_sesion(self):
        """Inicia el tracking de tiempo de juego"""
        self._tiempo_inicio = datetime.now()
    
    def pausar_sesion(self):
        """Pausa el tracking y acumula el tiempo"""
        if self._tiempo_inicio:
            tiempo_sesion = datetime.now() - self._tiempo_inicio
            self._tiempo_acumulado += tiempo_sesion
            self._tiempo_inicio = None
    
    def obtener_tiempo_jugado(self) -> timedelta:
        """Obtiene el tiempo total jugado"""
        tiempo_total = self._tiempo_acumulado
        
        if self._tiempo_inicio:
            tiempo_total += datetime.now() - self._tiempo_inicio
        
        return tiempo_total
    
    def _formatear_tiempo_jugado(self) -> str:
        """Formatea el tiempo jugado como string legible"""
        tiempo = self.obtener_tiempo_jugado()
        horas = int(tiempo.total_seconds() // 3600)
        minutos = int((tiempo.total_seconds() % 3600) // 60)
        
        return f"{horas}h {minutos}m"
    
    # ========================================================================
    # Utilidades privadas
    # ========================================================================
    
    def _obtener_ruta_slot(self, slot: int) -> Path:
        """Obtiene la ruta del archivo de un slot"""
        return self.directorio / f"slot_{slot:02d}.json"
    
    # ========================================================================
    # Validación e integridad
    # ========================================================================
    
    def verificar_integridad(self, slot: int) -> tuple[bool, Optional[str]]:
        """
        Verifica la integridad de un guardado.
        
        Args:
            slot: Número de slot a verificar
        
        Returns:
            (es_valido, mensaje_error)
        """
        try:
            datos = self.cargar_partida(slot)
            
            # Verificaciones básicas
            if not datos.personaje.get('nombre'):
                return False, "Datos de personaje incompletos"
            
            if datos.version != "1.0.0":
                return False, f"Versión incompatible: {datos.version}"
            
            return True, None
            
        except FileNotFoundError:
            return False, "Slot vacío"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def reparar_guardado(self, slot: int) -> bool:
        """
        Intenta reparar un guardado corrupto.
        
        Args:
            slot: Slot a reparar
        
        Returns:
            True si se reparó exitosamente
        """
        # TODO: Implementar lógica de reparación
        # Por ahora solo retorna False
        return False


if __name__ == "__main__":
    from entidades import Ficha, Hephix, HephixTipo, ClaseTipo
    
    print("=== Demo del Sistema de Persistencia ===\n")
    
    # Crear personaje de prueba
    ficha = Ficha()
    ficha.caracteristicas.fuerza = 8
    ficha.caracteristicas.resistencia = 7
    ficha.caracteristicas.stamina = 3
    
    personaje = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha,
        historia="Un guerrero valiente"
    )
    
    # Crear contexto
    contexto = ContextoNarrativo(
        checkpoint_actual="inicio_aventura",
        ubicacion_actual="Ciudad de Amarth"
    )
    
    # Obtener servicio (Singleton)
    servicio = PersistenciaService()
    servicio.iniciar_sesion()
    
    # Guardar
    print("Guardando partida en slot 1...")
    archivo = servicio.guardar_partida(personaje, contexto, slot=1)
    print(f"✅ Guardado en: {archivo}\n")
    
    # Listar partidas
    print("Partidas guardadas:")
    for info in servicio.listar_partidas():
        if info.existe:
            print(f"  {info}")
    
    # Cargar
    print("\nCargando partida del slot 1...")
    datos_cargados = servicio.cargar_partida(1)
    print(f"✅ Partida cargada: {datos_cargados.nombre_partida}")
    print(f"   Personaje: {datos_cargados.personaje['nombre']}")
    print(f"   Ubicación: {datos_cargados.contexto.ubicacion_actual}")