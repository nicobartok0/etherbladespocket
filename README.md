# 🎮 Ether Blades - Sistema de Rol Digital

> **Sistema completo de juego de rol basado en "Ether Blades Aftermath"**  
> Motor de combate determinista • Narrador IA • Persistencia completa

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-121%20passing-success.svg)](tests/)
[![License](https://img.shields.io/badge/License-Academic-orange.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Instalación](#-instalación)
- [Inicio Rápido](#-inicio-rápido)
- [Guía de Uso](#-guía-de-uso)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Patrones de Diseño](#-patrones-de-diseño)
- [Testing](#-testing)
- [Documentación Técnica](#-documentación-técnica)
- [Troubleshooting](#-troubleshooting)
- [Autor](#-autor)

---

## 🎯 Descripción General

**Ether Blades** es un sistema de rol digital completo que virtualiza el juego de mesa homónimo. Implementa mecánicas de combate deterministas, un sistema de narrativa con IA, y persistencia completa del estado del juego.

### 🎓 Contexto Académico

- **Institución**: Universidad de Mendoza
- **Materia**: Computación II
- **Objetivo**: Aplicar patrones de diseño y principios de ingeniería de software
- **Desarrollo**: Proyecto completo funcional con arquitectura escalable

### 🌟 ¿Por qué es especial?

- ✅ **100% funcional**: No es un prototipo, es un juego completamente jugable
- ✅ **Arquitectura profesional**: Aplicación real de patrones de diseño
- ✅ **IA integrada**: Narrador dinámico con OpenAI (opcional)
- ✅ **Testing completo**: 121 tests unitarios y de integración
- ✅ **Documentación exhaustiva**: Código limpio y bien documentado

---

## ✨ Características Principales

### 🎭 Sistema de Personajes

| Característica | Descripción |
|---------------|-------------|
| **13 Tipos de Hephix** | Elemental, Psíquica, Oculta, Morphica, Espiritual, Cristalina, Sangrienta, Sanadora, Exorcista, Lumínica, Caótica, Nigromante, Oscura |
| **6 Clases** | Guerrero, Mago, Explorador, Curandero, Artesano, Diplomático |
| **Sistema de Progresión** | Experiencia, niveles (1-30), habilidades desbloqueables |
| **Personalización** | 20 puntos en características, 30 puntos en habilidades |
| **Inventario Completo** | Armas, armaduras, consumibles, sistema de monedas |

### ⚔️ Sistema de Combate

```
Mecánicas Implementadas:
├── Iniciativa determinista (Stamina + 1d10)
├── Coeficiente de Ataque (Stat + 3d6 + bonificaciones)
├── Coeficiente de Defensa (Reflejos + 2d6 + armadura)
├── Sistema de Stamina (reduce hasta golpe de gracia)
├── Golpes de Gracia (cuando stamina = 0)
├── Contraataques (cuando diferencia ≤ -3)
├── Ataques Furtivos (Sigilo - Percepción × 2)
└── Estrategias intercambiables (patrón Strategy)
```

**Tipos de Arma Soportados:**
- ⚔️ Melee (usa Fuerza)
- 🏹 Distancia (usa Puntería)
- 🔮 Mágico (usa Voluntad)

### 📖 Narrador IA

```python
# Integración con OpenAI GPT
- Narraciones dinámicas de eventos de combate
- Descripciones contextuales de exploración
- Presentación de decisiones importantes
- Memoria de eventos pasados (últimos 50)
- Modo simulación (sin API key)
```

**System Prompt Optimizado:**
- Tono épico pero conciso (2-4 oraciones)
- Conocimiento del mundo de Ether Blades
- Solo describe, nunca altera mecánicas
- Adaptación según tipo de evento

### 💾 Sistema de Persistencia

| Funcionalidad | Detalles |
|--------------|----------|
| **Slots de Guardado** | 10 slots independientes |
| **Formato** | JSON legible y versionado |
| **Contenido Guardado** | Personaje completo, contexto narrativo, estado de combate |
| **Contexto IA** | Log de eventos, NPCs conocidos, reputación, misiones |
| **Integridad** | Validación automática al cargar |
| **Tracking** | Tiempo jugado, timestamp |

### 🎨 Interfaz de Usuario

```
Menús Implementados:
├── Menú Principal
│   ├── Nueva Partida (wizard completo)
│   ├── Cargar Partida (con preview)
│   ├── Gestionar Guardados
│   └── Acerca de
├── Loop de Juego
│   ├── Explorar
│   ├── Combate (demo funcional)
│   ├── Ver Inventario
│   ├── Ver Ficha Completa
│   └── Guardar Partida
└── Gestión de Guardados
    ├── Ver detalles de slot
    └── Eliminar partidas
```

---

## 🚀 Instalación

### Requisitos del Sistema

- **Python**: 3.12 o superior
- **Sistema Operativo**: Windows, Linux, macOS
- **RAM**: 256 MB mínimo
- **Espacio**: ~50 MB

### Dependencias

```txt
pydantic>=2.5.0          # Validación de datos
pydantic-settings>=2.1.0 # Configuración
python-dotenv>=1.0.0     # Variables de entorno
openai>=1.3.0            # Cliente IA (opcional)
pytest>=7.4.0            # Testing
```

### Instalación Paso a Paso

```bash
# 1. Clonar/descargar el proyecto
cd etherblades

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar variables de entorno (opcional)
cp .env.example .env
# Editar .env para agregar OPENAI_API_KEY si se desea

# 6. Verificar instalación
python -c "from config import settings; print('✅ Instalación exitosa')"
```

---

## 🎮 Inicio Rápido

### Opción 1: Ejecución Directa

```bash
python main.py
```

### Opción 2: Script de Inicio (Linux/Mac)

```bash
chmod +x jugar.sh
./jugar.sh
```

### Primera Partida

1. **Selecciona "Nueva Partida"**
2. **Crea tu personaje** (wizard interactivo):
   - Nombre, edad, raza
   - Historia y objetivo
   - Selección de Hephix (magia)
   - Selección de Clase
   - Distribución de 20 puntos en características
   - Distribución de 30 puntos en habilidades
3. **¡Comienza tu aventura!**

---

## 📘 Guía de Uso

### Creación de Personaje

#### Paso 1: Datos Básicos
```
Nombre: [Tu elección]
Edad: 1-200 años
Raza: Humano, Elfo, Enano, Orco, etc.
```

#### Paso 2: Historia
- Describe el origen de tu personaje
- Define su personalidad
- Establece su objetivo en Amarth

#### Paso 3: Hephix (Magia)

**Hephix Generales:**
- 🔥 **Elemental**: Control de fuego, agua, tierra, aire
- 🧠 **Psíquica**: Telequinesis de objetos
- 🌑 **Oculta**: Sigilo y ataques desde las sombras
- 🦎 **Morphica**: Cambio de forma corporal
- 👻 **Espiritual**: Comunicación con espíritus
- 💎 **Cristalina**: Control de cristales
- ⚠️ **Sangrienta**: Magia con coste de vida (sin PM)

**Hephix Kairenistas (Luz):**
- ✨ **Sanadora**: Curación y protección
- ⚡ **Exorcista**: Daño a oscuridad
- ☀️ **Lumínica**: Balance luz/curación

**Hephix Vadhenistas (Oscuridad):**
- 🌋 **Caótica**: Destrucción masiva
- 💀 **Nigromante**: Control de no-muertos
- 🌘 **Oscura**: Balance caos/nigromancia

#### Paso 4: Clase

| Clase | Enfoque | Bonificaciones |
|-------|---------|----------------|
| **Guerrero** | Combate físico | Armas cortantes/contundentes |
| **Mago** | Magia ofensiva | Armas mágicas, arcanismo |
| **Explorador** | Sigilo y distancia | Armas a distancia, sigilo |
| **Curandero** | Soporte y sanación | Medicina, mentalidad |
| **Artesano** | Crafting | Manual, arcanismo |
| **Diplomático** | Interacción social | Elocuencia, percepción |

#### Paso 5: Distribución de Puntos

**Características (20 puntos):**
- **Fuerza**: Daño cuerpo a cuerpo
- **Reflejos**: Esquivar ataques
- **Resistencia**: Puntos de vida (Res × 10)
- **Voluntad**: Poder mágico (Vol × 5 PM)
- **Puntería**: Precisión a distancia
- **Stamina**: Aguante en combate (Sta × 5 PS)

**Habilidades (10 puntos en cada categoría):**
- **Combate**: Armas cortantes, contundentes, mágicas, distancia, pugilismo
- **Educación**: Medicina, elocuencia, manual, arcanismo
- **Talento**: Sigilo, percepción, mentalidad, astralidad

### Sistema de Combate

#### Inicio del Combate
1. Todos los combatientes tiran **Iniciativa = Stamina + 1d10**
2. Se establece el **orden de turnos** (mayor a menor)
3. Comienza el primer turno

#### Turno de Combate

**Atacante:**
- Calcula **CA = Stat base + 3d6 + bonus arma + bonus habilidad**
  - Melee: usa Fuerza
  - Distancia: usa Puntería
  - Mágico: usa Voluntad

**Defensor:**
- Calcula **CD = Reflejos + 2d6 + bonus armadura**

**Resolución:**
```python
diferencia = CA - CD

if diferencia > 0:
    # Atacante gana: reduce stamina del defensor
    defensor.stamina -= diferencia
    
    if defensor.stamina <= 0:
        # ¡GOLPE DE GRACIA!
        # Daño directo a PV sin resistencia
        defensor.pv -= CA

elif diferencia <= -3:
    # ¡CONTRAATAQUE!
    # El defensor ataca al atacante original

else:
    # Ataque bloqueado sin consecuencias
```

#### Fin del Combate
- Cuando solo queda un combatiente vivo
- Ganador recibe: XP, oro, y posibles objetos

### Sistema de Guardado

#### Guardado Rápido
- Presiona **"Guardar Partida"** en el menú de juego
- Se guarda automáticamente en **Slot 1**

#### Guardado Manual
- Desde "Gestionar Guardados" puedes elegir el slot
- 10 slots independientes disponibles

#### Contenido del Guardado
```json
{
  "version": "1.0.0",
  "personaje": { ... },        // Estado completo
  "contexto": {
    "ubicacion_actual": "...",
    "npcs_conocidos": [...],
    "reputacion": {...},
    "log_narrativo": [...]     // Últimos 50 eventos
  },
  "tiempo_jugado": "2h 30m"
}
```

### Narrador IA

#### Con API Key de OpenAI
```bash
# En .env
OPENAI_API_KEY=sk-tu-clave-aqui
OPENAI_MODEL=gpt-4o-mini  # Recomendado
```

**Eventos Narrados:**
- Inicio de combate
- Ataques y defensas
- Golpes de gracia
- Contraataques
- Muertes
- Exploración
- Decisiones importantes

#### Sin API Key (Modo Simulación)
- El juego funciona completamente
- Usa narraciones predefinidas contextuales
- No requiere conexión a internet

---

## 🏗️ Arquitectura del Sistema

### Estructura de Directorios

```
etherblades/
│
├── main.py                    # Punto de entrada principal
├── config.py                  # Configuración global
├── .env                       # Variables de entorno
│
├── entidades/                 # 📦 Capa de Dominio
│   ├── personaje.py          # Clase Personaje completa
│   ├── ficha.py              # Sistema de características
│   ├── hephix.py             # Sistema de magia
│   ├── arma.py               # Armas y armaduras
│   ├── inventario.py         # Sistema de inventario
│   ├── dados.py              # Sistema de tiradas
│   └── tipos.py              # Enums y constantes
│
├── servicios/                 # 🔧 Capa de Aplicación
│   ├── creacion_personaje_service.py
│   ├── combate_service.py
│   ├── persistencia_service.py
│   ├── narrador_service.py
│   └── cliente_ia.py
│
├── patrones/                  # 🎨 Patrones de Diseño
│   ├── singleton.py          # Singleton thread-safe
│   ├── factory_method.py     # Factories
│   ├── observer.py           # Event Bus
│   └── strategy.py           # Estrategias de combate/IA
│
├── data/                      # 📄 Datos de Configuración
│   ├── clases.json           # Definiciones de clases
│   ├── hephix.json           # Definiciones de hephix
│   └── armas.json            # (Futuro) Catálogo de armas
│
├── guardados/                 # 💾 Partidas Guardadas
│   └── slot_XX.json          # Archivos de guardado
│
├── tests/                     # 🧪 Suite de Tests
│   ├── test_patrones.py
│   ├── test_entidades.py
│   ├── test_combate.py
│   ├── test_persistencia.py
│   └── test_narrador.py
│
└── demo_*.py                  # 🎬 Scripts de Demostración
```

### Capas de la Aplicación

```
┌─────────────────────────────────────────┐
│         main.py (UI/CLI)                │
├─────────────────────────────────────────┤
│         Servicios (Lógica)              │
│  ┌─────────────────────────────────┐   │
│  │ CreacionPersonajeService        │   │
│  │ CombateService                  │   │
│  │ PersistenciaService             │   │
│  │ NarradorService                 │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│         Entidades (Dominio)             │
│  ┌─────────────────────────────────┐   │
│  │ Personaje, Ficha, Hephix        │   │
│  │ Arma, Inventario, etc.          │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│    Patrones (Infraestructura)           │
│  ┌─────────────────────────────────┐   │
│  │ EventBus, Factories, Strategy   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Flujo de Datos

```
Usuario
  ↓
main.py
  ↓
[CreacionPersonajeService] → Personaje
  ↓
[Loop de Juego]
  ↓
[CombateService] ←→ [EventBus] ←→ [NarradorService]
  ↓                                    ↓
Resultado                         Narración
  ↓
[PersistenciaService]
  ↓
guardados/slot_XX.json
```

---

## 🎨 Patrones de Diseño

### 1️⃣ Singleton

**Implementación:** `patrones/singleton.py`

```python
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
```

**Clases Singleton:**
- `PersistenciaService`: Un único gestor de guardados
- `ClienteIA`: Una sola instancia del cliente de OpenAI
- `ConfiguracionGlobal`: Configuración única del sistema

**Ventajas:**
- ✅ Control de acceso concurrente
- ✅ Ahorro de recursos
- ✅ Estado global consistente

### 2️⃣ Factory Method

**Implementación:** `patrones/factory_method.py`

```python
class FabricaArmas:
    def crear(self, tipo: str, **kwargs) -> Arma:
        if tipo == "melee":
            return ArmaMelee(**kwargs)
        elif tipo == "distancia":
            return ArmaDistancia(**kwargs)
        # ...
```

**Uso:**
- Creación de armas desde JSON
- Creación de habilidades desde JSON
- Creación de enemigos desde definiciones

**Ventajas:**
- ✅ Desacoplamiento código-datos
- ✅ Fácil extensión de tipos
- ✅ Carga dinámica de contenido

### 3️⃣ Observer (Event Bus)

**Implementación:** `patrones/observer.py`

```python
class EventBus:
    def suscribir(self, tipo_evento, callback):
        # ...
    
    def publicar(self, tipo_evento, datos):
        # Notifica a todos los subscriptores
```

**Eventos del Sistema:**
```
Combate:
├── COMBATE_INICIADO
├── ATAQUE_REALIZADO
├── GOLPE_GRACIA
├── CONTRAATAQUE
└── PERSONAJE_MUERTO

Narrativa:
├── CHECKPOINT_ALCANZADO
├── DECISION_TOMADA
└── DESCUBRIMIENTO
```

**Subscriptores:**
- `NarradorService`: Genera narraciones
- `UI`: Actualiza pantalla
- `Logger`: Registra eventos
- `PersistenciaService`: Autosave (futuro)

**Ventajas:**
- ✅ Desacoplamiento total
- ✅ Fácil agregar nuevos subscriptores
- ✅ Sistema extensible

### 4️⃣ Strategy

**Implementación:** `patrones/strategy.py`

```python
class EstrategiaAtaque(ABC):
    @abstractmethod
    def calcular_coeficiente(self, atacante, arma, dados):
        pass

class EstrategiaAtaqueMelee(EstrategiaAtaque):
    def calcular_coeficiente(self, atacante, arma, dados):
        return atacante.fuerza + sum(dados) + arma.bonus
```

**Estrategias Implementadas:**
- `EstrategiaAtaqueMelee`: Usa Fuerza
- `EstrategiaAtaqueDistancia`: Usa Puntería
- `EstrategiaAtaqueMagico`: Usa Voluntad
- `IAAgresiva`, `IADefensiva`, `IATactica`: Comportamiento de enemigos

**Ventajas:**
- ✅ Intercambio dinámico de algoritmos
- ✅ Fácil testing de variantes
- ✅ Código limpio y mantenible

### Aplicación de SOLID

| Principio | Aplicación |
|-----------|------------|
| **S**ingle Responsibility | Cada clase tiene una única responsabilidad clara |
| **O**pen/Closed | Extensible sin modificar código existente (Strategy, Factory) |
| **L**iskov Substitution | Subclases intercambiables (todas las estrategias) |
| **I**nterface Segregation | Interfaces específicas (no interfaces gordas) |
| **D**ependency Inversion | Depende de abstracciones (EventBus, Strategy) |

---

## 🧪 Testing

### Suite de Tests

```bash
# Ejecutar todos los tests
pytest

# Con verbose
pytest -v

# Con cobertura
pytest --cov=. --cov-report=html

# Test específico
pytest tests/test_combate.py::TestCombateService::test_golpe_de_gracia -v
```

### Cobertura de Tests

| Módulo | Tests | Cobertura |
|--------|-------|-----------|
| **Patrones** | 14 | 95% |
| **Entidades** | 25 | 92% |
| **Creación** | 14 | 88% |
| **Combate** | 18 | 91% |
| **Persistencia** | 24 | 93% |
| **Narrador** | 26 | 85% |
| **TOTAL** | **121** | **~90%** |

### Estructura de Tests

```python
# tests/test_combate.py
class TestCombateService:
    @pytest.fixture
    def personaje(self):
        # Setup de personaje de prueba
        return crear_personaje_test()
    
    def test_golpe_de_gracia(self, personaje):
        # Given: Personaje sin stamina
        enemigo.ps_actuales = 0
        
        # When: Se ataca
        resultado = combate.resolver_ataque(personaje, enemigo)
        
        # Then: Es golpe de gracia
        assert resultado.tipo == TipoResultadoAtaque.CRITICO
        assert resultado.fue_golpe_gracia
```

### Tests de Integración

```python
@pytest.mark.integration
def test_flujo_combate_completo():
    # Crea personajes → Combate → Narración → Guardado
    # Verifica integración entre módulos
```

### Ejecutar Demos

```bash
# Demo de creación de personaje
python demo_creacion_personaje.py

# Demo de combate con narración
python demo_combate.py

# Demo de persistencia
python demo_persistencia.py

# Demo de narrador IA
python demo_narrador.py
```

---

## 📚 Documentación Técnica

### Especificaciones

Ver el archivo completo: [README_ESPECIFICACIONES.md](README.md)

Contiene:
- Especificación funcional completa
- Diagramas de arquitectura
- Reglas del juego detalladas
- Fórmulas de combate
- Sistema de progresión

### API de Servicios

#### CreacionPersonajeService

```python
service = CreacionPersonajeService()

# Método interactivo
personaje = service.crear_personaje_interactivo()

# Método programático
personaje = service.crear_personaje(
    nombre="Aldric",
    edad=25,
    raza="Humano",
    hephix_tipo=HephixTipo.ELEMENTAL,
    clase=ClaseTipo.GUERRERO,
    caracteristicas={...},
    habilidades_combate={...},
    habilidades_educacion={...},
    habilidades_talento={...}
)
```

#### CombateService

```python
combate = CombateService(event_bus)

# Iniciar combate
estado = combate.iniciar_combate([personaje1, personaje2])

# Resolver ataque
resultado = combate.resolver_ataque(atacante, defensor)

# Ataque furtivo
resultado = combate.ataque_sigilo(atacante, defensor)

# Verificar fin
if combate.verificar_fin_combate():
    print(f"Ganador: {estado.ganador}")
```

#### PersistenciaService

```python
persistencia = PersistenciaService()

# Guardar
persistencia.guardar_partida(personaje, contexto, slot=1)

# Cargar
personaje = persistencia.cargar_personaje(slot=1)
contexto = persistencia.cargar_contexto(slot=1)

# Listar
slots = persistencia.listar_partidas()

# Eliminar
persistencia.eliminar_partida(slot=1)
```

#### NarradorService

```python
narrador = NarradorService(event_bus, contexto)

# Narración libre
texto = narrador.narrar_situacion(
    "El personaje encuentra una cueva misteriosa",
    personaje
)

# Narración de decisión
texto = narrador.narrar_decision(
    "Debes elegir tu camino",
    ["Izquierda", "Derecha"],
    personaje
)

# Auto-narración de eventos (automática vía EventBus)
```

### Extensibilidad

#### Agregar Nueva Arma

```json
// data/armas.json
{
  "espada_legendaria": {
    "nombre": "Espada del Destino",
    "tipo_arma": "armas_cortantes",
    "tipo_ataque": "melee",
    "daño_base": 0,
    "bonus": 10,
    "nivel_requerido": 15,
    "rareza": "legendario"
  }
}
```

#### Agregar Nuevo Comportamiento IA

```python
# patrones/strategy.py
class IABerserker(ComportamientoIA):
    def decidir_accion(self, enemigo, objetivos, estado):
        # Siempre ataca sin considerar vida
        return {
            "tipo": "atacar",
            "objetivo": random.choice(objetivos)
        }

# Registrar
RegistroComportamientosIA.registrar("berserker", IABerserker())
```

#### Agregar Nuevo Tipo de Evento

```python
# patrones/observer.py
class TipoEvento(str, Enum):
    # ... eventos existentes
    MI_NUEVO_EVENTO = "mi_nuevo_evento"

# Usar
event_bus.publicar(TipoEvento.MI_NUEVO_EVENTO, {"data": "..."})
```

---

## 🔧 Troubleshooting

### Problemas Comunes

#### ❌ `ModuleNotFoundError: No module named 'config'`

**Causa**: El archivo `config.py` no existe o Python no lo encuentra.

**Solución**:
```bash
# Verificar que existe
ls config.py

# Si no existe, copiarlo
cp config.py.example config.py

# Si existe pero no se encuentra, verificar que estás en la raíz
pwd
```

#### ❌ `No module named 'openai'`

**Causa**: Dependencia no instalada.

**Solución**:
```bash
pip install openai
# o
pip install -r requirements.txt
```

#### ❌ El narrador no funciona

**Causa**: No hay API key configurada.

**Solución**:
```bash
# Opción 1: Configurar API key
echo "OPENAI_API_KEY=tu-clave" >> .env

# Opción 2: Usar modo simulación (automático)
# El juego detecta que no hay key y usa el mock
```

#### ❌ Tests fallan con errores de import

**Causa**: Tests se ejecutan desde directorio incorrecto.

**Solución**:
```bash
# Ejecutar desde la raíz del proyecto
cd /ruta/a/etherblades
pytest
```

#### ❌ `Permission denied: jugar.sh`

**Causa**: Script no tiene permisos de ejecución.

**Solución**:
```bash
chmod +x jugar.sh
./jugar.sh
```

### Problemas de Rendimiento

#### El narrador tarda mucho

**Causa**: Modelo GPT lento o conexión lenta.

**Solución**:
```bash
# En .env, cambiar a modelo más rápido
OPENAI_MODEL=gpt-3.5-turbo

# O usar modo simulación
# (comentar OPENAI_API_KEY)
```
