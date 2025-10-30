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
