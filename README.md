# Sistema de Rol "Ether Blades"
### Documento de especificación funcional y técnica

---

## 1. Descripción general del sistema

El sistema "Ether Blades" es un motor de juego de rol digital basado en las reglas del juego de mesa homónimo.  
Su objetivo es permitir la **creación de personajes**, el **avance narrativo dentro de un mundo persistente**, la **resolución determinista de combates**, y la **integración con un narrador inteligente** (basado en la API de ChatGPT) que describe los eventos y opciones del jugador.

La arquitectura del sistema sigue principios de **orientación a objetos**, **separación de responsabilidades** y aplicación de **patrones de diseño clásicos** para lograr modularidad, extensibilidad y mantenibilidad.

---

## 2. Objetivos funcionales principales

1. Crear, guardar y cargar personajes.
2. Ejecutar reglas de combate deterministas según los manuales.
3. Permitir instancias narrativas donde el jugador toma decisiones.
4. Generar narraciones dinámicas mediante un narrador IA.
5. Mantener registro persistente del progreso (puntos de historia, inventario, estadísticas).
6. Facilitar futuras expansiones (nuevas razas, armas, habilidades, mundos).

---

## 3. Estructura de directorios recomendada

```
etherblades/
│
├── main.py                        # Punto de entrada del sistema
│
├── entidades/                     # Clases del dominio
│   ├── personaje.py               # Clase Personaje y sus atributos
│   ├── ficha.py                   # Cálculo de PV, PM, PCF, PCT
│   ├── arma.py                    # Clases Arma base y subtipos (melee, distancia, mágica)
│   ├── habilidad.py               # Clases Habilidad y Efecto
│   ├── enemigo.py                 # Clase Enemigo y sus estrategias de IA
│   ├── inventario.py              # Gestión de objetos, ítems y equipo
│   ├── partida.py                 # Estado de juego y punto narrativo actual
│   └── escenario.py               # Representación del mundo (zonas, checkpoints)
│
├── servicios/                     # Lógica de aplicación
│   ├── combate_service.py         # Reglas y cálculos deterministas del combate
│   ├── historia_service.py        # Control de flujo narrativo
│   ├── narrador_service.py        # Integración con ChatGPT
│   ├── persistencia_service.py    # Guardar y cargar partidas
│   ├── eventos_service.py         # Sistema de eventos (Observer)
│   └── fabrica_service.py         # Creación de entidades (Factory Method)
│
├── patrones/                      # Implementaciones de patrones de diseño
│   ├── singleton.py               # Singleton para recursos únicos
│   ├── factory_method.py          # Factory base
│   ├── observer.py                # EventBus (suscripción y publicación)
│   ├── strategy.py                # Estrategias de combate y comportamiento
│   └── __init__.py
│
├── data/                          # Archivos de definición de armas, habilidades, etc.
│   ├── armas.json
│   ├── habilidades.json
│   └── enemigos.json
│
└── tests/                         # Pruebas unitarias y de integración
    ├── test_combate.py
    ├── test_persistencia.py
    └── test_narrador.py
```

---


---

## 4. Patrones de diseño aplicados

### 4.1 Singleton
**Uso:** garantizar una única instancia global de un recurso.

**Clases Singleton:**
- `ConfiguracionGlobal`: contiene reglas del sistema, versión, semilla, rutas de datos.
- `GestorPersistencia`: maneja los guardados/cargas de partidas.
- `ClienteIA`: interfaz con la API de ChatGPT, evita múltiples instancias que saturen la API.

**Funcionamiento:**
```python
# patrones/singleton.py
import threading

class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

### 4.2 Factory Method

Uso: crear entidades complejas (Armas, Habilidades, Enemigos) sin acoplar el código cliente a las clases concretas.

Clases:

FabricaArmas

FabricaHabilidades

FabricaEnemigos

**Funcionamiento:**
# patrones/factory_method.py

```class FabricaArmas:
    @staticmethod
    def crear_arma(tipo: str, **kwargs):
        from entidades.arma import ArmaMelee, ArmaDistancia, ArmaMagica
        if tipo == "melee":
            return ArmaMelee(**kwargs)
        elif tipo == "distancia":
            return ArmaDistancia(**kwargs)
        elif tipo == "magica":
            return ArmaMagica(**kwargs)
        else:
            raise ValueError(f"Tipo de arma desconocido: {tipo}")
            
Esto permite que, al leer un JSON con las armas, el sistema decida automáticamente qué clase instanciar.

4.3 Observer

Uso: notificar a subsistemas cuando ocurren eventos relevantes (daños, muertes, nivel-ups, etc.).

Clases:

EventBus (sujeto observado)

Subscriptores: UI, Logger, NarradorService, Autosave

Funcionamiento:

```# patrones/observer.py
class EventBus:
    def __init__(self):
        self._subscriptores = {}

    def suscribir(self, evento, callback):
        self._subscriptores.setdefault(evento, []).append(callback)

    def publicar(self, evento, data):
        for cb in self._subscriptores.get(evento, []):
            cb(data)
            
Ejemplos de uso:
``eventos = EventBus()
eventos.suscribir('ataque_resuelto', narrador_service.describir_evento)
eventos.suscribir('ataque_resuelto', ui.actualizar_pantalla)

4.4 Strategy

Uso: intercambiar algoritmos de cálculo de daño, elección de objetivos o comportamiento enemigo sin modificar el motor de combate.

Clases:

EstrategiaAtaque

EstrategiaAtaqueMelee

EstrategiaAtaqueDistancia

EstrategiaAtaqueMagica

EstrategiaIA

IAAgresiva

IAReservada

IAEvasiva

Funcionamiento:

``# patrones/strategy.py
from abc import ABC, abstractmethod

class EstrategiaAtaque(ABC):
    @abstractmethod
    def calcular_coeficiente(self, atacante, arma, dados):
        pass

class EstrategiaAtaqueMelee(EstrategiaAtaque):
    def calcular_coeficiente(self, atacante, arma, dados):
        return atacante.fuerza + sum(dados) + arma.bonus

class EstrategiaAtaqueDistancia(EstrategiaAtaque):
    def calcular_coeficiente(self, atacante, arma, dados):
        return atacante.punteria + sum(dados) + arma.bonus

El CombateService usa estas estrategias dinámicamente según el tipo de arma del atacante

. Servicios principales
5.1 CombateService

Encargado de ejecutar combates por turnos deterministas.
Aplica reglas de Ether Blades y comunica los resultados al EventBus.

Responsabilidades:

Calcular iniciativa (SP + D10)

Resolver ataques, defensas, daños y stamina

Disparar eventos (ataque_resuelto, personaje_muerto, fin_combate)

5.2 NarradorService

Recibe los eventos publicados y solicita una narración a ClienteIA.
Nunca altera resultados del combate: solo describe lo ocurrido y las consecuencias narrativas.

Flujo:

EventBus publica evento ataque_resuelto.

NarradorService genera prompt estructurado.

Llama a ClienteIA.narrar_evento(evento).

Retorna texto descriptivo para UI.

5.3 PersistenciaService

Responsable de guardar y restaurar el estado del juego.
Usa GestorPersistencia (Singleton) para garantizar un único acceso concurrente.

Datos persistidos:

Personaje (atributos, stats, inventario)

Enemigos y estado actual del combate

Checkpoint narrativo

Log de eventos importantes

Formato sugerido: JSON.

5.4 HistoriaService

Gestiona el flujo de historia fuera de combate.
Determina qué bloque narrativo mostrar según el punto actual y las decisiones del jugador.

6. Historias de Usuario (Ampliadas)
US-001: Creación de personaje

Como jugador
Quiero crear un personaje con raza, clase, atributos, hephix y trasfondo
Para comenzar una campaña personalizada

Criterios:

Se muestran atributos base y puntos disponibles.

Las fórmulas de PV, PM, PCF, PCT se aplican automáticamente.

El personaje se guarda en disco.

US-002: Guardar y cargar partida

Como jugador
Quiero poder guardar y continuar la partida
Para no perder mi progreso

Criterios:

Guardado serializa todos los datos relevantes (incluyendo estado narrativo).

Carga restaura fielmente la partida.

Persistencia gestionada por Singleton.

US-010: Combate determinista

Como jugador
Quiero que los combates sigan las reglas oficiales
Para mantener coherencia con el juego de mesa

Criterios:

Combate por turnos.

Tiradas de iniciativa, ataque y defensa con d10.

Aplicación de estrategias según tipo de arma.

Publicación de eventos.

US-011: Narración de eventos

Como jugador
Quiero ver narraciones dinámicas de mis acciones
Para sentir inmersión en el mundo

Criterios:

NarradorService recibe eventos de combate.

Llama a ChatGPT con contexto del mundo.

Muestra texto descriptivo.

US-020: Avance narrativo

Como jugador
Quiero que el mundo reaccione a mis decisiones
Para tener una historia dinámica

Criterios:

HistoriaService determina el siguiente bloque narrativo.

Las elecciones se validan por reglas.

El progreso se guarda en cada checkpoint.

US-030: Notificaciones globales

Como desarrollador
Quiero que subsistemas reciban eventos automáticamente
Para evitar acoplamiento entre módulos

Criterios:

EventBus implementa patrón Observer.

Los subscriptores registran callbacks.

Los eventos se propagan a todos los observadores.

US-040: Fábrica de entidades

Como desarrollador
Quiero crear entidades desde definiciones JSON
Para mantener un sistema extensible y desacoplado

Criterios:

FactoryMethod produce instancias correctas según tipo.

Los datos se cargan desde archivos de configuración.

Nuevos tipos de arma o habilidad pueden añadirse sin modificar código cliente.

US-050: Estrategias de combate

Como diseñador de juego
Quiero poder modificar la lógica de ataque sin tocar el motor
Para probar distintas variantes de reglas

Criterios:

EstrategiaAtaque seleccionada en tiempo de ejecución.

Nuevas estrategias se pueden registrar dinámicamente.

CombateService usa composición, no herencia.

US-060: Narrador con IA

Como jugador
Quiero que el narrador describa la historia según contexto
Para mantener coherencia y ambientación

Criterios:

NarradorService estructura prompts con datos objetivos.

IA responde en formato controlado.

Narraciones se almacenan para reuso.

US-070: Pruebas de motor

Como tester
Quiero verificar que los cálculos del motor son correctos
Para garantizar coherencia y reproducibilidad

Criterios:

Pruebas unitarias sobre cálculos de CA/CD, PV/PM, daño, stamina.

Verificación de publicación de eventos esperados.

Pruebas de regresión automática tras cada cambio.

7. Reglas de extensión modular

Nuevas armas o habilidades se agregan en data/ y se procesan con FactoryMethod.

Nuevas estrategias de combate o IA se agregan en patrones/strategy.py.

Nuevos eventos se suscriben sin modificar los publicadores.

El narrador IA puede ser reemplazado por otro modelo manteniendo la misma interfaz (NarradorService).

8. Consideraciones técnicas

Lenguaje: Python 3.12+

Persistencia: JSON plano o SQLite (opcional)

Dependencias externas: openai, pydantic, dataclasses-json

Testing: pytest

Principio de diseño: SRP (Single Responsibility), OCP (Open/Closed), Liskov Substitution.

9. Resumen de los patrones en el flujo general
Etapa	Patrón aplicado	Descripción breve
Carga de configuración	Singleton	ConfiguracionGlobal única
Creación de entidades	Factory Method	Fábricas para Armas, Habilidades, Enemigos
Cálculo de acciones	Strategy	Estrategias intercambiables de ataque o IA
Propagación de resultados	Observer	Notificación de eventos (UI, narrador, logs)
Persistencia de partidas	Singleton	GestorPersistencia único controlando accesos
Narrador IA	Observer + Singleton	Recibe eventos, usa instancia única de ClienteIA

10. Futuras ampliaciones

Implementar modo multijugador local (turnos alternos).

Editor visual de personajes.

Módulo de campaña y misiones.

Interfaz web o CLI avanzada.

Logs narrativos exportables como historia jugada.

Autor: Nicolás Bartolomeo
Materia: Computación II - Universidad de Mendoza
Sistema propuesto: Ether Blades RPG Engine
Versión: 1.0


