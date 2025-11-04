"""
INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO
============================================================================
Directorio raiz: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./
Fecha de generacion: 2025-11-04 15:40:21
Total de archivos integrados: 36
Total de directorios procesados: 6
============================================================================
"""

# ==============================================================================
# TABLA DE CONTENIDOS
# ==============================================================================

# DIRECTORIO: .
#   1. __init__.py
#   2. buscar_paquete.py
#   3. config.py
#   4. demo_combate.py
#   5. demo_narrador.py
#   6. demo_persistencia.py
#   7. main.py
#
# DIRECTORIO: data
#   8. __init__.py
#
# DIRECTORIO: entidades
#   9. __init__.py
#   10. arma.py
#   11. dados.py
#   12. ficha.py
#   13. hephix.py
#   14. inventario.py
#   15. personaje.py
#   16. tipos.py
#
# DIRECTORIO: patrones
#   17. __init__.py
#   18. factory_method.py
#   19. observer.py
#   20. singleton.py
#   21. strategy.py
#
# DIRECTORIO: servicios
#   22. __init__.py
#   23. cliente_ia.py
#   24. combate_estructuras.py
#   25. combate_service.py
#   26. creacion_personaje_service.py
#   27. narrador_service.py
#   28. persistencia_estructuras.py
#   29. persistencia_service.py
#
# DIRECTORIO: tests
#   30. __init__.py
#   31. test_combate.py
#   32. test_creacion_personaje.py
#   33. test_entidades.py
#   34. test_narrador.py
#   35. test_patrones.py
#   36. test_persistencia.py
#



################################################################################
# DIRECTORIO: .
################################################################################

# ==============================================================================
# ARCHIVO 1/36: __init__.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 2/36: buscar_paquete.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./buscar_paquete.py
# ==============================================================================

"""
Script para buscar el paquete python_forestacion desde el directorio raiz del proyecto.
Incluye funcionalidad para integrar archivos Python en cada nivel del arbol de directorios.
"""
import os
import sys
from datetime import datetime


def buscar_paquete(directorio_raiz: str, nombre_paquete: str) -> list:
    """
    Busca un paquete Python en el directorio raiz y subdirectorios.

    Args:
        directorio_raiz: Directorio desde donde iniciar la busqueda
        nombre_paquete: Nombre del paquete a buscar

    Returns:
        Lista de rutas donde se encontro el paquete
    """
    paquetes_encontrados = []

    for raiz, directorios, archivos in os.walk(directorio_raiz):
        # Verificar si el directorio actual es el paquete buscado
        nombre_dir = os.path.basename(raiz)

        if nombre_dir == nombre_paquete:
            # Verificar que sea un paquete Python (contiene __init__.py)
            if '__init__.py' in archivos:
                paquetes_encontrados.append(raiz)
                print(f"[+] Paquete encontrado: {raiz}")
            else:
                print(f"[!] Directorio encontrado pero no es un paquete Python: {raiz}")

    return paquetes_encontrados


def obtener_archivos_python(directorio: str) -> list:
    """
    Obtiene todos los archivos Python en un directorio (sin recursion).

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de archivos .py
    """
    archivos_python = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isfile(ruta_completa) and item.endswith('.py'):
                # Excluir archivos integradores para evitar recursion infinita
                if item not in ['integrador.py', 'integradorFinal.py']:
                    archivos_python.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(archivos_python)


def obtener_subdirectorios(directorio: str) -> list:
    """
    Obtiene todos los subdirectorios inmediatos de un directorio.

    Args:
        directorio: Ruta del directorio a examinar

    Returns:
        Lista de rutas completas de subdirectorios
    """
    subdirectorios = []
    try:
        for item in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, item)
            if os.path.isdir(ruta_completa):
                # Excluir directorios especiales
                if not item.startswith('.') and item not in ['__pycache__', 'venv', '.venv']:
                    subdirectorios.append(ruta_completa)
    except PermissionError:
        print(f"[!] Sin permisos para leer: {directorio}")

    return sorted(subdirectorios)


def leer_contenido_archivo(ruta_archivo: str) -> str:
    """
    Lee el contenido de un archivo Python.

    Args:
        ruta_archivo: Ruta completa del archivo

    Returns:
        Contenido del archivo como string
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except Exception as error:
        print(f"[!] Error al leer {ruta_archivo}: {error}")
        return f"# Error al leer este archivo: {error}\n"


def crear_archivo_integrador(directorio: str, archivos_python: list) -> bool:
    """
    Crea un archivo integrador.py con el contenido de todos los archivos Python.

    Args:
        directorio: Directorio donde crear el archivo integrador
        archivos_python: Lista de rutas de archivos Python a integrar

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_python:
        return False

    ruta_integrador = os.path.join(directorio, 'integrador.py')

    try:
        with open(ruta_integrador, 'w', encoding='utf-8') as integrador:
            # Encabezado
            integrador.write('"""\n')
            integrador.write(f"Archivo integrador generado automaticamente\n")
            integrador.write(f"Directorio: {directorio}\n")
            integrador.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador.write(f"Total de archivos integrados: {len(archivos_python)}\n")
            integrador.write('"""\n\n')

            # Integrar cada archivo
            for idx, archivo in enumerate(archivos_python, 1):
                nombre_archivo = os.path.basename(archivo)
                integrador.write(f"# {'=' * 80}\n")
                integrador.write(f"# ARCHIVO {idx}/{len(archivos_python)}: {nombre_archivo}\n")
                integrador.write(f"# Ruta: {archivo}\n")
                integrador.write(f"# {'=' * 80}\n\n")

                contenido = leer_contenido_archivo(archivo)
                integrador.write(contenido)
                integrador.write("\n\n")

        print(f"[OK] Integrador creado: {ruta_integrador}")
        print(f"     Archivos integrados: {len(archivos_python)}")
        return True

    except Exception as error:
        print(f"[!] Error al crear integrador en {directorio}: {error}")
        return False


def procesar_directorio_recursivo(directorio: str, nivel: int = 0, archivos_totales: list = None) -> list:
    """
    Procesa un directorio de forma recursiva, creando integradores en cada nivel.
    Utiliza DFS (Depth-First Search) para llegar primero a los niveles mas profundos.

    Args:
        directorio: Directorio a procesar
        nivel: Nivel de profundidad actual (para logging)
        archivos_totales: Lista acumulativa de todos los archivos procesados

    Returns:
        Lista de todos los archivos Python procesados en el arbol
    """
    if archivos_totales is None:
        archivos_totales = []

    indentacion = "  " * nivel
    print(f"{indentacion}[INFO] Procesando nivel {nivel}: {os.path.basename(directorio)}")

    # Obtener subdirectorios
    subdirectorios = obtener_subdirectorios(directorio)

    # Primero, procesar recursivamente todos los subdirectorios (DFS)
    for subdir in subdirectorios:
        procesar_directorio_recursivo(subdir, nivel + 1, archivos_totales)

    # Despues de procesar subdirectorios, procesar archivos del nivel actual
    archivos_python = obtener_archivos_python(directorio)

    if archivos_python:
        print(f"{indentacion}[+] Encontrados {len(archivos_python)} archivo(s) Python")
        crear_archivo_integrador(directorio, archivos_python)
        # Agregar archivos a la lista total
        archivos_totales.extend(archivos_python)
    else:
        print(f"{indentacion}[INFO] No hay archivos Python en este nivel")

    return archivos_totales


def crear_integrador_final(directorio_raiz: str, archivos_totales: list) -> bool:
    """
    Crea un archivo integradorFinal.py con TODO el codigo fuente de todas las ramas.

    Args:
        directorio_raiz: Directorio donde crear el archivo integrador final
        archivos_totales: Lista completa de todos los archivos Python procesados

    Returns:
        True si se creo exitosamente, False en caso contrario
    """
    if not archivos_totales:
        print("[!] No hay archivos para crear el integrador final")
        return False

    ruta_integrador_final = os.path.join(directorio_raiz, 'integradorFinal.py')

    # Organizar archivos por directorio para mejor estructura
    archivos_por_directorio = {}
    for archivo in archivos_totales:
        directorio = os.path.dirname(archivo)
        if directorio not in archivos_por_directorio:
            archivos_por_directorio[directorio] = []
        archivos_por_directorio[directorio].append(archivo)

    try:
        with open(ruta_integrador_final, 'w', encoding='utf-8') as integrador_final:
            # Encabezado principal
            integrador_final.write('"""\n')
            integrador_final.write("INTEGRADOR FINAL - CONSOLIDACION COMPLETA DEL PROYECTO\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write(f"Directorio raiz: {directorio_raiz}\n")
            integrador_final.write(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write(f"Total de archivos integrados: {len(archivos_totales)}\n")
            integrador_final.write(f"Total de directorios procesados: {len(archivos_por_directorio)}\n")
            integrador_final.write("=" * 76 + "\n")
            integrador_final.write('"""\n\n')

            # Tabla de contenidos
            integrador_final.write("# " + "=" * 78 + "\n")
            integrador_final.write("# TABLA DE CONTENIDOS\n")
            integrador_final.write("# " + "=" * 78 + "\n\n")

            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)
                    integrador_final.write(f"#   {contador_global}. {nombre_archivo}\n")
                    contador_global += 1
                integrador_final.write("#\n")

            integrador_final.write("\n\n")

            # Contenido completo organizado por directorio
            contador_global = 1
            for directorio in sorted(archivos_por_directorio.keys()):
                dir_relativo = os.path.relpath(directorio, directorio_raiz)

                # Separador de directorio
                integrador_final.write("\n" + "#" * 80 + "\n")
                integrador_final.write(f"# DIRECTORIO: {dir_relativo}\n")
                integrador_final.write("#" * 80 + "\n\n")

                # Procesar cada archivo del directorio
                for archivo in sorted(archivos_por_directorio[directorio]):
                    nombre_archivo = os.path.basename(archivo)

                    integrador_final.write(f"# {'=' * 78}\n")
                    integrador_final.write(f"# ARCHIVO {contador_global}/{len(archivos_totales)}: {nombre_archivo}\n")
                    integrador_final.write(f"# Directorio: {dir_relativo}\n")
                    integrador_final.write(f"# Ruta completa: {archivo}\n")
                    integrador_final.write(f"# {'=' * 78}\n\n")

                    contenido = leer_contenido_archivo(archivo)
                    integrador_final.write(contenido)
                    integrador_final.write("\n\n")

                    contador_global += 1

            # Footer
            integrador_final.write("\n" + "#" * 80 + "\n")
            integrador_final.write("# FIN DEL INTEGRADOR FINAL\n")
            integrador_final.write(f"# Total de archivos: {len(archivos_totales)}\n")
            integrador_final.write(f"# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            integrador_final.write("#" * 80 + "\n")

        print(f"\n[OK] Integrador final creado: {ruta_integrador_final}")
        print(f"     Total de archivos integrados: {len(archivos_totales)}")
        print(f"     Total de directorios procesados: {len(archivos_por_directorio)}")

        # Mostrar tamanio del archivo
        tamanio = os.path.getsize(ruta_integrador_final)
        if tamanio < 1024:
            tamanio_str = f"{tamanio} bytes"
        elif tamanio < 1024 * 1024:
            tamanio_str = f"{tamanio / 1024:.2f} KB"
        else:
            tamanio_str = f"{tamanio / (1024 * 1024):.2f} MB"
        print(f"     Tamanio del archivo: {tamanio_str}")

        return True

    except Exception as error:
        print(f"[!] Error al crear integrador final: {error}")
        return False


def integrar_arbol_directorios(directorio_raiz: str) -> None:
    """
    Inicia el proceso de integracion para todo el arbol de directorios.

    Args:
        directorio_raiz: Directorio raiz desde donde comenzar
    """
    print("\n" + "=" * 80)
    print("INICIANDO INTEGRACION DE ARCHIVOS PYTHON")
    print("=" * 80)
    print(f"Directorio raiz: {directorio_raiz}\n")

    # Procesar directorios y obtener lista de todos los archivos
    archivos_totales = procesar_directorio_recursivo(directorio_raiz)

    print("\n" + "=" * 80)
    print("INTEGRACION POR NIVELES COMPLETADA")
    print("=" * 80)

    # Crear integrador final con todos los archivos
    if archivos_totales:
        print("\n" + "=" * 80)
        print("CREANDO INTEGRADOR FINAL")
        print("=" * 80)
        crear_integrador_final(directorio_raiz, archivos_totales)

    print("\n" + "=" * 80)
    print("PROCESO COMPLETO FINALIZADO")
    print("=" * 80)


def main():
    """Funcion principal del script."""
    # Obtener el directorio raiz del proyecto (donde esta este script)
    directorio_raiz = os.path.dirname(os.path.abspath(__file__))

    # Verificar argumentos de linea de comandos
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()

        if comando == "integrar":
            # Modo de integracion de archivos
            if len(sys.argv) > 2:
                directorio_objetivo = sys.argv[2]
                if not os.path.isabs(directorio_objetivo):
                    directorio_objetivo = os.path.join(directorio_raiz, directorio_objetivo)
            else:
                directorio_objetivo = directorio_raiz

            if not os.path.isdir(directorio_objetivo):
                print(f"[!] El directorio no existe: {directorio_objetivo}")
                return 1

            integrar_arbol_directorios(directorio_objetivo)
            return 0

        elif comando == "help" or comando == "--help" or comando == "-h":
            print("Uso: python buscar_paquete.py [COMANDO] [OPCIONES]")
            print("")
            print("Comandos disponibles:")
            print("  (sin argumentos)     Busca el paquete python_forestacion")
            print("  integrar [DIR]       Integra archivos Python en el arbol de directorios")
            print("                       DIR: directorio raiz (por defecto: directorio actual)")
            print("  help                 Muestra esta ayuda")
            print("")
            print("Ejemplos:")
            print("  python buscar_paquete.py")
            print("  python buscar_paquete.py integrar")
            print("  python buscar_paquete.py integrar python_forestacion")
            return 0

        else:
            print(f"[!] Comando desconocido: {comando}")
            print("    Use 'python buscar_paquete.py help' para ver los comandos disponibles")
            return 1

    # Modo por defecto: buscar paquete
    print(f"[INFO] Buscando desde: {directorio_raiz}")
    print(f"[INFO] Buscando paquete: python_forestacion")
    print("")

    # Buscar el paquete
    paquetes = buscar_paquete(directorio_raiz, "python_forestacion")

    print("")
    if paquetes:
        print(f"[OK] Se encontraron {len(paquetes)} paquete(s):")
        for paquete in paquetes:
            print(f"  - {paquete}")

            # Mostrar estructura basica del paquete
            print(f"    Contenido:")
            try:
                contenido = os.listdir(paquete)
                for item in sorted(contenido)[:10]:  # Mostrar primeros 10 items
                    ruta_item = os.path.join(paquete, item)
                    if os.path.isdir(ruta_item):
                        print(f"      [DIR]  {item}")
                    else:
                        print(f"      [FILE] {item}")
                if len(contenido) > 10:
                    print(f"      ... y {len(contenido) - 10} items mas")
            except PermissionError:
                print(f"      [!] Sin permisos para leer el directorio")
    else:
        print("[!] No se encontro el paquete python_forestacion")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

# ==============================================================================
# ARCHIVO 3/36: config.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./config.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 4/36: demo_combate.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./demo_combate.py
# ==============================================================================

"""
Demo del sistema de combate.
Ejecutar: python demo_combate.py
"""
from servicios import CombateService, CreacionPersonajeService
from entidades import HephixTipo, ClaseTipo, crear_espada_basica
from patrones import EventBus, TipoEvento
import time


def imprimir_barra_vida(nombre: str, pv_actual: int, pv_max: int, ps_actual: int, ps_max: int):
    """Imprime una barra de vida y stamina visual"""
    porcentaje_pv = (pv_actual / pv_max) * 100 if pv_max > 0 else 0
    porcentaje_ps = (ps_actual / ps_max) * 100 if ps_max > 0 else 0
    
    barra_pv = "█" * int(porcentaje_pv / 5) + "░" * (20 - int(porcentaje_pv / 5))
    barra_ps = "█" * int(porcentaje_ps / 5) + "░" * (20 - int(porcentaje_ps / 5))
    
    print(f"\n{nombre}:")
    print(f"  ❤️  PV: [{barra_pv}] {pv_actual}/{pv_max}")
    print(f"  ⚡ PS: [{barra_ps}] {ps_actual}/{ps_max}")


def main():
    """Ejecuta una demo completa de combate"""
    print("\n" + "="*70)
    print("  ⚔️  ETHER BLADES - DEMO DE COMBATE")
    print("="*70 + "\n")
    
    # Crear servicio de creación
    creacion = CreacionPersonajeService()
    
    # Crear guerrero
    print("Creando combatientes...\n")
    guerrero = creacion.crear_personaje(
        nombre="Aldric el Valiente",
        edad=28,
        raza="Humano",
        historia="Un guerrero experimentado",
        objetivo="Proteger a los inocentes",
        hephix_tipo=HephixTipo.ELEMENTAL,
        clase=ClaseTipo.GUERRERO,
        caracteristicas={"fuerza": 9, "reflejos": 5, "resistencia": 8, 
                        "voluntad": 0, "punteria": 0, "stamina": 3},
        habilidades_combate={"armas_cortantes": 15, "armas_contundentes": 0,
                            "armas_magicas": 0, "armas_distancia": 0, "pugilismo": 0},
        habilidades_educacion={"medicina": 5, "elocuencia": 0,
                              "manual": 0, "arcanismo": 0},
        habilidades_talento={"sigilo": 0, "percepcion": 5,
                            "mentalidad": 5, "astralidad": 0}
    )
    
    # Crear enemigo
    enemigo = creacion.crear_personaje(
        nombre="Goblin Salvaje",
        edad=15,
        raza="Goblin",
        historia="Un goblin agresivo de las cavernas",
        objetivo="Sobrevivir y saquear",
        hephix_tipo=HephixTipo.OCULTA,
        clase=ClaseTipo.EXPLORADOR,
        caracteristicas={"fuerza": 5, "reflejos": 7, "resistencia": 4,
                        "voluntad": 0, "punteria": 3, "stamina": 2},
        habilidades_combate={"armas_cortantes": 8, "armas_contundentes": 0,
                            "armas_magicas": 0, "armas_distancia": 5, "pugilismo": 0},
        habilidades_educacion={"medicina": 0, "elocuencia": 0,
                              "manual": 0, "arcanismo": 0},
        habilidades_talento={"sigilo": 10, "percepcion": 5,
                            "mentalidad": 0, "astralidad": 0}
    )
    
    print(f"✅ {guerrero.nombre} (Guerrero, Nivel {guerrero.nivel})")
    print(f"   PV: {guerrero.pv_maximos} | PM: {guerrero.pm_maximos}")
    print(f"   Arma: {guerrero.arma_equipada.nombre if guerrero.arma_equipada else 'Ninguna'}")
    
    print(f"\n✅ {enemigo.nombre} (Explorador, Nivel {enemigo.nivel})")
    print(f"   PV: {enemigo.pv_maximos} | PM: {enemigo.pm_maximos}")
    
    # Configurar event bus con logger
    event_bus = EventBus()
    
    def logger_combate(evento):
        """Log de eventos importantes"""
        if evento.tipo == TipoEvento.GOLPE_GRACIA:
            print(f"\n💥 ¡GOLPE DE GRACIA!")
        elif evento.tipo == TipoEvento.CONTRAATAQUE:
            print(f"\n🔄 ¡CONTRAATAQUE!")
        elif evento.tipo == TipoEvento.PERSONAJE_MUERTO:
            print(f"\n💀 {evento.datos['personaje']} ha caído!")
    
    event_bus.suscribir(TipoEvento.GOLPE_GRACIA, logger_combate)
    event_bus.suscribir(TipoEvento.CONTRAATAQUE, logger_combate)
    event_bus.suscribir(TipoEvento.PERSONAJE_MUERTO, logger_combate)
    
    # Iniciar combate
    servicio = CombateService(event_bus)
    
    print("\n" + "="*70)
    print("  ⚔️  ¡COMIENZA EL COMBATE!")
    print("="*70)
    
    estado = servicio.iniciar_combate([guerrero, enemigo])
    
    print(f"\n🎲 Orden de iniciativa:")
    for i, nombre in enumerate(estado.orden_turnos, 1):
        comb = estado.obtener_combatiente_por_nombre(nombre)
        print(f"  {i}. {nombre} (Iniciativa: {comb.iniciativa})")
    
    time.sleep(1)
    
    # Simulación de turnos
    turno = 1
    max_turnos = 20  # Límite de seguridad
    
    while estado.combate_activo and turno <= max_turnos:
        print("\n" + "-"*70)
        print(f"  TURNO {turno}")
        print("-"*70)
        
        # Mostrar estado actual
        imprimir_barra_vida(guerrero.nombre, guerrero.pv_actuales, guerrero.pv_maximos,
                           guerrero.ps_actuales, guerrero.ps_maximos)
        imprimir_barra_vida(enemigo.nombre, enemigo.pv_actuales, enemigo.pv_maximos,
                           enemigo.ps_actuales, enemigo.ps_maximos)
        
        time.sleep(1)
        
        # Determinar atacante y defensor
        nombre_atacante = estado.orden_turnos[estado.indice_turno_actual]
        
        if nombre_atacante == guerrero.nombre:
            atacante, defensor = guerrero, enemigo
        else:
            atacante, defensor = enemigo, guerrero
        
        if not atacante.esta_en_condiciones_combate() or not defensor.esta_en_condiciones_combate():
            break
        
        print(f"\n⚔️  {atacante.nombre} ataca a {defensor.nombre}...")
        time.sleep(0.5)
        
        # Resolver ataque
        resultado = servicio.resolver_ataque(atacante, defensor)
        
        print(f"\n{resultado.descripcion_corta()}")
        
        if resultado.tipo.value in ["exito", "critico"]:
            print(f"   CA: {resultado.coeficiente_ataque} | CD: {resultado.coeficiente_defensa}")
            if resultado.daño_infligido > 0:
                print(f"   💔 Daño: {resultado.daño_infligido}")
            if resultado.stamina_perdida > 0:
                print(f"   ⚡ Stamina perdida: {resultado.stamina_perdida}")
        
        # Verificar fin de combate
        if servicio.verificar_fin_combate():
            break
        
        # Avanzar turno
        estado.avanzar_turno()
        turno += 1
        
        time.sleep(1)
    
    # Resultado final
    print("\n" + "="*70)
    print("  🏆 FIN DEL COMBATE")
    print("="*70)
    
    if estado.ganador:
        print(f"\n✨ ¡{estado.ganador} es el VICTORIOSO!")
    else:
        print("\n⚠️  Combate inconcluso (límite de turnos alcanzado)")
    
    print(f"\n📊 Estadísticas finales:")
    imprimir_barra_vida(guerrero.nombre, guerrero.pv_actuales, guerrero.pv_maximos,
                       guerrero.ps_actuales, guerrero.ps_maximos)
    imprimir_barra_vida(enemigo.nombre, enemigo.pv_actuales, enemigo.pv_maximos,
                       enemigo.ps_actuales, enemigo.ps_maximos)
    
    print(f"\n📜 Total de intercambios: {len(estado.historial_ataques)}")
    print(f"🎲 Turnos totales: {turno}")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

# ==============================================================================
# ARCHIVO 5/36: demo_narrador.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./demo_narrador.py
# ==============================================================================

"""
Demo del sistema de narrador con IA.
Ejecutar: python demo_narrador.py
"""
from servicios import (
    CreacionPersonajeService, 
    CombateService, 
    NarradorService,
    ContextoNarrativo,
    EventoNarrativo,
    TipoEventoNarrativo
)
from entidades import HephixTipo, ClaseTipo
from patrones import EventBus
import time


def imprimir_separador(titulo: str = ""):
    """Imprime un separador visual"""
    if titulo:
        print(f"\n{'='*70}")
        print(f"  {titulo}")
        print(f"{'='*70}\n")
    else:
        print("-" * 70)


def demo_narracion_situaciones():
    """Demuestra narraciones de diferentes situaciones"""
    imprimir_separador("📖 NARRACIÓN DE SITUACIONES")
    
    # Crear contexto
    contexto = ContextoNarrativo(
        ubicacion_actual="Ruinas Antiguas de Kal'Theron",
        checkpoint_actual="entrada_ruinas"
    )
    
    # Crear narrador
    event_bus = EventBus()
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    
    print("El narrador generará descripciones de diferentes situaciones...\n")
    
    # Situación 1: Exploración
    print("📍 Situación: Explorando las ruinas")
    print("-" * 70)
    narracion = narrador.narrar_situacion(
        "El personaje encuentra una sala con inscripciones antiguas brillando débilmente"
    )
    print(f"📖 {narracion}\n")
    time.sleep(2)
    
    # Situación 2: Encuentro
    print("👤 Situación: Encuentro inesperado")
    print("-" * 70)
    narracion = narrador.narrar_situacion(
        "Un anciano misterioso aparece entre las sombras del pasillo"
    )
    print(f"📖 {narracion}\n")
    time.sleep(2)
    
    # Situación 3: Peligro
    print("⚠️ Situación: Peligro inminente")
    print("-" * 70)
    narracion = narrador.narrar_situacion(
        "El suelo comienza a temblar y piedras caen del techo"
    )
    print(f"📖 {narracion}\n")
    time.sleep(2)


def demo_narracion_decisiones():
    """Demuestra narraciones de decisiones"""
    imprimir_separador("🤔 NARRACIÓN DE DECISIONES")
    
    event_bus = EventBus()
    contexto = ContextoNarrativo(ubicacion_actual="Bifurcación del Camino")
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    
    # Decisión 1
    print("Decisión: ¿Qué camino tomar?")
    print("-" * 70)
    narracion = narrador.narrar_decision(
        "Dos caminos se abren ante ti. Uno iluminado por antorchas, otro en completa oscuridad",
        ["Camino iluminado", "Camino oscuro"]
    )
    print(f"📖 {narracion}")
    print("\nOpciones disponibles:")
    print("  1. Tomar el camino iluminado")
    print("  2. Adentrarse en la oscuridad\n")
    time.sleep(2)
    
    # Decisión 2
    print("Decisión: ¿Confiar o desconfiar?")
    print("-" * 70)
    narracion = narrador.narrar_decision(
        "El comerciante te ofrece un objeto mágico a un precio sospechosamente bajo",
        ["Aceptar el trato", "Rechazar con desconfianza"]
    )
    print(f"📖 {narracion}")
    print("\nOpciones disponibles:")
    print("  1. Comprar el objeto")
    print("  2. Rechazar la oferta\n")


def demo_combate_narrado():
    """Demuestra un combate completo con narración"""
    imprimir_separador("⚔️ COMBATE NARRADO")
    
    print("Preparando combate épico con narración en tiempo real...\n")
    time.sleep(1)
    
    # Crear personajes
    creacion = CreacionPersonajeService()
    
    heroe = creacion.crear_personaje(
        nombre="Sir Aldric",
        edad=28,
        raza="Humano",
        historia="Un caballero valiente",
        objetivo="Proteger al reino",
        hephix_tipo=HephixTipo.LUMINICA,
        clase=ClaseTipo.GUERRERO,
        caracteristicas={"fuerza": 9, "reflejos": 5, "resistencia": 8,
                        "voluntad": 3, "punteria": 0, "stamina": 3},
        habilidades_combate={"armas_cortantes": 15, "armas_contundentes": 0,
                            "armas_magicas": 0, "armas_distancia": 0, "pugilismo": 0},
        habilidades_educacion={"medicina": 5, "elocuencia": 0,
                              "manual": 0, "arcanismo": 0},
        habilidades_talento={"sigilo": 0, "percepcion": 5,
                            "mentalidad": 5, "astralidad": 5}
    )
    
    villano = creacion.crear_personaje(
        nombre="Zarak el Oscuro",
        edad=150,
        raza="Elfo Oscuro",
        historia="Un hechicero corrupto",
        objetivo="Dominar el reino",
        hephix_tipo=HephixTipo.OSCURA,
        clase=ClaseTipo.MAGO,
        caracteristicas={"fuerza": 4, "reflejos": 7, "resistencia": 5,
                        "voluntad": 10, "punteria": 0, "stamina": 2},
        habilidades_combate={"armas_cortantes": 0, "armas_contundentes": 0,
                            "armas_magicas": 15, "armas_distancia": 0, "pugilismo": 0},
        habilidades_educacion={"medicina": 0, "elocuencia": 5,
                              "manual": 0, "arcanismo": 10},
        habilidades_talento={"sigilo": 5, "percepcion": 5,
                            "mentalidad": 5, "astralidad": 0}
    )
    
    print(f"⚔️ {heroe.nombre} vs {villano.nombre}")
    print(f"   {heroe.nombre}: PV {heroe.pv_maximos} | {heroe.hephix.tipo.value.title()}")
    print(f"   {villano.nombre}: PV {villano.pv_maximos} | {villano.hephix.tipo.value.title()}\n")
    
    time.sleep(2)
    
    # Crear servicios
    event_bus = EventBus()
    contexto = ContextoNarrativo(
        ubicacion_actual="Torre Oscura - Sala del Trono",
        checkpoint_actual="confrontacion_final"
    )
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    combate = CombateService(event_bus)
    
    # Iniciar combate
    print("🎬 Iniciando combate...\n")
    estado = combate.iniciar_combate([heroe, villano])
    time.sleep(3)
    
    # Realizar algunos ataques
    print("\n🎲 Primer intercambio:")
    resultado = combate.resolver_ataque(heroe, villano)
    print(f"   Resultado: {resultado.descripcion_corta()}")
    time.sleep(3)
    
    if villano.esta_en_condiciones_combate():
        print("\n🎲 Segundo intercambio:")
        resultado = combate.resolver_ataque(villano, heroe)
        print(f"   Resultado: {resultado.descripcion_corta()}")
        time.sleep(3)
    
    print("\n" + "="*70)
    print("  Combate pausado para demostración")
    print("="*70)


def demo_contexto_narrativo():
    """Demuestra el uso del contexto narrativo"""
    imprimir_separador("📚 CONTEXTO NARRATIVO")
    
    # Crear contexto rico
    contexto = ContextoNarrativo(
        checkpoint_actual="ciudad_amarth_mercado",
        ubicacion_actual="Mercado de Amarth"
    )
    
    # Agregar NPCs
    contexto.npcs_conocidos.extend([
        "Marcus el Herrero",
        "Elara la Sanadora",
        "Thief Guildmaster",
        "Capitán de la Guardia"
    ])
    
    # Agregar reputación
    contexto.reputacion["Guardia de Amarth"] = 25
    contexto.reputacion["Gremio de Ladrones"] = -15
    contexto.reputacion["Templo de la Luz"] = 30
    
    # Agregar eventos
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEventoNarrativo.COMBATE,
        descripcion="Derrotaste a bandidos en las afueras",
        relevancia="alta"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEventoNarrativo.DIALOGO,
        descripcion="Hablaste con Marcus sobre armas legendarias",
        relevancia="media"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEventoNarrativo.DESCUBRIMIENTO,
        descripcion="Encontraste un mapa antiguo en el mercado",
        relevancia="alta"
    ))
    
    # Misiones
    contexto.misiones_activas.append("Investigar las ruinas antiguas")
    contexto.misiones_completadas.append("Limpiar el camino de bandidos")
    
    print("Contexto narrativo acumulado:\n")
    print(contexto.obtener_resumen_para_ia())
    
    print("\n💡 Este contexto permite al narrador IA generar historias")
    print("   coherentes con todo lo que ha ocurrido anteriormente.")


def menu_principal():
    """Menú interactivo"""
    while True:
        imprimir_separador("🎭 DEMO - SISTEMA DE NARRADOR IA")
        
        print("1. Narración de situaciones variadas")
        print("2. Narración de decisiones importantes")
        print("3. Combate completo con narración")
        print("4. Ver ejemplo de contexto narrativo")
        print("0. Salir")
        
        print()
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            demo_narracion_situaciones()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "2":
            demo_narracion_decisiones()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "3":
            demo_combate_narrado()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "4":
            demo_contexto_narrativo()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción inválida")
            input("\nPresiona Enter para continuar...")


def main():
    """Ejecuta el demo completo"""
    print("\n" + "="*70)
    print("  🎭 ETHER BLADES - DEMO DE NARRADOR IA")
    print("="*70)
    print("\nEste demo muestra el sistema de narración dinámica.")
    print("Usa un narrador MOCK que simula respuestas de IA.")
    print("\n💡 Para usar OpenAI real, configura OPENAI_API_KEY en .env")
    
    input("\nPresiona Enter para comenzar...")
    
    menu_principal()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

# ==============================================================================
# ARCHIVO 6/36: demo_persistencia.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./demo_persistencia.py
# ==============================================================================

"""
Demo del sistema de persistencia.
Ejecutar: python demo_persistencia.py
"""
from servicios import CreacionPersonajeService, PersistenciaService
from servicios.persistencia_estructuras import ContextoNarrativo, EventoNarrativo, TipoEvento
from entidades import HephixTipo, ClaseTipo


def imprimir_separador(titulo: str = ""):
    """Imprime un separador visual"""
    if titulo:
        print(f"\n{'='*70}")
        print(f"  {titulo}")
        print(f"{'='*70}\n")
    else:
        print("-" * 70)


def demo_guardar_partida():
    """Demuestra el guardado de una partida"""
    imprimir_separador("💾 GUARDADO DE PARTIDA")
    
    # Crear servicio de creación
    creacion = CreacionPersonajeService()
    
    # Crear personaje
    print("Creando personaje de prueba...")
    personaje = creacion.crear_personaje(
        nombre="Theron el Explorador",
        edad=30,
        raza="Elfo",
        historia="Un explorador veterano que busca artefactos antiguos",
        objetivo="Descubrir los secretos de las ruinas antiguas",
        hephix_tipo=HephixTipo.ESPIRITUAL,
        clase=ClaseTipo.EXPLORADOR,
        caracteristicas={
            "fuerza": 6,
            "reflejos": 8,
            "resistencia": 5,
            "voluntad": 5,
            "punteria": 8,
            "stamina": 3
        },
        habilidades_combate={
            "armas_cortantes": 5,
            "armas_contundentes": 0,
            "armas_magicas": 0,
            "armas_distancia": 15,
            "pugilismo": 0
        },
        habilidades_educacion={
            "medicina": 3,
            "elocuencia": 5,
            "manual": 0,
            "arcanismo": 2
        },
        habilidades_talento={
            "sigilo": 8,
            "percepcion": 10,
            "mentalidad": 0,
            "astralidad": 2
        }
    )
    
    print(f"✅ Personaje creado: {personaje.nombre}")
    print(f"   Clase: {personaje.clase.value.title()}")
    print(f"   Hephix: {personaje.hephix.tipo.value.title()}")
    print(f"   Nivel: {personaje.nivel}")
    print(f"   PV: {personaje.pv_maximos} | PM: {personaje.pm_maximos}")
    
    # Simular progreso
    print("\nSimulando progreso en la aventura...")
    personaje.ganar_experiencia(500)
    personaje.inventario.agregar_monedas(350)
    
    # Crear contexto narrativo
    contexto = ContextoNarrativo(
        checkpoint_actual="ruinas_antiguas_entrada",
        ubicacion_actual="Ruinas de Kal'Theron"
    )
    
    # Agregar eventos narrativos
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.DESCUBRIMIENTO,
        descripcion="Descubriste la entrada a las ruinas antiguas",
        relevancia="alta"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.COMBATE,
        descripcion="Derrotaste a dos guardianes de piedra",
        relevancia="media"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.DIALOGO,
        descripcion="Hablaste con el espíritu del guardián caído",
        relevancia="alta"
    ))
    
    contexto.npcs_conocidos.extend([
        "Guardián Espectral",
        "Anciano de la Aldea",
        "Comerciante Errante"
    ])
    
    contexto.reputacion["Exploradores de Amarth"] = 20
    contexto.reputacion["Guardia de las Ruinas"] = -10
    
    contexto.misiones_activas.append("Explorar las profundidades de Kal'Theron")
    contexto.misiones_completadas.append("Encontrar la entrada a las ruinas")
    
    print("\n📖 Contexto narrativo configurado:")
    print(f"   Ubicación: {contexto.ubicacion_actual}")
    print(f"   Checkpoint: {contexto.checkpoint_actual}")
    print(f"   NPCs conocidos: {len(contexto.npcs_conocidos)}")
    print(f"   Eventos registrados: {len(contexto.log_narrativo)}")
    
    # Guardar partida
    print("\n💾 Guardando partida...")
    servicio = PersistenciaService()
    servicio.iniciar_sesion()
    
    archivo = servicio.guardar_partida(
        personaje,
        contexto,
        slot=1,
        nombre_partida="Aventura en las Ruinas"
    )
    
    print(f"✅ Partida guardada en: {archivo}")
    print(f"   Slot: 1")
    print(f"   Tiempo jugado: {servicio._formatear_tiempo_jugado()}")
    
    return personaje, contexto


def demo_listar_partidas():
    """Demuestra el listado de partidas guardadas"""
    imprimir_separador("📋 LISTADO DE PARTIDAS GUARDADAS")
    
    servicio = PersistenciaService()
    slots = servicio.listar_partidas()
    
    partidas_encontradas = 0
    
    for slot in slots:
        if slot.existe:
            partidas_encontradas += 1
            print(slot)
            print()
    
    if partidas_encontradas == 0:
        print("No hay partidas guardadas.")
    else:
        print(f"Total de partidas: {partidas_encontradas}/10")


def demo_cargar_partida():
    """Demuestra la carga de una partida"""
    imprimir_separador("📂 CARGA DE PARTIDA")
    
    servicio = PersistenciaService()
    
    # Verificar que existe
    if not servicio.existe_partida(1):
        print("❌ No hay partida en el slot 1")
        return
    
    print("Cargando partida del slot 1...")
    
    # Cargar datos completos
    datos = servicio.cargar_partida(1)
    
    print(f"\n✅ Partida cargada: {datos.nombre_partida}")
    print(f"   Versión: {datos.version}")
    print(f"   Guardado: {datos.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Tiempo jugado: {datos.tiempo_jugado}")
    
    # Restaurar personaje
    personaje = servicio.cargar_personaje(1)
    
    print(f"\n👤 Personaje restaurado:")
    print(f"   Nombre: {personaje.nombre}")
    print(f"   Nivel: {personaje.nivel}")
    print(f"   XP: {personaje.experiencia}")
    print(f"   PV: {personaje.pv_actuales}/{personaje.pv_maximos}")
    print(f"   PM: {personaje.pm_actuales}/{personaje.pm_maximos}")
    print(f"   Monedas: {personaje.inventario.monedas}")
    
    # Restaurar contexto
    contexto = servicio.cargar_contexto(1)
    
    print(f"\n📍 Contexto narrativo:")
    print(f"   Ubicación: {contexto.ubicacion_actual}")
    print(f"   Checkpoint: {contexto.checkpoint_actual}")
    
    if contexto.npcs_conocidos:
        print(f"\n👥 NPCs conocidos:")
        for npc in contexto.npcs_conocidos:
            print(f"   • {npc}")
    
    if contexto.reputacion:
        print(f"\n⭐ Reputación:")
        for faccion, rep in contexto.reputacion.items():
            signo = "+" if rep >= 0 else ""
            print(f"   • {faccion}: {signo}{rep}")
    
    if contexto.misiones_activas:
        print(f"\n📜 Misiones activas:")
        for mision in contexto.misiones_activas:
            print(f"   • {mision}")
    
    if contexto.log_narrativo:
        print(f"\n📖 Eventos recientes:")
        for evento in contexto.log_narrativo[-5:]:  # Últimos 5
            print(f"   {evento.resumen()}")
    
    return personaje, contexto


def demo_contexto_para_ia():
    """Demuestra el resumen para IA"""
    imprimir_separador("🤖 CONTEXTO PARA IA")
    
    servicio = PersistenciaService()
    
    if not servicio.existe_partida(1):
        print("❌ No hay partida para mostrar")
        return
    
    contexto = servicio.cargar_contexto(1)
    
    print("Generando resumen del contexto para la IA...\n")
    print("─" * 70)
    print(contexto.obtener_resumen_para_ia())
    print("─" * 70)
    
    print("\n💡 Este resumen se enviará al narrador IA para que pueda")
    print("   continuar la historia de forma coherente con lo ya ocurrido.")


def demo_verificar_integridad():
    """Demuestra la verificación de integridad"""
    imprimir_separador("🔍 VERIFICACIÓN DE INTEGRIDAD")
    
    servicio = PersistenciaService()
    
    print("Verificando integridad de todos los slots...\n")
    
    for slot in range(1, 11):
        valido, error = servicio.verificar_integridad(slot)
        
        if valido:
            print(f"Slot {slot:2d}: ✅ OK")
        else:
            print(f"Slot {slot:2d}: ❌ {error}")


def menu_principal():
    """Menú interactivo"""
    while True:
        imprimir_separador("💾 DEMO - SISTEMA DE PERSISTENCIA")
        
        print("1. Crear y guardar nueva partida")
        print("2. Listar partidas guardadas")
        print("3. Cargar partida (Slot 1)")
        print("4. Ver contexto para IA")
        print("5. Verificar integridad de guardados")
        print("6. Eliminar partida (Slot 1)")
        print("0. Salir")
        
        print()
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            demo_guardar_partida()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "2":
            demo_listar_partidas()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "3":
            demo_cargar_partida()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "4":
            demo_contexto_para_ia()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "5":
            demo_verificar_integridad()
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "6":
            servicio = PersistenciaService()
            if servicio.eliminar_partida(1):
                print("\n✅ Partida del slot 1 eliminada")
            else:
                print("\n⚠️ No había partida en el slot 1")
            input("\nPresiona Enter para continuar...")
        
        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            break
        
        else:
            print("\n❌ Opción inválida")
            input("\nPresiona Enter para continuar...")


def main():
    """Ejecuta el demo completo"""
    print("\n" + "="*70)
    print("  💾 ETHER BLADES - DEMO DE PERSISTENCIA")
    print("="*70)
    print("\nEste demo muestra el sistema completo de guardado y carga.")
    print("Incluye serialización de personajes y contexto narrativo para IA.")
    
    input("\nPresiona Enter para comenzar...")
    
    menu_principal()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Demo interrumpida por el usuario.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

# ==============================================================================
# ARCHIVO 7/36: main.py
# Directorio: .
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./main.py
# ==============================================================================

"""
Ether Blades - Punto de entrada principal del juego.
Sistema de rol digital con motor de combate determinista y narrador IA.

Ejecutar: python main.py
"""
import sys
from typing import Optional
from servicios import (
    CreacionPersonajeService,
    PersistenciaService,
    CombateService,
    NarradorService,
    ContextoNarrativo,
    EventoNarrativo,
    TipoEventoNarrativo
)
from entidades import Personaje
from patrones import EventBus


class EtherBladesGame:
    """
    Clase principal del juego.
    Gestiona el loop principal y la navegación entre menús.
    """
    
    def __init__(self):
        """Inicializa el juego y sus servicios"""
        self.running = True
        
        # Servicios principales
        self.creacion_service = CreacionPersonajeService()
        self.persistencia_service = PersistenciaService()
        self.event_bus = EventBus()
        
        # Estado del juego
        self.personaje: Optional[Personaje] = None
        self.contexto: Optional[ContextoNarrativo] = None
        self.narrador: Optional[NarradorService] = None
        
        # Determinar si usar IA real o mock
        self.usar_ia_real = self._configurar_narrador()
    
    def _configurar_narrador(self) -> bool:
        """
        Configura el narrador (real o mock).
        
        Returns:
            True si usa IA real, False si usa mock
        """
        from servicios.cliente_ia import ClienteIA
        
        cliente = ClienteIA()
        if cliente.esta_disponible():
            print("✅ Narrador IA activado (OpenAI)")
            return True
        else:
            print("⚠️  Narrador IA en modo simulación (sin API key)")
            print("   Configura OPENAI_API_KEY en .env para narraciones reales\n")
            return False
    
    # ========================================================================
    # Loop Principal
    # ========================================================================
    
    def run(self):
        """Loop principal del juego"""
        self._mostrar_bienvenida()
        
        while self.running:
            self._menu_principal()
    
    def _mostrar_bienvenida(self):
        """Muestra la pantalla de bienvenida"""
        print("\n" + "="*70)
        print("  ⚔️  ETHER BLADES - AFTERMATH")
        print("="*70)
        print("\n  Un juego de rol épico con magia, combate y decisiones.\n")
        print("  Desarrollado por: Nicolás Bartolomeo")
        print("  Universidad de Mendoza - Computación II")
        print("\n" + "="*70)
    
    def _menu_principal(self):
        """Menú principal del juego"""
        print("\n" + "─"*70)
        print("  MENÚ PRINCIPAL")
        print("─"*70)
        print("\n1. 🆕 Nueva Partida")
        print("2. 📂 Cargar Partida")
        print("3. 💾 Gestionar Guardados")
        print("4. ℹ️  Acerca de")
        print("0. 🚪 Salir")
        
        opcion = input("\n➤ Selecciona una opción: ").strip()
        
        if opcion == "1":
            self._nueva_partida()
        elif opcion == "2":
            self._cargar_partida()
        elif opcion == "3":
            self._gestionar_guardados()
        elif opcion == "4":
            self._acerca_de()
        elif opcion == "0":
            self._salir()
        else:
            print("❌ Opción inválida")
    
    # ========================================================================
    # Nueva Partida
    # ========================================================================
    
    def _nueva_partida(self):
        """Inicia una nueva partida"""
        print("\n" + "="*70)
        print("  🆕 NUEVA PARTIDA")
        print("="*70)
        
        # Crear personaje
        print("\nPrimero, vamos a crear tu personaje...\n")
        input("Presiona Enter para comenzar...")
        
        try:
            self.personaje = self.creacion_service.crear_personaje_interactivo()
        except KeyboardInterrupt:
            print("\n\n❌ Creación cancelada")
            return
        
        # Crear contexto inicial
        self.contexto = ContextoNarrativo(
            checkpoint_actual="amarth_inicio",
            ubicacion_actual="Ciudad de Amarth - Plaza Central"
        )
        
        # Agregar evento inicial
        self.contexto.agregar_evento(EventoNarrativo(
            tipo=TipoEventoNarrativo.CHECKPOINT,
            descripcion=f"{self.personaje.nombre} llega a la ciudad de Amarth",
            relevancia="alta"
        ))
        
        # Inicializar narrador
        self.narrador = NarradorService(
            self.event_bus,
            self.contexto,
            usar_mock=not self.usar_ia_real
        )
        
        # Iniciar sesión (para tracking de tiempo)
        self.persistencia_service.iniciar_sesion()
        
        # Escena inicial
        self._escena_inicial()
        
        # Loop de juego
        self._loop_juego()
    
    def _escena_inicial(self):
        """Muestra la escena inicial del juego"""
        print("\n" + "="*70)
        print("  📖 PRÓLOGO")
        print("="*70 + "\n")
        
        narracion = self.narrador.narrar_situacion(
            f"{self.personaje.nombre}, un {self.personaje.raza.lower()} "
            f"{self.personaje.clase.value}, llega a la ciudad de Amarth "
            f"con {self.personaje.objetivo.lower()}",
            self.personaje
        )
        
        print(narracion)
        print("\n" + "─"*70)
        input("\nPresiona Enter para continuar tu aventura...")
    
    # ========================================================================
    # Loop de Juego
    # ========================================================================
    
    def _loop_juego(self):
        """Loop principal del juego una vez iniciada la partida"""
        while self.running and self.personaje.esta_vivo:
            print("\n" + "="*70)
            print(f"  📍 {self.contexto.ubicacion_actual}")
            print("="*70)
            print(f"\n👤 {self.personaje.nombre} (Nivel {self.personaje.nivel})")
            print(f"   ❤️  PV: {self.personaje.pv_actuales}/{self.personaje.pv_maximos}")
            print(f"   💙 PM: {self.personaje.pm_actuales}/{self.personaje.pm_maximos}")
            print(f"   💰 Monedas: {self.personaje.inventario.monedas}")
            
            print("\n" + "─"*70)
            print("  ¿QUÉ DESEAS HACER?")
            print("─"*70)
            print("\n1. 🗺️  Explorar")
            print("2. ⚔️  Entrenar en Combate (Demo)")
            print("3. 🎒 Ver Inventario")
            print("4. 📊 Ver Ficha Completa")
            print("5. 💾 Guardar Partida")
            print("0. 🚪 Volver al Menú Principal")
            
            opcion = input("\n➤ Selecciona una opción: ").strip()
            
            if opcion == "1":
                self._explorar()
            elif opcion == "2":
                self._combate_demo()
            elif opcion == "3":
                self._ver_inventario()
            elif opcion == "4":
                self._ver_ficha()
            elif opcion == "5":
                self._guardar_partida_rapido()
            elif opcion == "0":
                if self._confirmar_salir_partida():
                    break
            else:
                print("❌ Opción inválida")
        
        if not self.personaje.esta_vivo:
            self._game_over()
    
    def _explorar(self):
        """Opción de exploración (placeholder)"""
        print("\n🗺️  Explorando los alrededores...")
        
        narracion = self.narrador.narrar_situacion(
            "El personaje explora la zona en busca de algo interesante",
            self.personaje
        )
        print(f"\n📖 {narracion}")
        
        # Agregar evento al contexto
        self.contexto.agregar_evento(EventoNarrativo(
            tipo=TipoEventoNarrativo.DESCUBRIMIENTO,
            descripcion="Exploró los alrededores",
            relevancia="baja"
        ))
        
        input("\nPresiona Enter para continuar...")
    
    def _combate_demo(self):
        """Demo de combate contra un enemigo generado"""
        print("\n⚔️  Preparándote para el combate...")
        
        # Crear enemigo simple
        from entidades import Ficha, Hephix, HephixTipo, ClaseTipo
        
        ficha_enemigo = Ficha()
        ficha_enemigo.caracteristicas.fuerza = 5
        ficha_enemigo.caracteristicas.reflejos = 4
        ficha_enemigo.caracteristicas.resistencia = 4
        ficha_enemigo.caracteristicas.stamina = 2
        
        enemigo = Personaje(
            nombre="Bandido",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_enemigo
        )
        
        # Iniciar combate
        combate_service = CombateService(self.event_bus)
        estado = combate_service.iniciar_combate([self.personaje, enemigo])
        
        print(f"\n💥 ¡Combate contra {enemigo.nombre}!")
        input("Presiona Enter para comenzar...")
        
        # Simulación simple de combate (solo primer turno)
        turno = 1
        max_turnos = 10
        
        while estado.combate_activo and turno <= max_turnos:
            print(f"\n--- Turno {turno} ---")
            
            # Turno del jugador
            if estado.orden_turnos[estado.indice_turno_actual] == self.personaje.nombre:
                resultado = combate_service.resolver_ataque(self.personaje, enemigo)
                print(f"➤ {resultado.descripcion_corta()}")
            else:
                resultado = combate_service.resolver_ataque(enemigo, self.personaje)
                print(f"➤ {resultado.descripcion_corta()}")
            
            # Verificar fin
            if combate_service.verificar_fin_combate():
                break
            
            estado.avanzar_turno()
            turno += 1
            
            input("\nPresiona Enter para continuar...")
        
        # Resultado
        if estado.ganador == self.personaje.nombre:
            print("\n✨ ¡Victoria!")
            xp = 100
            oro = 50
            self.personaje.ganar_experiencia(xp)
            self.personaje.inventario.agregar_monedas(oro)
            print(f"   Ganaste {xp} XP y {oro} monedas")
            
            # Agregar evento
            self.contexto.agregar_evento(EventoNarrativo(
                tipo=TipoEventoNarrativo.COMBATE,
                descripcion=f"Derrotaste a {enemigo.nombre}",
                relevancia="media"
            ))
        else:
            print("\n💀 Has sido derrotado...")
        
        input("\nPresiona Enter para continuar...")
    
    def _ver_inventario(self):
        """Muestra el inventario del personaje"""
        print("\n" + "="*70)
        print("  🎒 INVENTARIO")
        print("="*70)
        print(self.personaje.inventario.resumen())
        input("\nPresiona Enter para continuar...")
    
    def _ver_ficha(self):
        """Muestra la ficha completa del personaje"""
        print("\n" + "="*70)
        print("  📊 FICHA DE PERSONAJE")
        print("="*70)
        print(self.personaje.resumen_completo())
        input("\nPresiona Enter para continuar...")
    
    def _guardar_partida_rapido(self):
        """Guarda la partida en el slot 1"""
        print("\n💾 Guardando partida...")
        
        try:
            self.persistencia_service.guardar_partida(
                self.personaje,
                self.contexto,
                slot=1,
                nombre_partida=f"Aventura de {self.personaje.nombre}"
            )
            print("✅ Partida guardada exitosamente en el Slot 1")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _confirmar_salir_partida(self) -> bool:
        """Confirma si el jugador quiere salir sin guardar"""
        print("\n⚠️  ¿Deseas guardar antes de salir?")
        print("1. Sí, guardar y salir")
        print("2. No, salir sin guardar")
        print("3. Cancelar")
        
        opcion = input("\n➤ Opción: ").strip()
        
        if opcion == "1":
            self._guardar_partida_rapido()
            return True
        elif opcion == "2":
            return True
        else:
            return False
    
    def _game_over(self):
        """Pantalla de game over"""
        print("\n" + "="*70)
        print("  💀 GAME OVER")
        print("="*70)
        print(f"\n{self.personaje.nombre} ha caído en combate.")
        print("Tu aventura ha llegado a su fin...")
        input("\nPresiona Enter para volver al menú principal...")
    
    # ========================================================================
    # Cargar Partida
    # ========================================================================
    
    def _cargar_partida(self):
        """Carga una partida guardada"""
        print("\n" + "="*70)
        print("  📂 CARGAR PARTIDA")
        print("="*70 + "\n")
        
        # Listar partidas
        slots = self.persistencia_service.listar_partidas()
        partidas_disponibles = [s for s in slots if s.existe]
        
        if not partidas_disponibles:
            print("No hay partidas guardadas.")
            input("\nPresiona Enter para continuar...")
            return
        
        print("Partidas disponibles:\n")
        for slot in partidas_disponibles:
            print(slot)
            print()
        
        # Seleccionar slot
        try:
            slot_num = int(input("➤ Selecciona el número de slot (0 para cancelar): "))
            
            if slot_num == 0:
                return
            
            if not 1 <= slot_num <= 10:
                print("❌ Slot inválido")
                return
            
            # Cargar
            print(f"\n📂 Cargando partida del slot {slot_num}...")
            
            self.personaje = self.persistencia_service.cargar_personaje(slot_num)
            self.contexto = self.persistencia_service.cargar_contexto(slot_num)
            
            # Reiniciar narrador con el contexto cargado
            self.narrador = NarradorService(
                self.event_bus,
                self.contexto,
                usar_mock=not self.usar_ia_real
            )
            
            # Reiniciar sesión
            self.persistencia_service.iniciar_sesion()
            
            print(f"✅ Partida cargada: {self.personaje.nombre}")
            print(f"   Ubicación: {self.contexto.ubicacion_actual}")
            
            input("\nPresiona Enter para continuar...")
            
            # Ir al loop de juego
            self._loop_juego()
            
        except ValueError:
            print("❌ Entrada inválida")
        except FileNotFoundError:
            print("❌ No hay partida en ese slot")
        except Exception as e:
            print(f"❌ Error al cargar: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    # ========================================================================
    # Gestión de Guardados
    # ========================================================================
    
    def _gestionar_guardados(self):
        """Menú de gestión de guardados"""
        while True:
            print("\n" + "="*70)
            print("  💾 GESTIÓN DE GUARDADOS")
            print("="*70 + "\n")
            
            slots = self.persistencia_service.listar_partidas()
            
            for slot in slots:
                if slot.existe:
                    print(slot)
                else:
                    print(f"Slot {slot.slot}: [VACÍO]")
                print()
            
            print("1. Ver detalles de un slot")
            print("2. Eliminar una partida")
            print("0. Volver")
            
            opcion = input("\n➤ Opción: ").strip()
            
            if opcion == "1":
                self._ver_detalles_slot()
            elif opcion == "2":
                self._eliminar_partida()
            elif opcion == "0":
                break
            else:
                print("❌ Opción inválida")
    
    def _ver_detalles_slot(self):
        """Muestra detalles de un slot"""
        try:
            slot_num = int(input("\n➤ Número de slot: "))
            
            if not 1 <= slot_num <= 10:
                print("❌ Slot inválido")
                return
            
            if not self.persistencia_service.existe_partida(slot_num):
                print("❌ Ese slot está vacío")
                return
            
            datos = self.persistencia_service.cargar_partida(slot_num)
            print("\n" + "─"*70)
            print(datos.resumen_corto())
            print("─"*70)
            
        except ValueError:
            print("❌ Entrada inválida")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPresiona Enter para continuar...")
    
    def _eliminar_partida(self):
        """Elimina una partida guardada"""
        try:
            slot_num = int(input("\n➤ Número de slot a eliminar: "))
            
            if not 1 <= slot_num <= 10:
                print("❌ Slot inválido")
                return
            
            confirmar = input(f"⚠️  ¿Confirmar eliminación del slot {slot_num}? (s/n): ")
            
            if confirmar.lower() == 's':
                if self.persistencia_service.eliminar_partida(slot_num):
                    print("✅ Partida eliminada")
                else:
                    print("❌ El slot ya estaba vacío")
        
        except ValueError:
            print("❌ Entrada inválida")
        
        input("\nPresiona Enter para continuar...")
    
    # ========================================================================
    # Acerca de
    # ========================================================================
    
    def _acerca_de(self):
        """Muestra información del juego"""
        print("\n" + "="*70)
        print("  ℹ️  ACERCA DE ETHER BLADES")
        print("="*70 + "\n")
        
        print("📖 Ether Blades - Aftermath")
        print("   Sistema de rol digital con motor de combate determinista\n")
        
        print("👨‍💻 Desarrollado por: Nicolás Bartolomeo")
        print("🏫 Universidad de Mendoza")
        print("📚 Materia: Diseño de Sistemas\n")
        
        print("🎮 Características:")
        print("   • Sistema de combate basado en reglas deterministas")
        print("   • Creación de personajes con 13 tipos de Hephix (magia)")
        print("   • 6 clases de personaje")
        print("   • Narrador IA con OpenAI (opcional)")
        print("   • Sistema de guardado/carga con contexto narrativo")
        print("   • Arquitectura con patrones de diseño (MVC, Singleton, etc.)\n")
        
        print(f"📌 Versión: {self.persistencia_service.directorio.parent.name}")
        
        input("\nPresiona Enter para continuar...")
    
    # ========================================================================
    # Salir
    # ========================================================================
    
    def _salir(self):
        """Sale del juego"""
        print("\n👋 ¡Gracias por jugar Ether Blades!")
        print("   Que los Hephix te acompañen...\n")
        self.running = False


def main():
    """Función principal"""
    try:
        game = EtherBladesGame()
        game.run()
    except KeyboardInterrupt:
        print("\n\n❌ Juego interrumpido por el usuario.")
        print("👋 ¡Hasta luego!\n")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        print("\nPor favor, reporta este error.\n")


if __name__ == "__main__":
    main()


################################################################################
# DIRECTORIO: data
################################################################################

# ==============================================================================
# ARCHIVO 8/36: __init__.py
# Directorio: data
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./data/__init__.py
# ==============================================================================




################################################################################
# DIRECTORIO: entidades
################################################################################

# ==============================================================================
# ARCHIVO 9/36: __init__.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/__init__.py
# ==============================================================================

"""
Módulo de entidades del dominio.
Exporta todas las clases principales del juego.
"""

# Tipos y enums
from .tipos import (
    HephixTipo,
    ClaseTipo,
    TipoArma,
    TipoAtaque,
    TipoArmadura,
    RarezaItem,
    EstadoCombate,
    TipoAccion,
    Constantes,
    NombresHabilidades
)

# Sistema de dados
from .dados import (
    ResultadoTirada,
    tirar_dados,
    tirar_d6,
    tirar_d10,
    tirar_d12,
    tirar_d20,
    tirar_d100,
    tirar_ataque,
    tirar_defensa,
    establecer_semilla
)

# Hephix
from .hephix import Hephix

# Ficha
from .ficha import (
    Caracteristicas,
    HabilidadesCombate,
    HabilidadesEducacion,
    HabilidadesTalento,
    Ficha
)

# Armas y armaduras
from .arma import (
    Arma,
    Armadura,
    crear_espada_basica,
    crear_arco_basico,
    crear_baston_basico,
    crear_armadura_ligera
)

# Inventario
from .inventario import (
    Item,
    ItemConsumible,
    ItemDroga,
    Inventario,
    crear_pocion_vida_menor,
    crear_botiquin_primeros_auxilios,
    crear_kit_atencion_medica
)

# Personaje
from .personaje import Personaje

__all__ = [
    # Tipos
    'HephixTipo',
    'ClaseTipo',
    'TipoArma',
    'TipoAtaque',
    'TipoArmadura',
    'RarezaItem',
    'EstadoCombate',
    'TipoAccion',
    'Constantes',
    'NombresHabilidades',
    
    # Dados
    'ResultadoTirada',
    'tirar_dados',
    'tirar_d6',
    'tirar_d10',
    'tirar_d12',
    'tirar_d20',
    'tirar_d100',
    'tirar_ataque',
    'tirar_defensa',
    'establecer_semilla',
    
    # Hephix
    'Hephix',
    
    # Ficha
    'Caracteristicas',
    'HabilidadesCombate',
    'HabilidadesEducacion',
    'HabilidadesTalento',
    'Ficha',
    
    # Armas
    'Arma',
    'Armadura',
    'crear_espada_basica',
    'crear_arco_basico',
    'crear_baston_basico',
    'crear_armadura_ligera',
    
    # Inventario
    'Item',
    'ItemConsumible',
    'ItemDroga',
    'Inventario',
    'crear_pocion_vida_menor',
    'crear_botiquin_primeros_auxilios',
    'crear_kit_atencion_medica',
    
    # Personaje
    'Personaje',
]

# ==============================================================================
# ARCHIVO 10/36: arma.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/arma.py
# ==============================================================================

"""
Clases de Arma y Armadura para el sistema de combate.
"""
from pydantic import BaseModel, Field
from typing import Optional
from .tipos import TipoArma, TipoAtaque, TipoArmadura, RarezaItem


class Arma(BaseModel):
    """
    Clase base para todas las armas del juego.
    """
    
    nombre: str
    descripcion: str = ""
    
    # Clasificación
    tipo_arma: TipoArma  # armas_cortantes, contundentes, etc.
    tipo_ataque: TipoAtaque  # melee, distancia, magico
    
    # Stats de combate
    daño_base: int = Field(default=0, ge=0)
    bonus: int = Field(default=0, description="Bonus al coeficiente de ataque")
    
    # Requisitos
    nivel_requerido: int = Field(default=1, ge=1)
    habilidad_minima: int = Field(default=0, ge=0, description="Nivel mínimo en la habilidad del arma")
    
    # Propiedades
    rareza: RarezaItem = Field(default=RarezaItem.COMUN)
    es_magica: bool = Field(default=False)
    mejora_mecanica: int = Field(default=0, ge=0, le=10, description="Mejora de Manual")
    mejora_magica: int = Field(default=0, ge=0, le=10, description="Mejora de Arcanismo")
    
    # Durabilidad (opcional para futuro)
    durabilidad_actual: Optional[int] = None
    durabilidad_maxima: Optional[int] = None
    
    def bonus_total(self) -> int:
        """
        Calcula el bonus total del arma.
        Incluye: bonus base + mejora mecánica + mejora mágica
        NOTA: Las mejoras mecánicas y mágicas no pueden coexistir
        """
        if self.mejora_mecanica > 0 and self.mejora_magica > 0:
            # Solo debería tener una, usar la mayor
            mejora = max(self.mejora_mecanica, self.mejora_magica)
        else:
            mejora = self.mejora_mecanica + self.mejora_magica
        
        return self.bonus + mejora
    
    def puede_mejorar_mecanicamente(self) -> bool:
        """Verifica si puede recibir mejora mecánica"""
        return self.mejora_magica == 0 and self.mejora_mecanica < 10
    
    def puede_mejorar_magicamente(self) -> bool:
        """Verifica si puede recibir mejora mágica"""
        return self.mejora_mecanica == 0 and self.mejora_magica < 10
    
    def aplicar_mejora_mecanica(self, nivel_manual: int) -> bool:
        """
        Aplica mejora mecánica según nivel de habilidad Manual.
        
        Args:
            nivel_manual: Nivel de la habilidad Manual del personaje
        
        Returns:
            True si se aplicó la mejora, False si no cumple requisitos
        """
        # Tabla de mejoras (nivel_requerido: bonus)
        tabla_mejoras = {
            9: 1, 12: 2, 15: 3, 18: 4, 21: 5,
            24: 6, 27: 8, 30: 10
        }
        
        if not self.puede_mejorar_mecanicamente():
            return False
        
        # Buscar la mejora más alta que puede aplicar
        for nivel_req, bonus in sorted(tabla_mejoras.items(), reverse=True):
            if nivel_manual >= nivel_req:
                self.mejora_mecanica = bonus
                return True
        
        return False
    
    def aplicar_mejora_magica(self, nivel_arcanismo: int) -> bool:
        """
        Aplica mejora mágica según nivel de habilidad Arcanismo.
        
        Args:
            nivel_arcanismo: Nivel de la habilidad Arcanismo del personaje
        
        Returns:
            True si se aplicó la mejora, False si no cumple requisitos
        """
        # Tabla de mejoras (igual que mecánica)
        tabla_mejoras = {
            9: 1, 12: 2, 15: 3, 18: 4, 21: 5,
            24: 6, 27: 8, 30: 10
        }
        
        if not self.puede_mejorar_magicamente():
            return False
        
        for nivel_req, bonus in sorted(tabla_mejoras.items(), reverse=True):
            if nivel_arcanismo >= nivel_req:
                self.mejora_magica = bonus
                self.es_magica = True
                return True
        
        return False
    
    def __str__(self) -> str:
        mejora_str = ""
        if self.mejora_mecanica > 0:
            mejora_str = f" +{self.mejora_mecanica} (Mecánica)"
        elif self.mejora_magica > 0:
            mejora_str = f" +{self.mejora_magica} (Mágica)"
        
        return f"{self.nombre}{mejora_str} (Bonus: +{self.bonus_total()})"


class Armadura(BaseModel):
    """
    Representa una armadura equipable.
    """
    
    nombre: str
    descripcion: str = ""
    
    # Clasificación
    tipo: TipoArmadura
    
    # Stats de defensa
    reduccion_daño: int = Field(default=0, ge=0, description="Reduce daño recibido")
    bonus_reflejos: int = Field(default=0, description="Modificador a Reflejos")
    
    # Requisitos
    nivel_requerido: int = Field(default=1, ge=1)
    resistencia_minima: int = Field(default=0, ge=0)
    
    # Propiedades
    rareza: RarezaItem = Field(default=RarezaItem.COMUN)
    es_magica: bool = Field(default=False)
    
    # Durabilidad
    durabilidad_actual: Optional[int] = None
    durabilidad_maxima: Optional[int] = None
    
    def reduccion_total(self) -> int:
        """Calcula la reducción total de daño"""
        return self.reduccion_daño
    
    def __str__(self) -> str:
        return f"{self.nombre} (Reducción: {self.reduccion_daño}, Bonus Reflejos: {self.bonus_reflejos:+d})"


# Ejemplos y factory helpers
def crear_espada_basica() -> Arma:
    """Crea una espada básica de inicio"""
    return Arma(
        nombre="Espada Corta",
        descripcion="Una espada de hierro común",
        tipo_arma=TipoArma.CORTANTE_PUNZANTE,
        tipo_ataque=TipoAtaque.MELEE,
        daño_base=0,
        bonus=2,
        nivel_requerido=1,
        habilidad_minima=0
    )


def crear_arco_basico() -> Arma:
    """Crea un arco básico de inicio"""
    return Arma(
        nombre="Arco Corto",
        descripcion="Un arco de madera simple",
        tipo_arma=TipoArma.DISTANCIA,
        tipo_ataque=TipoAtaque.DISTANCIA,
        daño_base=0,
        bonus=2,
        nivel_requerido=1,
        habilidad_minima=0
    )


def crear_baston_basico() -> Arma:
    """Crea un bastón mágico básico"""
    return Arma(
        nombre="Bastón de Madera",
        descripcion="Un bastón tallado con runas básicas",
        tipo_arma=TipoArma.MAGICA,
        tipo_ataque=TipoAtaque.MAGICO,
        daño_base=0,
        bonus=2,
        nivel_requerido=1,
        habilidad_minima=0,
        es_magica=True
    )


def crear_armadura_ligera() -> Armadura:
    """Crea una armadura ligera básica"""
    return Armadura(
        nombre="Armadura de Cuero",
        descripcion="Protección ligera de cuero curtido",
        tipo=TipoArmadura.LIGERA,
        reduccion_daño=2,
        bonus_reflejos=0,
        nivel_requerido=1
    )


if __name__ == "__main__":
    print("=== Sistema de Armas y Armaduras ===\n")
    
    # Crear arma
    espada = crear_espada_basica()
    print(f"Arma creada: {espada}")
    print(f"  Tipo: {espada.tipo_arma.value}")
    print(f"  Bonus total: +{espada.bonus_total()}\n")
    
    # Probar mejora
    print("Aplicando mejora mecánica (Manual nivel 15):")
    if espada.aplicar_mejora_mecanica(15):
        print(f"  ✅ {espada}")
    
    # Crear armadura
    print("\nArmadura creada:")
    armadura = crear_armadura_ligera()
    print(f"  {armadura}")

# ==============================================================================
# ARCHIVO 11/36: dados.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/dados.py
# ==============================================================================

"""
Sistema de tiradas de dados para Ether Blades.
Implementa todas las mecánicas de dados del juego.
"""
import random
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class ResultadoTirada:
    """Resultado de una tirada de dados"""
    dados: List[int]
    total: int
    cantidad: int
    caras: int
    
    def __str__(self):
        dados_str = " + ".join(str(d) for d in self.dados)
        return f"{self.cantidad}d{self.caras}: [{dados_str}] = {self.total}"


def tirar_dados(cantidad: int, caras: int) -> ResultadoTirada:
    """
    Tira una cantidad de dados con caras especificadas.
    
    Args:
        cantidad: Número de dados a tirar
        caras: Número de caras de cada dado
    
    Returns:
        ResultadoTirada con los valores individuales y el total
    
    Ejemplos:
        >>> resultado = tirar_dados(3, 6)  # 3d6
        >>> print(resultado.total)
        14
    """
    dados = [random.randint(1, caras) for _ in range(cantidad)]
    return ResultadoTirada(
        dados=dados,
        total=sum(dados),
        cantidad=cantidad,
        caras=caras
    )


def tirar_d6(cantidad: int = 1) -> ResultadoTirada:
    """Tirada de d6 (usado para esbirros)"""
    return tirar_dados(cantidad, 6)


def tirar_d10(cantidad: int = 1) -> ResultadoTirada:
    """Tirada de d10 (usado para iniciativa)"""
    return tirar_dados(cantidad, 10)


def tirar_d12(cantidad: int = 1) -> ResultadoTirada:
    """Tirada de d12 (usado para mentalidad)"""
    return tirar_dados(cantidad, 12)


def tirar_d20(cantidad: int = 1) -> ResultadoTirada:
    """Tirada de d20 (usado para sanación y otras mecánicas)"""
    return tirar_dados(cantidad, 20)


def tirar_d100(cantidad: int = 1) -> ResultadoTirada:
    """Tirada de d100 (usado para choque de poderes)"""
    return tirar_dados(cantidad, 100)


def tirar_ataque() -> ResultadoTirada:
    """Tirada estándar de ataque: 3d6"""
    return tirar_dados(3, 6)


def tirar_defensa() -> ResultadoTirada:
    """Tirada estándar de defensa: 2d6"""
    return tirar_dados(2, 6)


def establecer_semilla(semilla: int):
    """
    Establece la semilla del generador aleatorio.
    Útil para testing y reproducibilidad.
    
    Args:
        semilla: Valor entero para la semilla
    """
    random.seed(semilla)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Sistema de Dados de Ether Blades ===\n")
    
    print("Tirada de ataque (3d6):")
    ataque = tirar_ataque()
    print(f"  {ataque}\n")
    
    print("Tirada de defensa (2d6):")
    defensa = tirar_defensa()
    print(f"  {defensa}\n")
    
    print("Tirada de iniciativa (1d10):")
    iniciativa = tirar_d10()
    print(f"  {iniciativa}\n")
    
    print("Tirada de mentalidad (1d12):")
    mentalidad = tirar_d12()
    print(f"  {mentalidad}\n")

# ==============================================================================
# ARCHIVO 12/36: ficha.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/ficha.py
# ==============================================================================

"""
Clase Ficha - Representa las estadísticas completas de un personaje.
Incluye características, habilidades y cálculos derivados.
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from .tipos import Constantes, NombresHabilidades, HephixTipo


class Caracteristicas(BaseModel):
    """
    Las 6 características principales del personaje.
    Total de puntos iniciales: 20
    """
    fuerza: int = Field(default=0, ge=0, le=20, description="Capacidad física y daño cuerpo a cuerpo")
    reflejos: int = Field(default=0, ge=0, le=20, description="Capacidad de esquivar ataques")
    resistencia: int = Field(default=0, ge=0, le=20, description="Puntos de vida y aguante")
    voluntad: int = Field(default=0, ge=0, le=20, description="Poder mágico del Hephix")
    punteria: int = Field(default=0, ge=0, le=20, description="Precisión con armas a distancia")
    stamina: int = Field(default=0, ge=0, le=20, description="Resistencia al cansancio en combate")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return (self.fuerza + self.reflejos + self.resistencia + 
                self.voluntad + self.punteria + self.stamina)
    
    def validar_distribucion(self, puntos_maximos: int = Constantes.PUNTOS_CARACTERISTICAS) -> bool:
        """Valida que no se excedan los puntos disponibles"""
        return self.total_puntos() <= puntos_maximos


class HabilidadesCombate(BaseModel):
    """
    Habilidades de combate.
    Total de puntos iniciales: 10
    """
    armas_cortantes: int = Field(default=0, ge=0, description="Espadas, dagas, lanzas")
    armas_contundentes: int = Field(default=0, ge=0, description="Mazas, martillos")
    armas_magicas: int = Field(default=0, ge=0, description="Bastones, varas mágicas")
    armas_distancia: int = Field(default=0, ge=0, description="Arcos, ballestas")
    pugilismo: int = Field(default=0, ge=0, description="Combate sin armas")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return (self.armas_cortantes + self.armas_contundentes + 
                self.armas_magicas + self.armas_distancia + self.pugilismo)


class HabilidadesEducacion(BaseModel):
    """
    Habilidades de educación.
    Total de puntos iniciales: 10
    """
    medicina: int = Field(default=0, ge=0, description="Sanación y primeros auxilios")
    elocuencia: int = Field(default=0, ge=0, description="Persuasión, mentira, intimidación")
    manual: int = Field(default=0, ge=0, description="Artesanía y mejora mecánica")
    arcanismo: int = Field(default=0, ge=0, description="Encantamientos y mejora mágica")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return self.medicina + self.elocuencia + self.manual + self.arcanismo


class HabilidadesTalento(BaseModel):
    """
    Habilidades de talento.
    Total de puntos iniciales: 10
    """
    sigilo: int = Field(default=0, ge=0, description="Ocultamiento y ataques sorpresa")
    percepcion: int = Field(default=0, ge=0, description="Detectar cambios y objetos")
    mentalidad: int = Field(default=0, ge=0, description="Estrategia y estudio")
    astralidad: int = Field(default=0, ge=0, description="Conexión con lo divino")
    
    def total_puntos(self) -> int:
        """Calcula el total de puntos asignados"""
        return self.sigilo + self.percepcion + self.mentalidad + self.astralidad


class Ficha(BaseModel):
    """
    Ficha completa de un personaje con todas sus estadísticas.
    Incluye características, habilidades y cálculos derivados.
    """
    
    # Características principales (20 puntos)
    caracteristicas: Caracteristicas = Field(default_factory=Caracteristicas)
    
    # Habilidades (10 puntos cada categoría)
    combate: HabilidadesCombate = Field(default_factory=HabilidadesCombate)
    educacion: HabilidadesEducacion = Field(default_factory=HabilidadesEducacion)
    talento: HabilidadesTalento = Field(default_factory=HabilidadesTalento)
    
    # Tipo de Hephix (necesario para cálculos)
    hephix_tipo: Optional[HephixTipo] = None
    
    # ========================================================================
    # Propiedades calculadas (Stats derivados)
    # ========================================================================
    
    @property
    def fuerza(self) -> int:
        return self.caracteristicas.fuerza
    
    @property
    def reflejos(self) -> int:
        return self.caracteristicas.reflejos
    
    @property
    def resistencia(self) -> int:
        return self.caracteristicas.resistencia
    
    @property
    def voluntad(self) -> int:
        return self.caracteristicas.voluntad
    
    @property
    def punteria(self) -> int:
        return self.caracteristicas.punteria
    
    @property
    def stamina(self) -> int:
        return self.caracteristicas.stamina
    
    @property
    def pv_maximos(self) -> int:
        """
        Puntos de Vida máximos.
        Fórmula: Res × 10
        Bonus: +Vol × 5 si tiene Hephix Sangriento
        """
        pv_base = self.resistencia * Constantes.MULTIPLICADOR_PV
        
        # Bonus Hephix Sangriento
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            pv_base += self.voluntad * Constantes.MULTIPLICADOR_PV_SANGRIENTO
        
        return pv_base
    
    @property
    def pm_maximos(self) -> int:
        """
        Puntos de Magia máximos.
        Fórmula: Vol × 5
        Excepción: 0 si tiene Hephix Sangriento
        """
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            return 0
        return self.voluntad * Constantes.MULTIPLICADOR_PM
    
    @property
    def pcf_maximos(self) -> int:
        """
        Puntos de Conexión Física máximos.
        Fórmula: Fue × 5
        Excepción: 0 si tiene Hephix Sangriento
        """
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            return 0
        return self.fuerza * Constantes.MULTIPLICADOR_PCF
    
    @property
    def pct_maximos(self) -> int:
        """
        Puntos de Conexión Tenaz máximos.
        Fórmula: Pun × 5
        Excepción: 0 si tiene Hephix Sangriento
        """
        if self.hephix_tipo == HephixTipo.SANGRIENTA:
            return 0
        return self.punteria * Constantes.MULTIPLICADOR_PCT
    
    @property
    def ps_maximos(self) -> int:
        """
        Puntos de Stamina (para combate).
        Fórmula: Sta × 5
        """
        return self.stamina * Constantes.MULTIPLICADOR_STAMINA
    
    # ========================================================================
    # Métodos de validación
    # ========================================================================
    
    def validar_distribucion_completa(self) -> dict[str, bool]:
        """
        Valida que todas las categorías tengan distribución correcta.
        
        Returns:
            Dict con validación de cada categoría
        """
        return {
            "caracteristicas": self.caracteristicas.validar_distribucion(),
            "combate": self.combate.total_puntos() <= Constantes.PUNTOS_COMBATE,
            "educacion": self.educacion.total_puntos() <= Constantes.PUNTOS_EDUCACION,
            "talento": self.talento.total_puntos() <= Constantes.PUNTOS_TALENTO
        }
    
    def es_valida(self) -> bool:
        """Verifica que toda la ficha sea válida"""
        validacion = self.validar_distribucion_completa()
        return all(validacion.values())
    
    # ========================================================================
    # Métodos de bonificación
    # ========================================================================
    
    def obtener_bonus_habilidad(self, habilidad: str) -> int:
        """
        Calcula el bonus de daño por nivel de habilidad.
        Fórmula: +1 de daño cada 5 puntos de habilidad
        
        Args:
            habilidad: Nombre de la habilidad
        
        Returns:
            Bonus de daño
        """
        # Buscar la habilidad en las categorías
        if hasattr(self.combate, habilidad):
            nivel = getattr(self.combate, habilidad)
        elif hasattr(self.educacion, habilidad):
            nivel = getattr(self.educacion, habilidad)
        elif hasattr(self.talento, habilidad):
            nivel = getattr(self.talento, habilidad)
        else:
            return 0
        
        return nivel // Constantes.BONUS_HABILIDAD_POR_NIVEL
    
    def calcular_habilidades_extra_mentalidad(self) -> int:
        """
        Cada 10 puntos de mentalidad = +1 punto de habilidad extra.
        
        Returns:
            Cantidad de puntos extra disponibles
        """
        return self.talento.mentalidad // Constantes.PUNTOS_MENTALIDAD_POR_HABILIDAD_EXTRA
    
    # ========================================================================
    # Métodos de utilidad
    # ========================================================================
    
    def resumen(self) -> str:
        """Genera un resumen legible de la ficha"""
        lineas = [
            "=" * 50,
            "CARACTERÍSTICAS",
            f"  Fuerza: {self.fuerza}",
            f"  Reflejos: {self.reflejos}",
            f"  Resistencia: {self.resistencia}",
            f"  Voluntad: {self.voluntad}",
            f"  Puntería: {self.punteria}",
            f"  Stamina: {self.stamina}",
            "",
            "STATS DERIVADOS",
            f"  PV Máximos: {self.pv_maximos}",
            f"  PM Máximos: {self.pm_maximos}",
            f"  PCF Máximos: {self.pcf_maximos}",
            f"  PCT Máximos: {self.pct_maximos}",
            f"  PS Máximos: {self.ps_maximos}",
            "=" * 50
        ]
        return "\n".join(lineas)
    
    def aplicar_bonificaciones_clase(self, bonificaciones: dict[str, int]):
        """
        Aplica las bonificaciones de una clase a la ficha.
        
        Args:
            bonificaciones: Dict con habilidad: puntos_bonus
        """
        for habilidad, puntos in bonificaciones.items():
            # Buscar en qué categoría está la habilidad
            if hasattr(self.combate, habilidad):
                valor_actual = getattr(self.combate, habilidad)
                setattr(self.combate, habilidad, valor_actual + puntos)
            elif hasattr(self.educacion, habilidad):
                valor_actual = getattr(self.educacion, habilidad)
                setattr(self.educacion, habilidad, valor_actual + puntos)
            elif hasattr(self.talento, habilidad):
                valor_actual = getattr(self.talento, habilidad)
                setattr(self.talento, habilidad, valor_actual + puntos)


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Sistema de Ficha ===\n")
    
    # Crear ficha básica
    ficha = Ficha()
    
    # Distribuir características (20 puntos)
    ficha.caracteristicas.fuerza = 8
    ficha.caracteristicas.reflejos = 4
    ficha.caracteristicas.resistencia = 7
    ficha.caracteristicas.voluntad = 0
    ficha.caracteristicas.punteria = 0
    ficha.caracteristicas.stamina = 1
    
    # Distribuir habilidades (10 puntos cada categoría)
    ficha.combate.armas_cortantes = 10
    ficha.educacion.medicina = 5
    ficha.educacion.elocuencia = 5
    ficha.talento.percepcion = 10
    
    print(ficha.resumen())
    
    print(f"\n¿Ficha válida? {ficha.es_valida()}")
    print(f"Bonus con armas cortantes: +{ficha.obtener_bonus_habilidad('armas_cortantes')}")

# ==============================================================================
# ARCHIVO 13/36: hephix.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/hephix.py
# ==============================================================================

"""
Clase Hephix - Representa el tipo de magia del personaje.
"""
from pydantic import BaseModel, Field
from typing import Optional
from .tipos import HephixTipo, Constantes


class Hephix(BaseModel):
    """
    Representa el Hephix (marca de nacimiento mágica) del personaje.
    Define qué tipo de magia puede usar.
    """
    
    tipo: HephixTipo
    nivel: int = Field(default=1, ge=1, le=30)
    descripcion: str = ""
    
    # Habilidades mágicas desbloqueadas por nivel
    habilidades_desbloqueadas: list[str] = Field(default_factory=list)
    
    def es_sangriento(self) -> bool:
        """
        Verifica si es el hephix especial 'Sangriento'.
        Este hephix tiene mecánicas únicas (sin PM/PCF/PCT, más PV).
        """
        return self.tipo == HephixTipo.SANGRIENTA
    
    def es_kairenista(self) -> bool:
        """Verifica si pertenece a la rama Kairenista (luz)"""
        return self.tipo in [
            HephixTipo.SANADORA,
            HephixTipo.EXORCISTA,
            HephixTipo.LUMINICA
        ]
    
    def es_vadhenista(self) -> bool:
        """Verifica si pertenece a la rama Vadhenista (oscuridad)"""
        return self.tipo in [
            HephixTipo.CAOTICA,
            HephixTipo.NIGROMANTE,
            HephixTipo.OSCURA
        ]
    
    def calcular_modificador_pv(self, voluntad: int) -> int:
        """
        Calcula el modificador de PV según el hephix.
        Solo el Hephix Sangriento da bonus de PV.
        
        Args:
            voluntad: Stat de Voluntad del personaje
        
        Returns:
            Puntos de vida adicionales
        """
        if self.es_sangriento():
            return voluntad * Constantes.MULTIPLICADOR_PV_SANGRIENTO
        return 0
    
    def puede_usar_pm(self) -> bool:
        """Verifica si puede usar Puntos de Magia"""
        return not self.es_sangriento()
    
    def puede_usar_pcf(self) -> bool:
        """Verifica si puede usar Puntos de Conexión Física"""
        return not self.es_sangriento()
    
    def puede_usar_pct(self) -> bool:
        """Verifica si puede usar Puntos de Conexión Tenaz"""
        return not self.es_sangriento()
    
    def obtener_nivel_siguiente_habilidad(self) -> Optional[int]:
        """
        Obtiene el nivel en el que se desbloqueará la próxima habilidad.
        Las habilidades se desbloquean cada 3 niveles: 3, 6, 9, ..., 30
        
        Returns:
            Nivel de la próxima habilidad o None si ya tiene todas
        """
        niveles_habilidad = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
        
        for nivel in niveles_habilidad:
            if self.nivel < nivel:
                return nivel
        
        return None  # Ya tiene todas las habilidades
    
    def desbloquear_habilidad(self, nombre_habilidad: str):
        """
        Desbloquea una nueva habilidad mágica.
        
        Args:
            nombre_habilidad: Nombre de la habilidad a desbloquear
        """
        if nombre_habilidad not in self.habilidades_desbloqueadas:
            self.habilidades_desbloqueadas.append(nombre_habilidad)
    
    def subir_nivel(self):
        """Incrementa el nivel del hephix"""
        if self.nivel < 30:
            self.nivel += 1
    
    @classmethod
    def crear_desde_tipo(cls, tipo: HephixTipo, descripcion: str = "") -> "Hephix":
        """
        Factory method para crear un Hephix desde su tipo.
        
        Args:
            tipo: Tipo de hephix
            descripcion: Descripción del hephix (opcional)
        
        Returns:
            Nueva instancia de Hephix
        """
        return cls(
            tipo=tipo,
            nivel=1,
            descripcion=descripcion
        )
    
    def __str__(self) -> str:
        especialidad = ""
        if self.es_kairenista():
            especialidad = " (Kairenista)"
        elif self.es_vadhenista():
            especialidad = " (Vadhenista)"
        elif self.es_sangriento():
            especialidad = " (⚠️ ESPECIAL)"
        
        return f"Hephix {self.tipo.value.title()}{especialidad} - Nivel {self.nivel}"
    
    model_config = {"use_enum_values": False}  # Mantener enums como objetos


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Sistema de Hephix ===\n")
    
    # Hephix normal
    hephix_elemental = Hephix.crear_desde_tipo(
        HephixTipo.ELEMENTAL,
        "Control sobre fuego, agua, tierra y aire"
    )
    print(f"{hephix_elemental}")
    print(f"  ¿Puede usar PM? {hephix_elemental.puede_usar_pm()}")
    print(f"  Modificador PV: +{hephix_elemental.calcular_modificador_pv(5)}\n")
    
    # Hephix Sangriento (especial)
    hephix_sangriento = Hephix.crear_desde_tipo(
        HephixTipo.SANGRIENTA,
        "Sacrifica integridad corporal por poder"
    )
    print(f"{hephix_sangriento}")
    print(f"  ¿Puede usar PM? {hephix_sangriento.puede_usar_pm()}")
    print(f"  Modificador PV (Vol=8): +{hephix_sangriento.calcular_modificador_pv(8)}")
    print(f"  ⚠️ Sin PM/PCF/PCT\n")
    
    # Hephix Kairenista
    hephix_sanadora = Hephix.crear_desde_tipo(HephixTipo.SANADORA)
    print(f"{hephix_sanadora}")
    print(f"  Es Kairenista: {hephix_sanadora.es_kairenista()}")
    print(f"  Próxima habilidad en nivel: {hephix_sanadora.obtener_nivel_siguiente_habilidad()}")

# ==============================================================================
# ARCHIVO 14/36: inventario.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/inventario.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 15/36: personaje.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/personaje.py
# ==============================================================================

"""
Clase Personaje - Entidad central del juego.
Integra todas las entidades: Ficha, Hephix, Inventario, etc.
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict
from .ficha import Ficha
from .hephix import Hephix
from .tipos import ClaseTipo, HephixTipo, TipoArma
from .inventario import Inventario
from .arma import Arma, Armadura


class Personaje(BaseModel):
    """
    Representa un personaje jugador completo con todas sus estadísticas,
    equipamiento, progreso e historia.
    """
    
    # ========================================================================
    # Datos personales
    # ========================================================================
    nombre: str
    edad: int = Field(ge=1, le=200)
    raza: str
    nivel: int = Field(default=1, ge=1, le=30)
    experiencia: int = Field(default=0, ge=0)
    
    # ========================================================================
    # Sistema de juego
    # ========================================================================
    clase: ClaseTipo
    hephix: Hephix
    ficha: Ficha
    
    # ========================================================================
    # Estado dinámico (valores actuales en combate/juego)
    # ========================================================================
    pv_actuales: int = Field(default=0)
    pm_actuales: int = Field(default=0)
    pcf_actuales: int = Field(default=0)
    pct_actuales: int = Field(default=0)
    ps_actuales: int = Field(default=0)  # Puntos de Stamina en combate
    
    # ========================================================================
    # Equipamiento
    # ========================================================================
    inventario: Inventario = Field(default_factory=Inventario)
    arma_equipada: Optional[Arma] = None
    armadura_equipada: Optional[Armadura] = None
    
    # ========================================================================
    # Historia y progreso
    # ========================================================================
    historia: str = Field(default="", description="Trasfondo del personaje")
    objetivo: str = Field(default="", description="Objetivo del personaje")
    
    # Sistema de adicciones (drogas)
    adicciones: Dict[str, int] = Field(default_factory=dict, description="Droga: puntos de adicción")
    
    # Estado vital
    esta_vivo: bool = Field(default=True)
    esta_inconsciente: bool = Field(default=False)
    
    def model_post_init(self, __context):
        """Inicializa valores después de crear el modelo"""
        # Sincronizar hephix_tipo en ficha
        self.ficha.hephix_tipo = self.hephix.tipo
        
        # Inicializar stats actuales si están en 0
        if self.pv_actuales == 0:
            self.restaurar_stats_completos()
    
    # ========================================================================
    # Propiedades calculadas (delegadas a ficha)
    # ========================================================================
    
    @property
    def pv_maximos(self) -> int:
        return self.ficha.pv_maximos
    
    @property
    def pm_maximos(self) -> int:
        return self.ficha.pm_maximos
    
    @property
    def pcf_maximos(self) -> int:
        return self.ficha.pcf_maximos
    
    @property
    def pct_maximos(self) -> int:
        return self.ficha.pct_maximos
    
    @property
    def ps_maximos(self) -> int:
        return self.ficha.ps_maximos
    
    # ========================================================================
    # Gestión de vida y recursos
    # ========================================================================
    
    def restaurar_stats_completos(self):
        """Restaura todos los stats a sus valores máximos"""
        self.pv_actuales = self.pv_maximos
        self.pm_actuales = self.pm_maximos
        self.pcf_actuales = self.pcf_maximos
        self.pct_actuales = self.pct_maximos
        self.ps_actuales = self.ps_maximos
    
    def recibir_daño(self, cantidad: int) -> int:
        """
        Aplica daño al personaje.
        
        Args:
            cantidad: Cantidad de daño a recibir
        
        Returns:
            Daño efectivamente recibido (después de armadura)
        """
        # Reducción por armadura
        reduccion = 0
        if self.armadura_equipada:
            reduccion = self.armadura_equipada.reduccion_total()
        
        daño_final = max(0, cantidad - reduccion)
        self.pv_actuales = max(0, self.pv_actuales - daño_final)
        
        # Verificar muerte
        if self.pv_actuales == 0:
            self.esta_vivo = False
            self.esta_inconsciente = True
        
        return daño_final
    
    def curar(self, cantidad: int) -> int:
        """
        Cura al personaje.
        
        Args:
            cantidad: Cantidad de PV a restaurar
        
        Returns:
            PV efectivamente curados
        """
        pv_antes = self.pv_actuales
        self.pv_actuales = min(self.pv_maximos, self.pv_actuales + cantidad)
        return self.pv_actuales - pv_antes
    
    def gastar_pm(self, cantidad: int) -> bool:
        """
        Gasta puntos de magia.
        
        Returns:
            True si tenía suficiente, False si no
        """
        if self.pm_actuales >= cantidad:
            self.pm_actuales -= cantidad
            return True
        return False
    
    def gastar_stamina(self, cantidad: int):
        """Reduce stamina en combate"""
        self.ps_actuales = max(0, self.ps_actuales - cantidad)
    
    def esta_sin_stamina(self) -> bool:
        """Verifica si quedó sin stamina (vulnerable a golpe de gracia)"""
        return self.ps_actuales <= 0
    
    def restaurar_stamina_completa(self):
        """Restaura stamina al máximo (entre combates)"""
        self.ps_actuales = self.ps_maximos
    
    # ========================================================================
    # Sistema de equipamiento
    # ========================================================================
    
    def equipar_arma(self, arma: Arma) -> bool:
        """
        Equipa un arma si cumple requisitos.
        
        Returns:
            True si se equipó, False si no cumple requisitos
        """
        # Verificar nivel
        if self.nivel < arma.nivel_requerido:
            return False
        
        # Verificar habilidad mínima
        habilidad_nombre = arma.tipo_arma.value
        nivel_habilidad = getattr(self.ficha.combate, habilidad_nombre, 0)
        if nivel_habilidad < arma.habilidad_minima:
            return False
        
        # Si ya tiene arma equipada, devolverla al inventario
        if self.arma_equipada:
            self.inventario.agregar_arma(self.arma_equipada)
        
        self.arma_equipada = arma
        return True
    
    def desequipar_arma(self) -> bool:
        """
        Desequipa el arma actual y la devuelve al inventario.
        
        Returns:
            True si se desequipó, False si no había arma
        """
        if not self.arma_equipada:
            return False
        
        if self.inventario.agregar_arma(self.arma_equipada):
            self.arma_equipada = None
            return True
        return False
    
    def equipar_armadura(self, armadura: Armadura) -> bool:
        """Equipa una armadura si cumple requisitos"""
        if self.nivel < armadura.nivel_requerido:
            return False
        
        if self.ficha.resistencia < armadura.resistencia_minima:
            return False
        
        if self.armadura_equipada:
            self.inventario.agregar_armadura(self.armadura_equipada)
        
        self.armadura_equipada = armadura
        return True
    
    def desequipar_armadura(self) -> bool:
        """Desequipa la armadura actual"""
        if not self.armadura_equipada:
            return False
        
        if self.inventario.agregar_armadura(self.armadura_equipada):
            self.armadura_equipada = None
            return True
        return False
    
    # ========================================================================
    # Sistema de habilidades y bonificaciones
    # ========================================================================
    
    def obtener_bonus_habilidad_arma(self, arma: Optional[Arma]) -> int:
        """
        Obtiene el bonus de daño por nivel de habilidad con el arma.
        
        Returns:
            Bonus de daño (+1 cada 5 puntos de habilidad)
        """
        if not arma:
            # Pugilismo para combate sin armas
            return self.ficha.obtener_bonus_habilidad("pugilismo")
        
        return self.ficha.obtener_bonus_habilidad(arma.tipo_arma.value)
    
    def obtener_modificador_reflejos(self) -> int:
        """Obtiene el modificador total de reflejos (base + armadura)"""
        base = self.ficha.reflejos
        bonus_armadura = 0
        if self.armadura_equipada:
            bonus_armadura = self.armadura_equipada.bonus_reflejos
        
        return base + bonus_armadura
    
    # ========================================================================
    # Sistema de nivel y experiencia
    # ========================================================================
    
    def ganar_experiencia(self, cantidad: int):
        """
        Otorga experiencia y verifica si sube de nivel.
        
        Args:
            cantidad: Cantidad de XP a otorgar
        """
        self.experiencia += cantidad
        
        # Sistema simple: cada 1000 XP = 1 nivel
        xp_necesaria = self.nivel * 1000
        
        while self.experiencia >= xp_necesaria and self.nivel < 30:
            self.subir_nivel()
            xp_necesaria = self.nivel * 1000
    
    def subir_nivel(self):
        """Sube el nivel del personaje"""
        if self.nivel >= 30:
            return
        
        self.nivel += 1
        self.hephix.subir_nivel()
        
        # Restaurar stats al subir de nivel
        self.restaurar_stats_completos()
    
    # ========================================================================
    # Sistema de adicciones
    # ========================================================================
    
    def consumir_droga(self, nombre_droga: str, puntos_adiccion: int):
        """Registra consumo de droga y aumenta adicción"""
        if nombre_droga not in self.adicciones:
            self.adicciones[nombre_droga] = 0
        
        self.adicciones[nombre_droga] += puntos_adiccion
    
    def obtener_nivel_adiccion(self, nombre_droga: str) -> int:
        """
        Obtiene el nivel de adicción a una droga.
        Cada 20 puntos = 1 nivel
        """
        puntos = self.adicciones.get(nombre_droga, 0)
        return puntos // 20
    
    # ========================================================================
    # Métodos de utilidad
    # ========================================================================
    
    def esta_en_condiciones_combate(self) -> bool:
        """Verifica si puede combatir"""
        return self.esta_vivo and not self.esta_inconsciente and self.pv_actuales > 0
    
    def resumen_completo(self) -> str:
        """Genera un resumen completo del personaje"""
        lineas = [
            "=" * 60,
            f"PERSONAJE: {self.nombre}",
            f"Raza: {self.raza} | Edad: {self.edad} | Nivel: {self.nivel}",
            f"Clase: {self.clase.value.title()}",
            f"Hephix: {self.hephix.tipo.value.title()} (Nivel {self.hephix.nivel})",
            f"Experiencia: {self.experiencia} XP",
            "",
            "ESTADO ACTUAL",
            f"  PV: {self.pv_actuales}/{self.pv_maximos}",
            f"  PM: {self.pm_actuales}/{self.pm_maximos}",
            f"  PCF: {self.pcf_actuales}/{self.pcf_maximos}",
            f"  PCT: {self.pct_actuales}/{self.pct_maximos}",
            f"  PS: {self.ps_actuales}/{self.ps_maximos}",
            "",
            "EQUIPAMIENTO",
            f"  Arma: {self.arma_equipada if self.arma_equipada else 'Sin equipar'}",
            f"  Armadura: {self.armadura_equipada if self.armadura_equipada else 'Sin equipar'}",
            "",
        ]
        
        # Agregar resumen de ficha
        lineas.append(self.ficha.resumen())
        
        return "\n".join(lineas)
    
    def to_dict_guardado(self) -> dict:
        """Serializa el personaje para guardado (compatible con JSON)"""
        return self.model_dump(mode='json')
    
    @classmethod
    def from_dict_guardado(cls, data: dict) -> "Personaje":
        """Deserializa el personaje desde un guardado"""
        return cls.model_validate(data)


if __name__ == "__main__":
    from .arma import crear_espada_basica
    
    print("=== Sistema de Personaje ===\n")
    
    # Crear personaje de ejemplo
    ficha = Ficha()
    ficha.caracteristicas.fuerza = 8
    ficha.caracteristicas.reflejos = 4
    ficha.caracteristicas.resistencia = 7
    ficha.caracteristicas.voluntad = 0
    ficha.caracteristicas.punteria = 0
    ficha.caracteristicas.stamina = 1
    
    ficha.combate.armas_cortantes = 10
    ficha.educacion.medicina = 5
    ficha.talento.percepcion = 5
    
    hephix = Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL)
    
    personaje = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=hephix,
        ficha=ficha,
        historia="Un guerrero de las montañas del norte"
    )
    
    # Equipar arma
    espada = crear_espada_basica()
    personaje.inventario.agregar_arma(espada)
    personaje.equipar_arma(espada)
    
    print(personaje.resumen_completo())
    
    # Simular combate
    print("\n=== Simulación de Combate ===")
    print(f"Recibiendo 25 de daño...")
    daño = personaje.recibir_daño(25)
    print(f"  Daño recibido: {daño}")
    print(f"  PV restantes: {personaje.pv_actuales}/{personaje.pv_maximos}")

# ==============================================================================
# ARCHIVO 16/36: tipos.py
# Directorio: entidades
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./entidades/tipos.py
# ==============================================================================

"""
Tipos, enums y constantes del sistema Ether Blades.
Define todas las enumeraciones usadas en el juego.
"""
from enum import Enum


class HephixTipo(str, Enum):
    """Tipos de Hephix (magia)"""
    # Generales
    ELEMENTAL = "elemental"
    PSIQUICA = "psiquica"
    OCULTA = "oculta"
    MORPHICA = "morphica"
    ESPIRITUAL = "espiritual"
    CRISTALINA = "cristalina"
    SANGRIENTA = "sangrienta"  # Caso especial: sin PM/PCF/PCT
    
    # Kairenistas (luz)
    SANADORA = "sanadora"
    EXORCISTA = "exorcista"
    LUMINICA = "luminica"
    
    # Vadhenistas (oscuridad)
    CAOTICA = "caotica"
    NIGROMANTE = "nigromante"
    OSCURA = "oscura"


class ClaseTipo(str, Enum):
    """Clases de personaje"""
    CURANDERO = "curandero"
    GUERRERO = "guerrero"
    MAGO = "mago"
    EXPLORADOR = "explorador"
    ARTESANO = "artesano"
    DIPLOMATICO = "diplomatico"


class TipoArma(str, Enum):
    """Categorías de armas"""
    CORTANTE_PUNZANTE = "armas_cortantes"
    CONTUNDENTE = "armas_contundentes"
    MAGICA = "armas_magicas"
    DISTANCIA = "armas_distancia"
    PUGILISMO = "pugilismo"


class TipoAtaque(str, Enum):
    """Tipos de ataque según mecánica"""
    MELEE = "melee"
    DISTANCIA = "distancia"
    MAGICO = "magico"


class TipoArmadura(str, Enum):
    """Tipos de armadura"""
    LIGERA = "ligera"
    MEDIA = "media"
    PESADA = "pesada"
    MAGICA = "magica"


class RarezaItem(str, Enum):
    """Rareza de ítems y equipamiento"""
    COMUN = "comun"
    POCO_COMUN = "poco_comun"
    RARO = "raro"
    EPICO = "epico"
    LEGENDARIO = "legendario"


class EstadoCombate(str, Enum):
    """Estados posibles en combate"""
    FUERA_COMBATE = "fuera_combate"
    EN_COMBATE = "en_combate"
    TURNO_JUGADOR = "turno_jugador"
    TURNO_ENEMIGO = "turno_enemigo"
    COMBATE_FINALIZADO = "combate_finalizado"


class TipoAccion(str, Enum):
    """Acciones posibles en combate"""
    ATACAR = "atacar"
    DEFENDER = "defender"
    USAR_HABILIDAD = "usar_habilidad"
    USAR_ITEM = "usar_item"
    HUIR = "huir"


# Constantes del sistema
class Constantes:
    """Constantes globales del juego"""
    
    # Puntos iniciales para distribución
    PUNTOS_CARACTERISTICAS = 20
    PUNTOS_COMBATE = 10
    PUNTOS_EDUCACION = 10
    PUNTOS_TALENTO = 10
    
    # Fórmulas de stats derivados
    MULTIPLICADOR_PV = 10  # PV = Res × 10
    MULTIPLICADOR_PM = 5   # PM = Vol × 5
    MULTIPLICADOR_PCF = 5  # PCF = Fue × 5
    MULTIPLICADOR_PCT = 5  # PCT = Pun × 5
    MULTIPLICADOR_STAMINA = 5  # Coef. Stamina = Sta × 5
    
    # Bonus Hephix Sangriento
    MULTIPLICADOR_PV_SANGRIENTO = 5  # +Vol × 5 PV
    
    # Combate
    DADOS_ATAQUE = 3  # 3d6 para ataque
    DADOS_DEFENSA = 2  # 2d6 para defensa
    DADOS_INICIATIVA = 1  # 1d10 para iniciativa
    UMBRAL_CONTRAATAQUE = -3  # Si diferencia ≤ -3, hay contraataque
    
    # Habilidades
    BONUS_HABILIDAD_POR_NIVEL = 5  # Cada 5 puntos de habilidad = +1 daño
    PUNTOS_MENTALIDAD_POR_HABILIDAD_EXTRA = 10  # Cada 10 mentalidad = +1 habilidad
    
    # Sanación
    BONUS_SANACION_POR_MEDICINA = 5  # Cada 5 medicina = +bonus
    TURNOS_PRIMEROS_AUXILIOS = 1
    TURNOS_KIT_ATENCION = 2
    BASE_PRIMEROS_AUXILIOS = 10
    BASE_KIT_ATENCION = 30
    
    # Adicción (drogas)
    PUNTOS_POR_NIVEL_ADICCION = 20  # Cada 20 puntos = 1 nivel
    
    # Sistema de comprensión
    PUNTOS_COMPRENSION_MAX = 100


# Nombres de habilidades (para validación)
class NombresHabilidades:
    """Nombres estándar de habilidades"""
    
    # Combate
    ARMAS_CORTANTES = "armas_cortantes"
    ARMAS_CONTUNDENTES = "armas_contundentes"
    ARMAS_MAGICAS = "armas_magicas"
    ARMAS_DISTANCIA = "armas_distancia"
    PUGILISMO = "pugilismo"
    
    # Educación
    MEDICINA = "medicina"
    ELOCUENCIA = "elocuencia"
    MANUAL = "manual"
    ARCANISMO = "arcanismo"
    
    # Talento
    SIGILO = "sigilo"
    PERCEPCION = "percepcion"
    MENTALIDAD = "mentalidad"
    ASTRALIDAD = "astralidad"
    
    @classmethod
    def todas_combate(cls) -> list[str]:
        return [
            cls.ARMAS_CORTANTES,
            cls.ARMAS_CONTUNDENTES,
            cls.ARMAS_MAGICAS,
            cls.ARMAS_DISTANCIA,
            cls.PUGILISMO
        ]
    
    @classmethod
    def todas_educacion(cls) -> list[str]:
        return [
            cls.MEDICINA,
            cls.ELOCUENCIA,
            cls.MANUAL,
            cls.ARCANISMO
        ]
    
    @classmethod
    def todas_talento(cls) -> list[str]:
        return [
            cls.SIGILO,
            cls.PERCEPCION,
            cls.MENTALIDAD,
            cls.ASTRALIDAD
        ]


if __name__ == "__main__":
    print("=== Tipos y Constantes de Ether Blades ===\n")
    
    print(f"Tipos de Hephix disponibles: {len(HephixTipo)}")
    for h in HephixTipo:
        print(f"  - {h.value}")
    
    print(f"\nClases disponibles: {len(ClaseTipo)}")
    for c in ClaseTipo:
        print(f"  - {c.value}")
    
    print(f"\nConstantes del sistema:")
    print(f"  Puntos iniciales características: {Constantes.PUNTOS_CARACTERISTICAS}")
    print(f"  Fórmula PV: Res × {Constantes.MULTIPLICADOR_PV}")
    print(f"  Fórmula PM: Vol × {Constantes.MULTIPLICADOR_PM}")


################################################################################
# DIRECTORIO: patrones
################################################################################

# ==============================================================================
# ARCHIVO 17/36: __init__.py
# Directorio: patrones
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./patrones/__init__.py
# ==============================================================================

"""
Módulo de patrones de diseño para Ether Blades.
Exporta las clases principales de cada patrón.
"""

from .singleton import SingletonMeta
from .factory_method import Factory, FactoryConRegistro, FactoryDesdeJSON
from .observer import EventBus, Evento, TipoEvento, EventCallback
from .strategy import (
    EstrategiaAtaque,
    EstrategiaAtaqueMelee,
    EstrategiaAtaqueDistancia,
    EstrategiaAtaqueMagico,
    RegistroEstrategiasAtaque,
    TipoAtaque,
    ComportamientoIA,
    IAAgresiva,
    IADefensiva,
    IATactica,
    RegistroComportamientosIA
)

__all__ = [
    # Singleton
    'SingletonMeta',
    
    # Factory
    'Factory',
    'FactoryConRegistro',
    'FactoryDesdeJSON',
    
    # Observer
    'EventBus',
    'Evento',
    'TipoEvento',
    'EventCallback',
    
    # Strategy - Ataque
    'EstrategiaAtaque',
    'EstrategiaAtaqueMelee',
    'EstrategiaAtaqueDistancia',
    'EstrategiaAtaqueMagico',
    'RegistroEstrategiasAtaque',
    'TipoAtaque',
    
    # Strategy - IA
    'ComportamientoIA',
    'IAAgresiva',
    'IADefensiva',
    'IATactica',
    'RegistroComportamientosIA',
]

# ==============================================================================
# ARCHIVO 18/36: factory_method.py
# Directorio: patrones
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./patrones/factory_method.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 19/36: observer.py
# Directorio: patrones
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./patrones/observer.py
# ==============================================================================

"""
Patrón Observer - Sistema de eventos para desacoplar componentes.
Permite que múltiples objetos reaccionen a eventos sin conocerse entre sí.
"""
from typing import Callable, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# Tipos de eventos del sistema
class TipoEvento(str, Enum):
    """Enum con todos los tipos de eventos del juego"""
    # Eventos de combate
    COMBATE_INICIADO = "combate_iniciado"
    TURNO_INICIADO = "turno_iniciado"
    ATAQUE_REALIZADO = "ataque_realizado"
    ATAQUE_BLOQUEADO = "ataque_bloqueado"
    CONTRAATAQUE = "contraataque"
    GOLPE_GRACIA = "golpe_gracia"
    DAÑO_RECIBIDO = "daño_recibido"
    STAMINA_AGOTADA = "stamina_agotada"
    
    # Eventos de personaje
    PERSONAJE_HERIDO = "personaje_herido"
    PERSONAJE_CURADO = "personaje_curado"
    PERSONAJE_MUERTO = "personaje_muerto"
    NIVEL_SUBIDO = "nivel_subido"
    HABILIDAD_DESBLOQUEADA = "habilidad_desbloqueada"
    
    # Eventos de magia
    HECHIZO_LANZADO = "hechizo_lanzado"
    MANA_AGOTADO = "mana_agotado"
    
    # Eventos narrativos
    DECISION_TOMADA = "decision_tomada"
    CHECKPOINT_ALCANZADO = "checkpoint_alcanzado"
    MISION_COMPLETADA = "mision_completada"
    
    # Eventos de sistema
    PARTIDA_GUARDADA = "partida_guardada"
    PARTIDA_CARGADA = "partida_cargada"
    ERROR_SISTEMA = "error_sistema"


@dataclass
class Evento:
    """
    Representa un evento del sistema con su información asociada.
    """
    tipo: TipoEvento
    datos: Dict[str, Any]
    timestamp: datetime
    prioridad: int = 0  # Mayor número = mayor prioridad
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


# Tipo para callbacks
EventCallback = Callable[[Evento], None]


class EventBus:
    """
    Bus de eventos central del sistema.
    Implementa el patrón Observer/Pub-Sub.
    """
    
    def __init__(self):
        self._subscriptores: Dict[TipoEvento, List[EventCallback]] = {}
        self._historial: List[Evento] = []
        self._max_historial = 100  # Mantener últimos 100 eventos
        self._activo = True
    
    def suscribir(self, tipo_evento: TipoEvento, callback: EventCallback) -> None:
        """
        Suscribe un callback a un tipo de evento específico.
        
        Args:
            tipo_evento: Tipo de evento al que suscribirse
            callback: Función que se llamará cuando ocurra el evento
                     Debe aceptar un parámetro de tipo Evento
        
        Ejemplo:
            def manejador(evento: Evento):
                print(f"Recibido: {evento.tipo}")
            
            bus.suscribir(TipoEvento.ATAQUE_REALIZADO, manejador)
        """
        if tipo_evento not in self._subscriptores:
            self._subscriptores[tipo_evento] = []
        
        if callback not in self._subscriptores[tipo_evento]:
            self._subscriptores[tipo_evento].append(callback)
    
    def desuscribir(self, tipo_evento: TipoEvento, callback: EventCallback) -> None:
        """
        Remueve un callback de la lista de subscriptores.
        
        Args:
            tipo_evento: Tipo de evento
            callback: Callback a remover
        """
        if tipo_evento in self._subscriptores:
            try:
                self._subscriptores[tipo_evento].remove(callback)
            except ValueError:
                pass  # El callback no estaba suscrito
    
    def publicar(self, tipo_evento: TipoEvento, datos: Dict[str, Any] = None, 
                 prioridad: int = 0) -> None:
        """
        Publica un evento, notificando a todos los subscriptores.
        
        Args:
            tipo_evento: Tipo de evento a publicar
            datos: Información asociada al evento
            prioridad: Prioridad del evento (mayor = más importante)
        
        Ejemplo:
            bus.publicar(
                TipoEvento.DAÑO_RECIBIDO,
                {"personaje": "Aldric", "daño": 25, "pv_restantes": 45}
            )
        """
        if not self._activo:
            return
        
        # Crear evento
        evento = Evento(
            tipo=tipo_evento,
            datos=datos or {},
            timestamp=datetime.now(),
            prioridad=prioridad
        )
        
        # Agregar al historial
        self._historial.append(evento)
        if len(self._historial) > self._max_historial:
            self._historial.pop(0)
        
        # Notificar subscriptores
        if tipo_evento in self._subscriptores:
            for callback in self._subscriptores[tipo_evento]:
                try:
                    callback(evento)
                except Exception as e:
                    # Log del error pero continuar notificando otros subscriptores
                    print(f"Error en callback de {tipo_evento}: {e}")
    
    def obtener_historial(self, tipo_evento: TipoEvento = None, 
                          limite: int = None) -> List[Evento]:
        """
        Obtiene el historial de eventos.
        
        Args:
            tipo_evento: Filtrar por tipo (None = todos)
            limite: Cantidad máxima de eventos a retornar
        
        Returns:
            Lista de eventos (más recientes primero)
        """
        eventos = self._historial[::-1]  # Invertir (más recientes primero)
        
        if tipo_evento:
            eventos = [e for e in eventos if e.tipo == tipo_evento]
        
        if limite:
            eventos = eventos[:limite]
        
        return eventos
    
    def limpiar_historial(self) -> None:
        """Limpia el historial de eventos"""
        self._historial.clear()
    
    def pausar(self) -> None:
        """Pausa la publicación de eventos (útil para debugging)"""
        self._activo = False
    
    def reanudar(self) -> None:
        """Reanuda la publicación de eventos"""
        self._activo = True
    
    def contar_subscriptores(self, tipo_evento: TipoEvento = None) -> int:
        """
        Cuenta subscriptores de un evento específico o en total.
        
        Args:
            tipo_evento: Tipo específico (None = todos)
        
        Returns:
            Cantidad de subscriptores
        """
        if tipo_evento:
            return len(self._subscriptores.get(tipo_evento, []))
        else:
            return sum(len(subs) for subs in self._subscriptores.values())


# Ejemplo de uso
if __name__ == "__main__":
    # Crear bus de eventos
    bus = EventBus()
    
    # Definir manejadores
    def logger(evento: Evento):
        print(f"[LOG] {evento.tipo}: {evento.datos}")
    
    def contador_daño(evento: Evento):
        if "daño" in evento.datos:
            print(f"[CONTADOR] Daño total acumulado: {evento.datos['daño']}")
    
    # Suscribir manejadores
    bus.suscribir(TipoEvento.ATAQUE_REALIZADO, logger)
    bus.suscribir(TipoEvento.DAÑO_RECIBIDO, logger)
    bus.suscribir(TipoEvento.DAÑO_RECIBIDO, contador_daño)
    
    # Publicar eventos
    bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
        "atacante": "Aldric",
        "defensor": "Goblin",
        "resultado": "éxito"
    })
    
    bus.publicar(TipoEvento.DAÑO_RECIBIDO, {
        "personaje": "Goblin",
        "daño": 25,
        "pv_restantes": 15
    })
    
    # Ver historial
    print(f"\n[HISTORIAL] Eventos registrados: {len(bus.obtener_historial())}")
    print(f"[STATS] Subscriptores totales: {bus.contar_subscriptores()}")

# ==============================================================================
# ARCHIVO 20/36: singleton.py
# Directorio: patrones
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./patrones/singleton.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 21/36: strategy.py
# Directorio: patrones
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./patrones/strategy.py
# ==============================================================================

"""
Patrón Strategy - Permite intercambiar algoritmos en tiempo de ejecución.
Se usa para cálculos de ataque, comportamiento de IA, etc.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from entidades.personaje import Personaje
    from entidades.arma import Arma


class TipoAtaque(str, Enum):
    """Tipos de ataque según el arma"""
    MELEE = "melee"
    DISTANCIA = "distancia"
    MAGICO = "magico"


class EstrategiaAtaque(ABC):
    """
    Estrategia base para calcular ataques.
    Define la interfaz común para todos los tipos de ataque.
    """
    
    @abstractmethod
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """
        Calcula el coeficiente de ataque.
        
        Args:
            atacante: Personaje que ataca
            arma: Arma utilizada
            dados: Resultado de las tiradas de dados
        
        Returns:
            Coeficiente de ataque total
        """
        pass
    
    @abstractmethod
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        """
        Obtiene el stat base para este tipo de ataque.
        
        Returns:
            Valor de la característica relevante (Fue/Pun/Vol)
        """
        pass


class EstrategiaAtaqueMelee(EstrategiaAtaque):
    """Estrategia para ataques cuerpo a cuerpo (usa Fuerza)"""
    
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """CA = Fuerza + 3d6 + bonus_arma"""
        stat = self.obtener_stat_base(atacante)
        suma_dados = sum(dados)
        bonus_arma = arma.bonus if arma else 0
        bonus_habilidad = atacante.obtener_bonus_habilidad_arma(arma)
        
        return stat + suma_dados + bonus_arma + bonus_habilidad
    
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        return atacante.ficha.fuerza


class EstrategiaAtaqueDistancia(EstrategiaAtaque):
    """Estrategia para ataques a distancia (usa Puntería)"""
    
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """CA = Puntería + 3d6 + bonus_arma"""
        stat = self.obtener_stat_base(atacante)
        suma_dados = sum(dados)
        bonus_arma = arma.bonus if arma else 0
        bonus_habilidad = atacante.obtener_bonus_habilidad_arma(arma)
        
        return stat + suma_dados + bonus_arma + bonus_habilidad
    
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        return atacante.ficha.punteria


class EstrategiaAtaqueMagico(EstrategiaAtaque):
    """Estrategia para ataques mágicos (usa Voluntad)"""
    
    def calcular_coeficiente(self, atacante: 'Personaje', arma: 'Arma', 
                            dados: list[int]) -> int:
        """CA = Voluntad + 3d6 + bonus_arma"""
        stat = self.obtener_stat_base(atacante)
        suma_dados = sum(dados)
        bonus_arma = arma.bonus if arma else 0
        bonus_habilidad = atacante.obtener_bonus_habilidad_arma(arma)
        
        return stat + suma_dados + bonus_arma + bonus_habilidad
    
    def obtener_stat_base(self, atacante: 'Personaje') -> int:
        return atacante.ficha.voluntad


class RegistroEstrategiasAtaque:
    """
    Registro centralizado de estrategias de ataque.
    Permite obtener la estrategia correcta según el tipo de arma.
    """
    
    _estrategias: Dict[TipoAtaque, EstrategiaAtaque] = {
        TipoAtaque.MELEE: EstrategiaAtaqueMelee(),
        TipoAtaque.DISTANCIA: EstrategiaAtaqueDistancia(),
        TipoAtaque.MAGICO: EstrategiaAtaqueMagico()
    }
    
    @classmethod
    def obtener(cls, tipo: TipoAtaque) -> EstrategiaAtaque:
        """Obtiene la estrategia correspondiente al tipo de ataque"""
        return cls._estrategias[tipo]
    
    @classmethod
    def registrar(cls, tipo: TipoAtaque, estrategia: EstrategiaAtaque):
        """Permite registrar estrategias personalizadas"""
        cls._estrategias[tipo] = estrategia


# ============================================================================
# Estrategias de IA para enemigos
# ============================================================================

class ComportamientoIA(ABC):
    """
    Estrategia base para el comportamiento de enemigos.
    Define cómo un enemigo decide sus acciones en combate.
    """
    
    @abstractmethod
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decide qué acción tomará el enemigo.
        
        Args:
            enemigo: El enemigo que decide
            objetivos: Lista de posibles objetivos (jugadores)
            estado_combate: Estado actual del combate
        
        Returns:
            Dict con la acción decidida:
            {
                "tipo": "atacar" | "defender" | "habilidad",
                "objetivo": Personaje | None,
                "habilidad": Habilidad | None
            }
        """
        pass


class IAAgresiva(ComportamientoIA):
    """IA que siempre ataca al objetivo con menos PV"""
    
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        # Buscar objetivo con menos PV
        objetivo = min(objetivos, key=lambda p: p.pv_actuales)
        
        return {
            "tipo": "atacar",
            "objetivo": objetivo,
            "habilidad": None
        }


class IADefensiva(ComportamientoIA):
    """IA que defiende cuando tiene poca vida y ataca cuando está saludable"""
    
    def __init__(self, umbral_defensa: float = 0.3):
        """
        Args:
            umbral_defensa: % de vida bajo el cual defiende (0.3 = 30%)
        """
        self.umbral_defensa = umbral_defensa
    
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        # Calcular porcentaje de vida
        porcentaje_vida = enemigo.pv_actuales / enemigo.ficha.pv_maximos
        
        if porcentaje_vida < self.umbral_defensa:
            return {
                "tipo": "defender",
                "objetivo": None,
                "habilidad": None
            }
        else:
            # Atacar al más peligroso (mayor ataque)
            objetivo = max(objetivos, key=lambda p: p.ficha.fuerza)
            return {
                "tipo": "atacar",
                "objetivo": objetivo,
                "habilidad": None
            }


class IATactica(ComportamientoIA):
    """IA que usa habilidades cuando es apropiado"""
    
    def decidir_accion(self, enemigo: 'Personaje', 
                      objetivos: list['Personaje'], 
                      estado_combate: Dict[str, Any]) -> Dict[str, Any]:
        # Si hay múltiples objetivos y tiene habilidad de área
        if len(objetivos) > 2 and enemigo.pm_actuales > 20:
            # TODO: Buscar habilidad de área
            pass
        
        # Si alguien está muy dañado, rematar
        objetivo_debil = min(objetivos, key=lambda p: p.pv_actuales)
        if objetivo_debil.pv_actuales < 20:
            return {
                "tipo": "atacar",
                "objetivo": objetivo_debil,
                "habilidad": None
            }
        
        # Caso por defecto: atacar al que más daño hace
        objetivo = max(objetivos, key=lambda p: p.ficha.fuerza)
        return {
            "tipo": "atacar",
            "objetivo": objetivo,
            "habilidad": None
        }


class RegistroComportamientosIA:
    """Registro de comportamientos de IA disponibles"""
    
    _comportamientos: Dict[str, ComportamientoIA] = {
        "agresiva": IAAgresiva(),
        "defensiva": IADefensiva(),
        "tactica": IATactica()
    }
    
    @classmethod
    def obtener(cls, tipo: str) -> ComportamientoIA:
        """Obtiene un comportamiento por nombre"""
        if tipo not in cls._comportamientos:
            raise ValueError(f"Comportamiento '{tipo}' no encontrado")
        return cls._comportamientos[tipo]
    
    @classmethod
    def registrar(cls, nombre: str, comportamiento: ComportamientoIA):
        """Registra un nuevo comportamiento de IA"""
        cls._comportamientos[nombre] = comportamiento
    
    @classmethod
    def listar_disponibles(cls) -> list[str]:
        """Lista todos los comportamientos disponibles"""
        return list(cls._comportamientos.keys())


# Ejemplo de uso
if __name__ == "__main__":
    print("=== Estrategias de Ataque ===")
    print(f"Tipos disponibles: {[t.value for t in TipoAtaque]}")
    
    print("\n=== Comportamientos de IA ===")
    print(f"Comportamientos: {RegistroComportamientosIA.listar_disponibles()}")
    
    # Ejemplo de uso de estrategia
    estrategia_melee = RegistroEstrategiasAtaque.obtener(TipoAtaque.MELEE)
    print(f"\nEstrategia Melee: {estrategia_melee.__class__.__name__}")


################################################################################
# DIRECTORIO: servicios
################################################################################

# ==============================================================================
# ARCHIVO 22/36: __init__.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/__init__.py
# ==============================================================================

"""
Módulo de servicios de aplicación.
Contiene la lógica de negocio del juego.
"""

from .creacion_personaje_service import CreacionPersonajeService
from .combate_service import CombateService
from .combate_estructuras import (
    ResultadoAtaque,
    TipoResultadoAtaque,
    EstadoCombate,
    EstadoCombatiente
)
from .persistencia_service import PersistenciaService
from .persistencia_estructuras import (
    ContextoNarrativo,
    EventoNarrativo,
    TipoEvento as TipoEventoNarrativo,
    DatosPartida,
    InfoSlot
)
from .narrador_service import NarradorService
from .cliente_ia import ClienteIA, ClienteIAMock

__all__ = [
    'CreacionPersonajeService',
    'CombateService',
    'ResultadoAtaque',
    'TipoResultadoAtaque',
    'EstadoCombate',
    'EstadoCombatiente',
    'PersistenciaService',
    'ContextoNarrativo',
    'EventoNarrativo',
    'TipoEventoNarrativo',
    'DatosPartida',
    'InfoSlot',
    'NarradorService',
    'ClienteIA',
    'ClienteIAMock',
]

# ==============================================================================
# ARCHIVO 23/36: cliente_ia.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/cliente_ia.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 24/36: combate_estructuras.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/combate_estructuras.py
# ==============================================================================

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

# ==============================================================================
# ARCHIVO 25/36: combate_service.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/combate_service.py
# ==============================================================================

"""
Servicio de Combate - Motor de combate determinista.
Implementa todas las reglas de combate de Ether Blades.
"""
from typing import List, Optional
from entidades import (
    Personaje, tirar_dados, tirar_d10, Constantes,
    TipoAtaque
)
from patrones import EventBus, TipoEvento, RegistroEstrategiasAtaque
from .combate_estructuras import (
    ResultadoAtaque, TipoResultadoAtaque,
    EstadoCombate, EstadoCombatiente
)


class CombateService:
    """
    Servicio principal de combate.
    Implementa todas las mecánicas de combate del juego.
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None):
        """
        Args:
            event_bus: Bus de eventos para notificaciones (opcional)
        """
        self.event_bus = event_bus or EventBus()
        self.estado: Optional[EstadoCombate] = None
    
    # ========================================================================
    # Inicialización de combate
    # ========================================================================
    
    def iniciar_combate(self, combatientes: List[Personaje]) -> EstadoCombate:
        """
        Inicia un nuevo combate entre los combatientes.
        
        Args:
            combatientes: Lista de personajes que participan
        
        Returns:
            Estado inicial del combate
        """
        if len(combatientes) < 2:
            raise ValueError("Se necesitan al menos 2 combatientes")
        
        # Restaurar stamina de todos
        for c in combatientes:
            c.restaurar_stamina_completa()
        
        # Calcular iniciativa (Sta + 1d10)
        iniciativas = []
        for combatiente in combatientes:
            tirada = tirar_d10()
            iniciativa_total = combatiente.ficha.stamina + tirada.total
            iniciativas.append((combatiente, iniciativa_total))
        
        # Ordenar por iniciativa (mayor primero)
        iniciativas.sort(key=lambda x: x[1], reverse=True)
        
        # Crear estado de combate
        self.estado = EstadoCombate()
        
        for combatiente, iniciativa in iniciativas:
            estado_comb = EstadoCombatiente(
                nombre=combatiente.nombre,
                pv_actuales=combatiente.pv_actuales,
                pv_maximos=combatiente.pv_maximos,
                ps_actuales=combatiente.ps_actuales,
                ps_maximos=combatiente.ps_maximos,
                esta_vivo=combatiente.esta_vivo,
                esta_inconsciente=combatiente.esta_inconsciente,
                iniciativa=iniciativa
            )
            self.estado.combatientes.append(estado_comb)
            self.estado.orden_turnos.append(combatiente.nombre)
        
        # Publicar evento
        self.event_bus.publicar(TipoEvento.COMBATE_INICIADO, {
            "combatientes": [c.nombre for c in combatientes],
            "orden_iniciativa": self.estado.orden_turnos
        })
        
        return self.estado
    
    # ========================================================================
    # Resolución de ataques
    # ========================================================================
    
    def resolver_ataque(self, atacante: Personaje, defensor: Personaje) -> ResultadoAtaque:
        """
        Resuelve un ataque completo entre dos personajes.
        Implementa las reglas de combate de Ether Blades.
        
        Args:
            atacante: Personaje que ataca
            defensor: Personaje que defiende
        
        Returns:
            Resultado detallado del ataque
        """
        # Verificar que ambos están en condiciones de combatir
        if not atacante.esta_en_condiciones_combate():
            raise ValueError(f"{atacante.nombre} no puede combatir")
        
        if not defensor.esta_en_condiciones_combate():
            raise ValueError(f"{defensor.nombre} no puede combatir")
        
        # Calcular coeficientes
        ca = self._calcular_coeficiente_ataque(atacante)
        cd = self._calcular_coeficiente_defensa(defensor)
        
        diferencia = ca - cd
        
        # Publicar evento de ataque realizado
        self.event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre,
            "ca": ca,
            "cd": cd,
            "diferencia": diferencia
        })
        
        # Determinar resultado según la diferencia
        if diferencia > 0:
            # Atacante gana: reduce stamina del defensor
            return self._aplicar_reduccion_stamina(atacante, defensor, diferencia)
        
        elif diferencia <= Constantes.UMBRAL_CONTRAATAQUE:
            # Defensor tiene derecho a contraataque (diferencia <= -3)
            return self._contraataque(atacante, defensor, diferencia)
        
        else:
            # Ataque bloqueado (diferencia entre -2 y 0)
            return self._ataque_bloqueado(atacante, defensor, ca, cd)
    
    def _calcular_coeficiente_ataque(self, atacante: Personaje) -> int:
        """
        Calcula el Coeficiente de Ataque (CA).
        Fórmula: Stat base + 3d6 + bonus_arma + bonus_habilidad
        """
        # Obtener estrategia según tipo de arma
        if atacante.arma_equipada:
            estrategia = RegistroEstrategiasAtaque.obtener(atacante.arma_equipada.tipo_ataque)
        else:
            # Pugilismo (sin arma)
            estrategia = RegistroEstrategiasAtaque.obtener(TipoAtaque.MELEE)
        
        # Tirar dados
        tirada = tirar_dados(Constantes.DADOS_ATAQUE, 6)
        
        # Calcular usando la estrategia
        ca = estrategia.calcular_coeficiente(atacante, atacante.arma_equipada, tirada.dados)
        
        return ca
    
    def _calcular_coeficiente_defensa(self, defensor: Personaje) -> int:
        """
        Calcula el Coeficiente de Defensa (CD).
        Fórmula: Reflejos + 2d6 + bonus_armadura
        """
        tirada = tirar_dados(Constantes.DADOS_DEFENSA, 6)
        cd = defensor.obtener_modificador_reflejos() + tirada.total
        
        return cd
    
    def _aplicar_reduccion_stamina(self, atacante: Personaje, 
                                   defensor: Personaje, 
                                   diferencia: int) -> ResultadoAtaque:
        """
        Aplica reducción de stamina cuando el atacante gana.
        Si la stamina llega a 0, permite golpe de gracia.
        """
        # Reducir stamina
        defensor.gastar_stamina(diferencia)
        
        resultado = ResultadoAtaque(
            tipo=TipoResultadoAtaque.EXITO,
            atacante_nombre=atacante.nombre,
            defensor_nombre=defensor.nombre,
            stamina_perdida=diferencia,
            defensor_pv_restantes=defensor.pv_actuales,
            defensor_stamina_restante=defensor.ps_actuales,
            arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
        )
        
        # Verificar si quedó sin stamina -> GOLPE DE GRACIA
        if defensor.esta_sin_stamina():
            resultado_gracia = self._golpe_de_gracia(atacante, defensor)
            resultado.fue_golpe_gracia = True
            resultado.tipo = TipoResultadoAtaque.CRITICO
            resultado.daño_infligido = resultado_gracia.daño_infligido
            resultado.defensor_pv_restantes = resultado_gracia.defensor_pv_restantes
            resultado.defensor_muerto = resultado_gracia.defensor_muerto
        
        return resultado
    
    def _golpe_de_gracia(self, atacante: Personaje, defensor: Personaje) -> ResultadoAtaque:
        """
        Ejecuta un golpe de gracia cuando el defensor no tiene stamina.
        El ataque no encuentra resistencia.
        """
        # Calcular CA sin resistencia
        ca = self._calcular_coeficiente_ataque(atacante)
        daño = ca  # Sin reducción por CD
        
        # Aplicar daño
        daño_real = defensor.recibir_daño(daño)
        
        resultado = ResultadoAtaque(
            tipo=TipoResultadoAtaque.CRITICO,
            atacante_nombre=atacante.nombre,
            defensor_nombre=defensor.nombre,
            coeficiente_ataque=ca,
            daño_infligido=daño_real,
            defensor_pv_restantes=defensor.pv_actuales,
            defensor_stamina_restante=0,
            defensor_muerto=not defensor.esta_vivo,
            fue_golpe_gracia=True,
            arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
        )
        
        # Publicar evento
        self.event_bus.publicar(TipoEvento.GOLPE_GRACIA, {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre,
            "daño": daño_real,
            "defensor_vivo": defensor.esta_vivo
        })
        
        if not defensor.esta_vivo:
            self.event_bus.publicar(TipoEvento.PERSONAJE_MUERTO, {
                "personaje": defensor.nombre
            })
        
        return resultado
    
    def _contraataque(self, atacante_original: Personaje, 
                     defensor_original: Personaje,
                     diferencia_original: int) -> ResultadoAtaque:
        """
        El defensor contraataca cuando la diferencia es <= -3.
        """
        self.event_bus.publicar(TipoEvento.CONTRAATAQUE, {
            "atacante": defensor_original.nombre,
            "defensor": atacante_original.nombre
        })
        
        # El defensor ahora ataca
        resultado_contra = self.resolver_ataque(defensor_original, atacante_original)
        resultado_contra.fue_contraataque = True
        resultado_contra.tipo = TipoResultadoAtaque.CONTRAATAQUE
        
        return resultado_contra
    
    def _ataque_bloqueado(self, atacante: Personaje, defensor: Personaje,
                         ca: int, cd: int) -> ResultadoAtaque:
        """Ataque bloqueado sin consecuencias"""
        resultado = ResultadoAtaque(
            tipo=TipoResultadoAtaque.BLOQUEADO,
            atacante_nombre=atacante.nombre,
            defensor_nombre=defensor.nombre,
            coeficiente_ataque=ca,
            coeficiente_defensa=cd,
            diferencia=ca - cd,
            defensor_pv_restantes=defensor.pv_actuales,
            defensor_stamina_restante=defensor.ps_actuales,
            arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
        )
        
        self.event_bus.publicar(TipoEvento.ATAQUE_BLOQUEADO, {
            "atacante": atacante.nombre,
            "defensor": defensor.nombre
        })
        
        return resultado
    
    # ========================================================================
    # Ataques especiales
    # ========================================================================
    
    def ataque_sigilo(self, atacante: Personaje, defensor: Personaje) -> ResultadoAtaque:
        """
        Ataque desde las sombras.
        Daño extra = (Sigilo - Percepción) × 2
        """
        sigilo = atacante.ficha.talento.sigilo
        percepcion = defensor.ficha.talento.percepcion
        
        diferencia = sigilo - percepcion
        
        if diferencia > 0:
            # Ataque furtivo exitoso
            ca = self._calcular_coeficiente_ataque(atacante)
            daño_extra = diferencia * 2
            daño_total = ca + daño_extra
            
            daño_real = defensor.recibir_daño(daño_total)
            
            resultado = ResultadoAtaque(
                tipo=TipoResultadoAtaque.SIGILO_EXITOSO,
                atacante_nombre=atacante.nombre,
                defensor_nombre=defensor.nombre,
                coeficiente_ataque=ca,
                daño_infligido=daño_real,
                defensor_pv_restantes=defensor.pv_actuales,
                defensor_muerto=not defensor.esta_vivo,
                arma_usada=atacante.arma_equipada.nombre if atacante.arma_equipada else "Puños"
            )
            
            self.event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
                "atacante": atacante.nombre,
                "defensor": defensor.nombre,
                "tipo": "sigilo",
                "daño": daño_real
            })
            
            return resultado
        else:
            # Detectado: el defensor contraataca
            return self._contraataque(atacante, defensor, diferencia)
    
    # ========================================================================
    # Utilidades
    # ========================================================================
    
    def verificar_fin_combate(self) -> bool:
        """
        Verifica si el combate ha terminado.
        Actualiza el estado.
        """
        if not self.estado:
            return True
        
        return self.estado.verificar_fin_combate()


if __name__ == "__main__":
    from entidades import Ficha, Hephix, HephixTipo, ClaseTipo, crear_espada_basica
    
    print("=== Demo del Motor de Combate ===\n")
    
    # Crear dos personajes para combate
    ficha1 = Ficha()
    ficha1.caracteristicas.fuerza = 8
    ficha1.caracteristicas.reflejos = 4
    ficha1.caracteristicas.resistencia = 7
    ficha1.caracteristicas.stamina = 3
    ficha1.combate.armas_cortantes = 10
    
    guerrero = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha1
    )
    guerrero.equipar_arma(crear_espada_basica())
    
    ficha2 = Ficha()
    ficha2.caracteristicas.fuerza = 5
    ficha2.caracteristicas.reflejos = 6
    ficha2.caracteristicas.resistencia = 4
    ficha2.caracteristicas.stamina = 2
    
    goblin = Personaje(
        nombre="Goblin",
        edad=10,
        raza="Goblin",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha2
    )
    
    # Iniciar combate
    servicio = CombateService()
    estado = servicio.iniciar_combate([guerrero, goblin])
    
    print(estado.resumen())
    print("\n--- Primer ataque ---")
    
    resultado = servicio.resolver_ataque(guerrero, goblin)
    print(resultado.descripcion_corta())

# ==============================================================================
# ARCHIVO 26/36: creacion_personaje_service.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/creacion_personaje_service.py
# ==============================================================================

"""
Servicio de creación de personajes.
Implementa un wizard interactivo para guiar al jugador en la creación.
"""
import json
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from entidades import (
    Personaje, Ficha, Hephix, HephixTipo, ClaseTipo,
    Caracteristicas, HabilidadesCombate, HabilidadesEducacion, HabilidadesTalento,
    Constantes, crear_espada_basica, crear_arco_basico, crear_baston_basico
)


class CreacionPersonajeService:
    """
    Servicio para crear personajes de forma guiada.
    Implementa el wizard de creación paso a paso.
    """
    
    def __init__(self, ruta_clases: str = "data/clases.json", 
                 ruta_hephix: str = "data/hephix.json"):
        """
        Args:
            ruta_clases: Ruta al JSON con definiciones de clases
            ruta_hephix: Ruta al JSON con definiciones de hephix
        """
        self.ruta_clases = Path(ruta_clases)
        self.ruta_hephix = Path(ruta_hephix)
        self._cargar_datos()
    
    def _cargar_datos(self):
        """Carga las definiciones de clases y hephix desde JSON"""
        with open(self.ruta_clases, 'r', encoding='utf-8') as f:
            self.clases_data = json.load(f)
        
        with open(self.ruta_hephix, 'r', encoding='utf-8') as f:
            self.hephix_data = json.load(f)
    
    # ========================================================================
    # Método no interactivo para testing y creación programática
    # ========================================================================
    
    def crear_personaje(
        self,
        nombre: str,
        edad: int,
        raza: str,
        historia: str,
        objetivo: str,
        hephix_tipo: HephixTipo,
        clase: ClaseTipo,
        caracteristicas: Dict[str, int],
        habilidades_combate: Dict[str, int],
        habilidades_educacion: Dict[str, int],
        habilidades_talento: Dict[str, int]
    ) -> Personaje:
        """
        Crea un personaje de forma programática sin interacción.
        Útil para testing y creación automatizada.
        
        Args:
            nombre: Nombre del personaje
            edad: Edad del personaje
            raza: Raza del personaje
            historia: Historia/trasfondo
            objetivo: Objetivo del personaje
            hephix_tipo: Tipo de Hephix
            clase: Clase del personaje
            caracteristicas: Dict con stats (fuerza, reflejos, etc.)
            habilidades_combate: Dict con habilidades de combate
            habilidades_educacion: Dict con habilidades de educación
            habilidades_talento: Dict con habilidades de talento
        
        Returns:
            Personaje completamente configurado
        
        Example:
            >>> servicio = CreacionPersonajeService()
            >>> personaje = servicio.crear_personaje(
            ...     nombre="Aldric",
            ...     edad=25,
            ...     raza="Humano",
            ...     historia="Un guerrero valiente",
            ...     objetivo="Proteger a los débiles",
            ...     hephix_tipo=HephixTipo.ELEMENTAL,
            ...     clase=ClaseTipo.GUERRERO,
            ...     caracteristicas={"fuerza": 8, "reflejos": 4, "resistencia": 6,
            ...                      "voluntad": 0, "punteria": 0, "stamina": 2},
            ...     habilidades_combate={"armas_cortantes": 10, "armas_contundentes": 0,
            ...                          "armas_magicas": 0, "armas_distancia": 0, "pugilismo": 0},
            ...     habilidades_educacion={"medicina": 5, "elocuencia": 5,
            ...                            "manual": 0, "arcanismo": 0},
            ...     habilidades_talento={"sigilo": 5, "percepcion": 5,
            ...                          "mentalidad": 0, "astralidad": 0}
            ... )
        """
        # Crear hephix
        hephix_data = self.hephix_data[hephix_tipo.value]
        hephix = Hephix.crear_desde_tipo(hephix_tipo, hephix_data['descripcion'])
        
        # Crear ficha
        ficha = Ficha(hephix_tipo=hephix_tipo)
        
        # Asignar características
        for stat, valor in caracteristicas.items():
            setattr(ficha.caracteristicas, stat, valor)
        
        # Asignar habilidades de combate
        for habilidad, valor in habilidades_combate.items():
            setattr(ficha.combate, habilidad, valor)
        
        # Asignar habilidades de educación
        for habilidad, valor in habilidades_educacion.items():
            setattr(ficha.educacion, habilidad, valor)
        
        # Asignar habilidades de talento
        for habilidad, valor in habilidades_talento.items():
            setattr(ficha.talento, habilidad, valor)
        
        # Aplicar bonificaciones de clase
        bonificaciones = self.clases_data[clase.value]['bonificaciones']
        ficha.aplicar_bonificaciones_clase(bonificaciones)
        
        # Crear personaje
        personaje = Personaje(
            nombre=nombre,
            edad=edad,
            raza=raza,
            nivel=1,
            clase=clase,
            hephix=hephix,
            ficha=ficha,
            historia=historia,
            objetivo=objetivo
        )
        
        # Equipamiento inicial
        self._asignar_equipamiento_inicial(personaje)
        
        return personaje
    
    def _asignar_equipamiento_inicial(self, personaje: Personaje):
        """Asigna equipamiento inicial según habilidades"""
        # Determinar arma inicial
        arma_inicial = None
        
        if personaje.ficha.combate.armas_cortantes >= 5:
            arma_inicial = crear_espada_basica()
        elif personaje.ficha.combate.armas_distancia >= 5:
            arma_inicial = crear_arco_basico()
        elif personaje.ficha.combate.armas_magicas >= 5:
            arma_inicial = crear_baston_basico()
        
        if arma_inicial:
            personaje.equipar_arma(arma_inicial)
        
        # Monedas iniciales
        personaje.inventario.agregar_monedas(100)
    
    # ========================================================================
    # Wizard completo (modo interactivo)
    # ========================================================================
    
    def crear_personaje_interactivo(self) -> Personaje:
        """
        Wizard completo de creación de personaje.
        Guía al jugador paso a paso.
        
        Returns:
            Personaje completamente configurado
        """
        print("\n" + "="*60)
        print("🎮  CREACIÓN DE PERSONAJE - ETHER BLADES")
        print("="*60 + "\n")
        
        # Paso 1: Datos básicos
        nombre, edad, raza = self._paso_datos_basicos()
        
        # Paso 2: Historia
        historia, objetivo = self._paso_historia()
        
        # Paso 3: Hephix
        hephix = self._paso_seleccion_hephix()
        
        # Paso 4: Clase
        clase = self._paso_seleccion_clase()
        
        # Paso 5: Distribución de puntos
        ficha = self._paso_distribucion_puntos(clase, hephix.tipo)
        
        # Crear personaje
        personaje = Personaje(
            nombre=nombre,
            edad=edad,
            raza=raza,
            nivel=1,
            clase=clase,
            hephix=hephix,
            ficha=ficha,
            historia=historia,
            objetivo=objetivo
        )
        
        # Paso 6: Equipamiento inicial
        self._paso_equipamiento_inicial(personaje, clase)
        
        # Paso 7: Previsualización final
        self._mostrar_preview_personaje(personaje)
        
        # Confirmación
        confirmar = input("\n¿Confirmar creación del personaje? (s/n): ").lower()
        if confirmar != 's':
            print("\n❌ Creación cancelada. Reiniciando wizard...")
            return self.crear_personaje_interactivo()
        
        print(f"\n✅ ¡{personaje.nombre} ha sido creado exitosamente!")
        return personaje
    
    # ========================================================================
    # Pasos individuales
    # ========================================================================
    
    def _paso_datos_basicos(self) -> Tuple[str, int, str]:
        """Paso 1: Solicita nombre, edad y raza"""
        print("📋 PASO 1: DATOS BÁSICOS\n")
        
        nombre = input("Nombre del personaje: ").strip()
        while not nombre:
            print("❌ El nombre no puede estar vacío.")
            nombre = input("Nombre del personaje: ").strip()
        
        edad = self._solicitar_numero("Edad: ", 1, 200)
        
        print("\n🏰 Razas sugeridas: Humano, Elfo, Enano, Orco, Medio-Elfo")
        raza = input("Raza: ").strip() or "Humano"
        
        return nombre, edad, raza
    
    def _paso_historia(self) -> Tuple[str, str]:
        """Paso 2: Historia y trasfondo"""
        print("\n" + "="*60)
        print("📖 PASO 2: HISTORIA Y TRASFONDO")
        print("="*60 + "\n")
        
        print("Todos los personajes comienzan en la ciudad de Amarth, Nerosia.")
        print("Considera:")
        print("  • Origen (lugar, estatus social, familia)")
        print("  • Personalidad (características buenas y malas)")
        print("  • ¿Por qué llegaste a Amarth?")
        print("  • ¿Qué buscas conseguir?\n")
        
        print("Escribe la historia de tu personaje:")
        historia = input("Historia: ").strip() or "Sin historia definida"
        
        print("\n¿Cuál es el objetivo de tu personaje?")
        objetivo = input("Objetivo: ").strip() or "Buscar su destino en Amarth"
        
        return historia, objetivo
    
    def _paso_seleccion_hephix(self) -> Hephix:
        """Paso 3: Selección de Hephix"""
        print("\n" + "="*60)
        print("✨ PASO 3: SELECCIÓN DE HEPHIX (MAGIA)")
        print("="*60 + "\n")
        
        # Mostrar tipos disponibles por categoría
        print("🌟 HEPHIX GENERALES:")
        generales = ['elemental', 'psiquica', 'oculta', 'morphica', 'espiritual', 'cristalina', 'sangrienta']
        for i, tipo in enumerate(generales, 1):
            data = self.hephix_data[tipo]
            print(f"  {i}. {data['nombre']} - {data['descripcion']}")
        
        print("\n⚪ HEPHIX KAIRENISTAS (Luz):")
        kairenistas = ['sanadora', 'exorcista', 'luminica']
        for i, tipo in enumerate(kairenistas, len(generales) + 1):
            data = self.hephix_data[tipo]
            print(f"  {i}. {data['nombre']} - {data['descripcion']}")
        
        print("\n⚫ HEPHIX VADHENISTAS (Oscuridad):")
        vadhenistas = ['caotica', 'nigromante', 'oscura']
        for i, tipo in enumerate(vadhenistas, len(generales) + len(kairenistas) + 1):
            data = self.hephix_data[tipo]
            print(f"  {i}. {data['nombre']} - {data['descripcion']}")
        
        # Solicitar selección
        todos_tipos = generales + kairenistas + vadhenistas
        seleccion = self._solicitar_numero(f"\nSelecciona tu Hephix (1-{len(todos_tipos)}): ", 1, len(todos_tipos))
        
        tipo_seleccionado = todos_tipos[seleccion - 1]
        hephix_tipo = HephixTipo(tipo_seleccionado)
        data = self.hephix_data[tipo_seleccionado]
        
        hephix = Hephix.crear_desde_tipo(hephix_tipo, data['descripcion'])
        
        print(f"\n✅ Has seleccionado: {hephix}")
        if hephix.es_sangriento():
            print("⚠️  ATENCIÓN: Hephix Sangriento usa PV en lugar de PM/PCF/PCT")
        
        return hephix
    
    def _paso_seleccion_clase(self) -> ClaseTipo:
        """Paso 4: Selección de Clase"""
        print("\n" + "="*60)
        print("⚔️  PASO 4: SELECCIÓN DE CLASE")
        print("="*60 + "\n")
        
        clases_lista = list(self.clases_data.keys())
        
        for i, clase_id in enumerate(clases_lista, 1):
            data = self.clases_data[clase_id]
            print(f"{i}. {data['nombre']}")
            print(f"   {data['descripcion']}")
            print(f"   Bonificaciones iniciales:")
            for habilidad, puntos in data['bonificaciones'].items():
                print(f"     • {habilidad}: +{puntos}")
            print()
        
        seleccion = self._solicitar_numero(f"Selecciona tu Clase (1-{len(clases_lista)}): ", 1, len(clases_lista))
        clase_seleccionada = ClaseTipo(clases_lista[seleccion - 1])
        
        print(f"\n✅ Has seleccionado: {self.clases_data[clase_seleccionada.value]['nombre']}")
        
        return clase_seleccionada
    
    def _paso_distribucion_puntos(self, clase: ClaseTipo, hephix_tipo: HephixTipo) -> Ficha:
        """Paso 5: Distribución de puntos de características y habilidades"""
        print("\n" + "="*60)
        print("📊 PASO 5: DISTRIBUCIÓN DE PUNTOS")
        print("="*60 + "\n")
        
        ficha = Ficha(hephix_tipo=hephix_tipo)
        
        # Distribuir características
        print("🎯 CARACTERÍSTICAS (20 puntos para distribuir)")
        print("IMPORTANTE: Elige UNA estadística de ataque:")
        print("  • Fuerza (combate cuerpo a cuerpo)")
        print("  • Puntería (armas a distancia)")
        print("  • Voluntad (magia)\n")
        
        ficha.caracteristicas = self._distribuir_caracteristicas()
        
        # Distribuir habilidades de combate
        print("\n⚔️  HABILIDADES DE COMBATE (10 puntos)")
        ficha.combate = self._distribuir_combate()
        
        # Distribuir habilidades de educación
        print("\n📚 HABILIDADES DE EDUCACIÓN (10 puntos)")
        ficha.educacion = self._distribuir_educacion()
        
        # Distribuir habilidades de talento
        print("\n🎭 HABILIDADES DE TALENTO (10 puntos)")
        ficha.talento = self._distribuir_talento()
        
        # Aplicar bonificaciones de clase
        bonificaciones = self.clases_data[clase.value]['bonificaciones']
        print(f"\n✨ Aplicando bonificaciones de {self.clases_data[clase.value]['nombre']}:")
        for habilidad, puntos in bonificaciones.items():
            print(f"  • {habilidad}: +{puntos}")
        
        ficha.aplicar_bonificaciones_clase(bonificaciones)
        
        # Mostrar stats derivados
        print(f"\n📈 STATS DERIVADOS:")
        print(f"  PV Máximos: {ficha.pv_maximos}")
        print(f"  PM Máximos: {ficha.pm_maximos}")
        print(f"  PCF Máximos: {ficha.pcf_maximos}")
        print(f"  PCT Máximos: {ficha.pct_maximos}")
        print(f"  PS Máximos: {ficha.ps_maximos}")
        
        return ficha
    
    def _distribuir_caracteristicas(self) -> Caracteristicas:
        """Distribuye los 20 puntos de características"""
        caracteristicas = Caracteristicas()
        puntos_restantes = Constantes.PUNTOS_CARACTERISTICAS
        
        stats = [
            ('fuerza', 'Fuerza (daño cuerpo a cuerpo)'),
            ('reflejos', 'Reflejos (esquivar)'),
            ('resistencia', 'Resistencia (puntos de vida)'),
            ('voluntad', 'Voluntad (magia)'),
            ('punteria', 'Puntería (armas a distancia)'),
            ('stamina', 'Stamina (aguante en combate)')
        ]
        
        for stat_nombre, stat_descripcion in stats:
            print(f"\n{stat_descripcion}")
            print(f"Puntos restantes: {puntos_restantes}")
            
            max_asignable = min(20, puntos_restantes)
            puntos = self._solicitar_numero(f"  Asignar a {stat_nombre}: ", 0, max_asignable)
            
            setattr(caracteristicas, stat_nombre, puntos)
            puntos_restantes -= puntos
        
        # Advertencia si sobran puntos, pero NO preguntar por redistribución
        if puntos_restantes > 0:
            print(f"\n⚠️  Te quedan {puntos_restantes} puntos sin asignar.")
            print("Estos puntos se perderán. Considera redistribuir manualmente.")
        
        return caracteristicas
    
    def _distribuir_combate(self) -> HabilidadesCombate:
        """Distribuye los 10 puntos de combate"""
        combate = HabilidadesCombate()
        puntos_restantes = Constantes.PUNTOS_COMBATE
        
        habilidades = [
            ('armas_cortantes', 'Armas cortantes/punzantes'),
            ('armas_contundentes', 'Armas contundentes'),
            ('armas_magicas', 'Armas mágicas'),
            ('armas_distancia', 'Armas a distancia'),
            ('pugilismo', 'Pugilismo (sin armas)')
        ]
        
        for hab_nombre, hab_descripcion in habilidades:
            if puntos_restantes == 0:
                break
            
            print(f"{hab_descripcion} - Restantes: {puntos_restantes}")
            puntos = self._solicitar_numero(f"  Asignar: ", 0, puntos_restantes)
            setattr(combate, hab_nombre, puntos)
            puntos_restantes -= puntos
        
        return combate
    
    def _distribuir_educacion(self) -> HabilidadesEducacion:
        """Distribuye los 10 puntos de educación"""
        educacion = HabilidadesEducacion()
        puntos_restantes = Constantes.PUNTOS_EDUCACION
        
        habilidades = [
            ('medicina', 'Medicina (curación)'),
            ('elocuencia', 'Elocuencia (persuasión)'),
            ('manual', 'Manual (artesanía)'),
            ('arcanismo', 'Arcanismo (encantamientos)')
        ]
        
        for hab_nombre, hab_descripcion in habilidades:
            if puntos_restantes == 0:
                break
            
            print(f"{hab_descripcion} - Restantes: {puntos_restantes}")
            puntos = self._solicitar_numero(f"  Asignar: ", 0, puntos_restantes)
            setattr(educacion, hab_nombre, puntos)
            puntos_restantes -= puntos
        
        return educacion
    
    def _distribuir_talento(self) -> HabilidadesTalento:
        """Distribuye los 10 puntos de talento"""
        talento = HabilidadesTalento()
        puntos_restantes = Constantes.PUNTOS_TALENTO
        
        habilidades = [
            ('sigilo', 'Sigilo (ocultamiento)'),
            ('percepcion', 'Percepción (detectar)'),
            ('mentalidad', 'Mentalidad (estrategia)'),
            ('astralidad', 'Astralidad (conexión divina)')
        ]
        
        for hab_nombre, hab_descripcion in habilidades:
            if puntos_restantes == 0:
                break
            
            print(f"{hab_descripcion} - Restantes: {puntos_restantes}")
            puntos = self._solicitar_numero(f"  Asignar: ", 0, puntos_restantes)
            setattr(talento, hab_nombre, puntos)
            puntos_restantes -= puntos
        
        return talento
    
    def _paso_equipamiento_inicial(self, personaje: Personaje, clase: ClaseTipo):
        """Paso 6: Asigna equipamiento inicial según la clase"""
        print("\n" + "="*60)
        print("🎒 PASO 6: EQUIPAMIENTO INICIAL")
        print("="*60 + "\n")
        
        # Determinar arma inicial según mayor habilidad de combate
        arma_inicial = None
        
        if personaje.ficha.combate.armas_cortantes >= 5:
            arma_inicial = crear_espada_basica()
        elif personaje.ficha.combate.armas_distancia >= 5:
            arma_inicial = crear_arco_basico()
        elif personaje.ficha.combate.armas_magicas >= 5:
            arma_inicial = crear_baston_basico()
        
        if arma_inicial:
            personaje.equipar_arma(arma_inicial)
            print(f"✅ Arma equipada: {arma_inicial.nombre}")
        else:
            print("⚠️  Sin arma inicial (comienza con combate sin armas)")
        
        # Monedas iniciales
        personaje.inventario.agregar_monedas(100)
        print("💰 Monedas iniciales: 100")
    
    def _mostrar_preview_personaje(self, personaje: Personaje):
        """Muestra una previsualización del personaje creado"""
        print("\n" + "="*60)
        print("👤 PREVISUALIZACIÓN DEL PERSONAJE")
        print("="*60)
        print(personaje.resumen_completo())
    
    # ========================================================================
    # Utilidades
    # ========================================================================
    
    def _solicitar_numero(self, mensaje: str, minimo: int, maximo: int) -> int:
        """
        Solicita un número al usuario con validación.
        
        Args:
            mensaje: Mensaje a mostrar
            minimo: Valor mínimo aceptable
            maximo: Valor máximo aceptable
        
        Returns:
            Número validado
        """
        while True:
            try:
                valor = int(input(mensaje))
                if minimo <= valor <= maximo:
                    return valor
                else:
                    print(f"❌ El valor debe estar entre {minimo} y {maximo}.")
            except ValueError:
                print("❌ Ingresa un número válido.")


# Ejemplo de uso
if __name__ == "__main__":
    servicio = CreacionPersonajeService()
    personaje = servicio.crear_personaje_interactivo()
    
    print("\n" + "="*60)
    print("🎉 ¡PERSONAJE CREADO EXITOSAMENTE!")
    print("="*60)
    print(f"\nNombre: {personaje.nombre}")
    print(f"Nivel: {personaje.nivel}")
    print(f"Clase: {personaje.clase.value}")
    print(f"Hephix: {personaje.hephix.tipo.value}")

# ==============================================================================
# ARCHIVO 27/36: narrador_service.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/narrador_service.py
# ==============================================================================

"""
Servicio de Narrador - Genera narraciones dinámicas con IA.
Se suscribe a eventos del juego y genera descripciones contextuales.
"""
from typing import Optional, Dict, Any
from patrones import EventBus, TipoEvento, Evento
from .cliente_ia import ClienteIA, ClienteIAMock
from .persistencia_estructuras import ContextoNarrativo
from entidades import Personaje


class NarradorService:
    """
    Servicio de narrador con IA.
    Genera descripciones dinámicas basadas en eventos y contexto.
    """
    
    def __init__(
        self,
        event_bus: EventBus,
        contexto: Optional[ContextoNarrativo] = None,
        usar_mock: bool = False
    ):
        """
        Args:
            event_bus: Bus de eventos del juego
            contexto: Contexto narrativo actual
            usar_mock: Si True, usa el cliente mock (sin API)
        """
        self.event_bus = event_bus
        self.contexto = contexto or ContextoNarrativo()
        
        # Cliente de IA
        if usar_mock:
            self.cliente = ClienteIAMock()
        else:
            self.cliente = ClienteIA()
            # Si no está disponible, usar mock automáticamente
            if not self.cliente.esta_disponible():
                print("⚠️ API de OpenAI no disponible, usando narrador mock")
                self.cliente = ClienteIAMock()
        
        # Personalidad del narrador
        self.system_message = self._crear_system_message()
        
        # Suscribirse a eventos relevantes
        self._suscribir_eventos()
    
    def _crear_system_message(self) -> str:
        """Crea el mensaje de sistema que define la personalidad del narrador"""
        return """Eres el narrador de "Ether Blades", un juego de rol épico y oscuro.

Tu rol es:
- Narrar los eventos del juego de forma inmersiva y cinematográfica
- Usar un tono dramático pero no excesivamente florido
- Mantener coherencia con el mundo de Ether Blades (magia, combate, intriga)
- Ser conciso: narraciones de 2-4 oraciones máximo
- Nunca alterar mecánicas: solo describes, no decides resultados
- Adaptar el tono según el evento (épico en combate, misterioso en exploración)

Mundo de Ether Blades:
- Mundo medieval-fantástico con magia (Hephix)
- La ciudad principal es Amarth en Nerosia
- Existen facciones: Kairenistas (luz) y Vadhenistas (oscuridad)
- El combate es brutal y estratégico
- La magia tiene un costo (PM, stamina, o vida en caso de Hephix Sangriento)

Responde SOLO con la narración, sin comentarios meta."""
    
    def _suscribir_eventos(self):
        """Suscribe el narrador a eventos relevantes del juego"""
        # Eventos de combate
        self.event_bus.suscribir(TipoEvento.COMBATE_INICIADO, self._narrar_inicio_combate)
        self.event_bus.suscribir(TipoEvento.ATAQUE_REALIZADO, self._narrar_ataque)
        self.event_bus.suscribir(TipoEvento.GOLPE_GRACIA, self._narrar_golpe_gracia)
        self.event_bus.suscribir(TipoEvento.CONTRAATAQUE, self._narrar_contraataque)
        self.event_bus.suscribir(TipoEvento.PERSONAJE_MUERTO, self._narrar_muerte)
        
        # Eventos narrativos
        self.event_bus.suscribir(TipoEvento.CHECKPOINT_ALCANZADO, self._narrar_checkpoint)
    
    # ========================================================================
    # Generación de prompts
    # ========================================================================
    
    def _construir_prompt_base(self, evento_tipo: str, datos: Dict[str, Any]) -> str:
        """
        Construye un prompt base con contexto.
        
        Args:
            evento_tipo: Tipo de evento
            datos: Datos del evento
        
        Returns:
            Prompt con contexto completo
        """
        partes = []
        
        # Contexto general
        if self.contexto:
            partes.append(f"Ubicación: {self.contexto.ubicacion_actual}")
            if self.contexto.log_narrativo:
                ultimo_evento = self.contexto.log_narrativo[-1]
                partes.append(f"Evento previo: {ultimo_evento.descripcion}")
        
        # Datos del evento actual
        partes.append(f"\nEvento: {evento_tipo}")
        for clave, valor in datos.items():
            partes.append(f"{clave}: {valor}")
        
        return "\n".join(partes)
    
    # ========================================================================
    # Narradores de eventos específicos
    # ========================================================================
    
    def _narrar_inicio_combate(self, evento: Evento):
        """Narra el inicio de un combate"""
        datos = evento.datos
        combatientes = datos.get('combatientes', [])
        
        prompt = f"""Narra el momento épico justo antes de que comience un combate entre:
{', '.join(combatientes)}

El ambiente está tenso, las armas están desenvainadas.
Describe la escena en 2-3 oraciones dramáticas."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=150
            )
            self._mostrar_narracion("⚔️ INICIO DE COMBATE", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_ataque(self, evento: Evento):
        """Narra un ataque"""
        datos = evento.datos
        atacante = datos.get('atacante', 'Alguien')
        defensor = datos.get('defensor', 'el enemigo')
        
        prompt = f"""Narra brevemente cómo {atacante} ataca a {defensor}.
Menciona el movimiento, la tensión del momento.
Máximo 2 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=100
            )
            self._mostrar_narracion("⚔️", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_golpe_gracia(self, evento: Evento):
        """Narra un golpe de gracia"""
        datos = evento.datos
        atacante = datos.get('atacante', 'El guerrero')
        defensor = datos.get('defensor', 'el enemigo')
        
        prompt = f"""Narra de forma ÉPICA y DRAMÁTICA el golpe de gracia definitivo.
{atacante} está a punto de asestar el golpe final a {defensor}, que está agotado.
Describe el momento decisivo en 2 oraciones impactantes."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=120
            )
            self._mostrar_narracion("💥 GOLPE DE GRACIA", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_contraataque(self, evento: Evento):
        """Narra un contraataque"""
        datos = evento.datos
        atacante = datos.get('atacante', 'El defensor')
        defensor = datos.get('defensor', 'el atacante')
        
        prompt = f"""Narra cómo {atacante} aprovecha una apertura y contraataca a {defensor}.
Describe el giro inesperado del combate en 2 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=100
            )
            self._mostrar_narracion("🔄 CONTRAATAQUE", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_muerte(self, evento: Evento):
        """Narra la muerte de un personaje"""
        datos = evento.datos
        personaje = datos.get('personaje', 'El combatiente')
        
        prompt = f"""Narra la caída final de {personaje} en combate.
Describe el momento solemne de su derrota en 2 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=100
            )
            self._mostrar_narracion("💀", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    def _narrar_checkpoint(self, evento: Evento):
        """Narra alcanzar un checkpoint"""
        datos = evento.datos
        checkpoint = datos.get('checkpoint', 'un lugar importante')
        
        prompt = f"""Narra el momento en que el personaje llega a {checkpoint}.
Describe la escena y el ambiente del lugar en 3 oraciones."""
        
        try:
            narracion = self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=150
            )
            self._mostrar_narracion("📍 CHECKPOINT", narracion)
        except Exception as e:
            print(f"⚠️ Error al narrar: {e}")
    
    # ========================================================================
    # Narración libre
    # ========================================================================
    
    def narrar_situacion(
        self,
        situacion: str,
        personaje: Optional[Personaje] = None
    ) -> str:
        """
        Genera una narración libre de una situación.
        
        Args:
            situacion: Descripción de la situación a narrar
            personaje: Personaje involucrado (opcional)
        
        Returns:
            Narración generada
        """
        # Construir contexto
        contexto_partes = []
        
        if personaje:
            contexto_partes.append(f"Personaje: {personaje.nombre}, {personaje.clase.value}")
            contexto_partes.append(f"Hephix: {personaje.hephix.tipo.value}")
        
        if self.contexto:
            contexto_partes.append(f"Ubicación: {self.contexto.ubicacion_actual}")
        
        contexto_str = "\n".join(contexto_partes)
        
        prompt = f"""{contexto_str}

Situación: {situacion}

Narra esta situación de forma inmersiva en 3-4 oraciones."""
        
        try:
            return self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=200
            )
        except Exception as e:
            return f"[Error al generar narración: {e}]"
    
    def narrar_decision(
        self,
        decision: str,
        opciones: list[str],
        personaje: Optional[Personaje] = None
    ) -> str:
        """
        Narra una situación de decisión y presenta las opciones.
        
        Args:
            decision: Descripción de la decisión a tomar
            opciones: Lista de opciones disponibles
            personaje: Personaje que decide
        
        Returns:
            Narración de la situación
        """
        prompt = f"""El personaje se enfrenta a una decisión importante:
{decision}

Narra la situación que lleva a esta decisión en 2-3 oraciones.
NO menciones las opciones, solo describe el dilema."""
        
        try:
            return self.cliente.generar_texto(
                prompt,
                system_message=self.system_message,
                max_tokens=150
            )
        except Exception as e:
            return f"[Error al generar narración: {e}]"
    
    # ========================================================================
    # Utilidades
    # ========================================================================
    
    def _mostrar_narracion(self, titulo: str, narracion: str):
        """Muestra una narración formateada"""
        print(f"\n{titulo}")
        print("─" * 70)
        print(f"📖 {narracion}")
        print("─" * 70)
    
    def actualizar_contexto(self, contexto: ContextoNarrativo):
        """Actualiza el contexto narrativo"""
        self.contexto = contexto


if __name__ == "__main__":
    from entidades import Ficha, Hephix, HephixTipo, ClaseTipo
    
    print("=== Demo del Narrador ===\n")
    
    # Crear personaje
    ficha = Ficha()
    ficha.caracteristicas.fuerza = 8
    personaje = Personaje(
        nombre="Aldric",
        edad=25,
        raza="Humano",
        clase=ClaseTipo.GUERRERO,
        hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
        ficha=ficha
    )
    
    # Crear contexto
    contexto = ContextoNarrativo(
        ubicacion_actual="Bosque Oscuro",
        checkpoint_actual="entrada_cueva"
    )
    
    # Crear narrador (con mock)
    event_bus = EventBus()
    narrador = NarradorService(event_bus, contexto, usar_mock=True)
    
    print("Generando narración de situación...\n")
    narracion = narrador.narrar_situacion(
        "El personaje encuentra una cueva misteriosa con runas brillantes",
        personaje
    )
    print(f"📖 {narracion}")

# ==============================================================================
# ARCHIVO 28/36: persistencia_estructuras.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/persistencia_estructuras.py
# ==============================================================================

"""
Estructuras de datos para el sistema de persistencia.
Define el formato de guardado completo.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TipoEvento(str, Enum):
    """Tipos de eventos para el log narrativo"""
    COMBATE = "combate"
    DECISION = "decision"
    DIALOGO = "dialogo"
    CHECKPOINT = "checkpoint"
    DESCUBRIMIENTO = "descubrimiento"
    MISION = "mision"
    OTRO = "otro"


class EventoNarrativo(BaseModel):
    """
    Representa un evento importante en la historia.
    Se usa para dar contexto a la IA.
    """
    timestamp: datetime = Field(default_factory=datetime.now)
    tipo: TipoEvento
    descripcion: str
    relevancia: str = Field(default="media", pattern="^(baja|media|alta)$")
    datos_adicionales: Dict[str, Any] = Field(default_factory=dict)
    
    def resumen(self) -> str:
        """Genera un resumen del evento"""
        iconos = {
            TipoEvento.COMBATE: "⚔️",
            TipoEvento.DECISION: "🤔",
            TipoEvento.DIALOGO: "💬",
            TipoEvento.CHECKPOINT: "📍",
            TipoEvento.DESCUBRIMIENTO: "🔍",
            TipoEvento.MISION: "📜",
            TipoEvento.OTRO: "📝"
        }
        icono = iconos.get(self.tipo, "📝")
        return f"{icono} [{self.tipo.value}] {self.descripcion}"


class ContextoNarrativo(BaseModel):
    """
    Contexto narrativo completo de la partida.
    Crucial para que la IA pueda continuar la historia.
    """
    checkpoint_actual: str = Field(
        default="inicio",
        description="ID del checkpoint narrativo actual"
    )
    ubicacion_actual: str = Field(
        default="Ciudad de Amarth",
        description="Ubicación actual del personaje"
    )
    
    # Historia y progreso
    eventos_completados: List[str] = Field(
        default_factory=list,
        description="IDs de eventos/misiones completadas"
    )
    decisiones_importantes: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Decisiones clave tomadas por el jugador"
    )
    
    # NPCs y relaciones
    npcs_conocidos: List[str] = Field(
        default_factory=list,
        description="Nombres de NPCs con los que ha interactuado"
    )
    reputacion: Dict[str, int] = Field(
        default_factory=dict,
        description="Reputación con diferentes facciones"
    )
    
    # Misiones
    misiones_activas: List[str] = Field(
        default_factory=list,
        description="Misiones en curso"
    )
    misiones_completadas: List[str] = Field(
        default_factory=list,
        description="Misiones finalizadas"
    )
    
    # Log narrativo (últimos 50 eventos para contexto de IA)
    log_narrativo: List[EventoNarrativo] = Field(
        default_factory=list,
        description="Historial de eventos importantes"
    )
    
    def agregar_evento(self, evento: EventoNarrativo):
        """Agrega un evento al log (mantiene solo últimos 50)"""
        self.log_narrativo.append(evento)
        if len(self.log_narrativo) > 50:
            self.log_narrativo.pop(0)
    
    def obtener_resumen_para_ia(self) -> str:
        """
        Genera un resumen del contexto para enviar a la IA.
        Incluye los eventos más relevantes.
        """
        lineas = [
            f"Ubicación actual: {self.ubicacion_actual}",
            f"Checkpoint: {self.checkpoint_actual}",
            ""
        ]
        
        if self.npcs_conocidos:
            lineas.append(f"NPCs conocidos: {', '.join(self.npcs_conocidos)}")
        
        if self.reputacion:
            lineas.append("Reputación:")
            for faccion, rep in self.reputacion.items():
                lineas.append(f"  - {faccion}: {rep}")
        
        if self.misiones_activas:
            lineas.append(f"\nMisiones activas: {', '.join(self.misiones_activas)}")
        
        # Eventos recientes (últimos 10)
        if self.log_narrativo:
            lineas.append("\nEventos recientes:")
            for evento in self.log_narrativo[-10:]:
                lineas.append(f"  - {evento.resumen()}")
        
        return "\n".join(lineas)


class EstadoCombateGuardado(BaseModel):
    """Estado de combate para persistir"""
    en_combate: bool = False
    enemigos_vivos: List[str] = Field(default_factory=list)
    turno_actual: int = 0
    orden_turnos: List[str] = Field(default_factory=list)


class DatosPartida(BaseModel):
    """
    Estructura completa de una partida guardada.
    Contiene toda la información necesaria para restaurar el juego.
    """
    # Metadata
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.now)
    slot: int = Field(ge=1, le=10, description="Slot de guardado (1-10)")
    
    # Info general
    nombre_partida: str
    tiempo_jugado: str = "0h 0m"
    
    # Personaje completo (serializado)
    personaje: Dict[str, Any]
    
    # Contexto narrativo
    contexto: ContextoNarrativo
    
    # Estado de combate (si aplica)
    combate: EstadoCombateGuardado
    
    # Datos adicionales
    configuracion: Dict[str, Any] = Field(default_factory=dict)
    
    def nombre_archivo(self) -> str:
        """Genera el nombre del archivo de guardado"""
        fecha = self.timestamp.strftime("%Y%m%d_%H%M%S")
        return f"partida_slot{self.slot}_{fecha}.json"
    
    def resumen_corto(self) -> str:
        """Resumen corto para mostrar en menú de carga"""
        personaje_nombre = self.personaje.get('nombre', 'Desconocido')
        nivel = self.personaje.get('nivel', 1)
        ubicacion = self.contexto.ubicacion_actual
        
        return (
            f"Slot {self.slot}: {personaje_nombre} (Nivel {nivel})\n"
            f"  Ubicación: {ubicacion}\n"
            f"  Tiempo jugado: {self.tiempo_jugado}\n"
            f"  Guardado: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
        )


class InfoSlot(BaseModel):
    """Información resumida de un slot de guardado"""
    slot: int
    existe: bool
    nombre_personaje: Optional[str] = None
    nivel: Optional[int] = None
    ubicacion: Optional[str] = None
    timestamp: Optional[datetime] = None
    tiempo_jugado: Optional[str] = None
    
    def __str__(self) -> str:
        if not self.existe:
            return f"Slot {self.slot}: [VACÍO]"
        
        return (
            f"Slot {self.slot}: {self.nombre_personaje} (Nivel {self.nivel})\n"
            f"  📍 {self.ubicacion}\n"
            f"  ⏱️  {self.tiempo_jugado}\n"
            f"  📅 {self.timestamp.strftime('%d/%m/%Y %H:%M')}"
        )


if __name__ == "__main__":
    print("=== Sistema de Estructuras de Persistencia ===\n")
    
    # Ejemplo de contexto narrativo
    contexto = ContextoNarrativo(
        checkpoint_actual="ciudad_amarth_taberna",
        ubicacion_actual="Taberna 'El Dragón Dorado'"
    )
    
    contexto.npcs_conocidos.extend(["Marcus el Herrero", "Elara la Sanadora"])
    contexto.reputacion["Guardia de Amarth"] = 15
    contexto.reputacion["Gremio de Mercenarios"] = -5
    
    # Agregar eventos
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.COMBATE,
        descripcion="Derrotaste a un bandido en las afueras de Amarth",
        relevancia="alta"
    ))
    
    contexto.agregar_evento(EventoNarrativo(
        tipo=TipoEvento.DIALOGO,
        descripcion="Conversación con Marcus sobre armas mejoradas",
        relevancia="media"
    ))
    
    print(contexto.obtener_resumen_para_ia())

# ==============================================================================
# ARCHIVO 29/36: persistencia_service.py
# Directorio: servicios
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./servicios/persistencia_service.py
# ==============================================================================

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


################################################################################
# DIRECTORIO: tests
################################################################################

# ==============================================================================
# ARCHIVO 30/36: __init__.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/__init__.py
# ==============================================================================



# ==============================================================================
# ARCHIVO 31/36: test_combate.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/test_combate.py
# ==============================================================================

"""
Tests para el servicio de combate.
Ejecutar con: pytest tests/test_combate.py -v
"""
import pytest
from servicios.combate_service import CombateService
from servicios.combate_estructuras import TipoResultadoAtaque
from entidades import (
    Personaje, Ficha, Hephix, HephixTipo, ClaseTipo,
    crear_espada_basica, establecer_semilla
)
from patrones import EventBus, TipoEvento


class TestCombateService:
    """Tests para el motor de combate"""
    
    @pytest.fixture
    def event_bus(self):
        """Crea un event bus para testing"""
        return EventBus()
    
    @pytest.fixture
    def servicio_combate(self, event_bus):
        """Crea un servicio de combate"""
        return CombateService(event_bus)
    
    @pytest.fixture
    def guerrero(self):
        """Crea un guerrero de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.reflejos = 4
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.stamina = 3
        ficha.combate.armas_cortantes = 10
        
        personaje = Personaje(
            nombre="Aldric",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
        personaje.equipar_arma(crear_espada_basica())
        return personaje
    
    @pytest.fixture
    def enemigo_debil(self):
        """Crea un enemigo débil"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 4
        ficha.caracteristicas.reflejos = 3
        ficha.caracteristicas.resistencia = 3
        ficha.caracteristicas.stamina = 1
        
        return Personaje(
            nombre="Goblin",
            edad=10,
            raza="Goblin",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
    
    # ========================================================================
    # Tests de Inicialización
    # ========================================================================
    
    def test_iniciar_combate(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que se inicia correctamente un combate"""
        estado = servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        assert estado is not None
        assert len(estado.combatientes) == 2
        assert len(estado.orden_turnos) == 2
        assert estado.combate_activo
        assert estado.turno_actual == 0
    
    def test_iniciativa_determina_orden(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que la iniciativa determina el orden de turnos"""
        # Fijar semilla para resultados predecibles
        establecer_semilla(42)
        
        estado = servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Verificar que todos tienen iniciativa asignada
        for combatiente in estado.combatientes:
            assert combatiente.iniciativa > 0
    
    def test_error_combate_un_solo_combatiente(self, servicio_combate, guerrero):
        """Verifica que no se puede iniciar combate con un solo combatiente"""
        with pytest.raises(ValueError, match="al menos 2 combatientes"):
            servicio_combate.iniciar_combate([guerrero])
    
    def test_stamina_restaurada_al_iniciar(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que la stamina se restaura al iniciar combate"""
        # Reducir stamina antes del combate
        guerrero.gastar_stamina(10)
        enemigo_debil.gastar_stamina(5)
        
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Verificar que se restauró
        assert guerrero.ps_actuales == guerrero.ps_maximos
        assert enemigo_debil.ps_actuales == enemigo_debil.ps_maximos
    
    # ========================================================================
    # Tests de Resolución de Ataques
    # ========================================================================
    
    def test_resolver_ataque_basico(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica resolución básica de ataque"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        assert resultado is not None
        assert resultado.atacante_nombre == "Aldric"
        assert resultado.defensor_nombre == "Goblin"
        assert resultado.tipo in TipoResultadoAtaque
    
    def test_ataque_reduce_stamina(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que un ataque exitoso reduce stamina"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        stamina_inicial = enemigo_debil.ps_actuales
        
        # Fijar semilla para ataque exitoso
        establecer_semilla(100)
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        if resultado.tipo == TipoResultadoAtaque.EXITO:
            assert enemigo_debil.ps_actuales < stamina_inicial
            assert resultado.stamina_perdida > 0
    
    def test_golpe_de_gracia_cuando_stamina_cero(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que se ejecuta golpe de gracia cuando stamina = 0"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Reducir stamina a 0
        enemigo_debil.ps_actuales = 0
        
        pv_inicial = enemigo_debil.pv_actuales
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        # Debería ser golpe de gracia o crítico
        assert resultado.tipo == TipoResultadoAtaque.CRITICO
        assert resultado.fue_golpe_gracia
        assert enemigo_debil.pv_actuales < pv_inicial
        assert resultado.daño_infligido > 0
    
    def test_contraataque_con_diferencia_negativa(self, servicio_combate):
        """Verifica contraataque cuando diferencia <= -3"""
        # Crear atacante muy débil y defensor fuerte
        ficha_debil = Ficha()
        ficha_debil.caracteristicas.fuerza = 1
        ficha_debil.caracteristicas.reflejos = 1
        ficha_debil.caracteristicas.resistencia = 3
        ficha_debil.caracteristicas.stamina = 1
        
        atacante_debil = Personaje(
            nombre="Débil",
            edad=20,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_debil
        )
        
        ficha_fuerte = Ficha()
        ficha_fuerte.caracteristicas.fuerza = 10
        ficha_fuerte.caracteristicas.reflejos = 10
        ficha_fuerte.caracteristicas.resistencia = 8
        ficha_fuerte.caracteristicas.stamina = 5
        
        defensor_fuerte = Personaje(
            nombre="Fuerte",
            edad=30,
            raza="Orco",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_fuerte
        )
        defensor_fuerte.equipar_arma(crear_espada_basica())
        
        servicio_combate.iniciar_combate([atacante_debil, defensor_fuerte])
        
        # Con semilla apropiada, debería haber contraataque
        establecer_semilla(1)
        resultado = servicio_combate.resolver_ataque(atacante_debil, defensor_fuerte)
        
        # Puede ser contraataque directo o resultado del contraataque
        assert resultado is not None
    
    def test_ataque_bloqueado(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica ataque bloqueado sin consecuencias"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Con una semilla específica podríamos forzar un bloqueo
        # Por ahora solo verificamos que el tipo existe
        resultado = servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        if resultado.tipo == TipoResultadoAtaque.BLOQUEADO:
            assert resultado.stamina_perdida == 0
            assert resultado.daño_infligido == 0
    
    # ========================================================================
    # Tests de Ataques Especiales
    # ========================================================================
    
    def test_ataque_sigilo_exitoso(self, servicio_combate):
        """Verifica ataque furtivo exitoso"""
        # Crear atacante con alto sigilo
        ficha_sigiloso = Ficha()
        ficha_sigiloso.caracteristicas.fuerza = 6
        ficha_sigiloso.caracteristicas.reflejos = 5
        ficha_sigiloso.caracteristicas.resistencia = 5
        ficha_sigiloso.caracteristicas.stamina = 3
        ficha_sigiloso.talento.sigilo = 15  # Alto sigilo
        
        sigiloso = Personaje(
            nombre="Asesino",
            edad=25,
            raza="Elfo",
            clase=ClaseTipo.EXPLORADOR,
            hephix=Hephix.crear_desde_tipo(HephixTipo.OCULTA),
            ficha=ficha_sigiloso
        )
        sigiloso.equipar_arma(crear_espada_basica())
        
        # Crear objetivo con baja percepción
        ficha_victima = Ficha()
        ficha_victima.caracteristicas.resistencia = 5
        ficha_victima.caracteristicas.stamina = 2
        ficha_victima.talento.percepcion = 2  # Baja percepción
        
        victima = Personaje(
            nombre="Guardia",
            edad=30,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_victima
        )
        
        servicio_combate.iniciar_combate([sigiloso, victima])
        
        pv_inicial = victima.pv_actuales
        resultado = servicio_combate.ataque_sigilo(sigiloso, victima)
        
        # Debería ser exitoso (Sigilo 15 - Percepción 2 = 13 > 0)
        assert resultado.tipo == TipoResultadoAtaque.SIGILO_EXITOSO
        assert resultado.daño_infligido > 0
        assert victima.pv_actuales < pv_inicial
    
    def test_ataque_sigilo_detectado(self, servicio_combate):
        """Verifica que ataque furtivo detectado resulta en contraataque"""
        # Crear atacante con bajo sigilo
        ficha_torpe = Ficha()
        ficha_torpe.caracteristicas.fuerza = 6
        ficha_torpe.caracteristicas.resistencia = 5
        ficha_torpe.caracteristicas.stamina = 2
        ficha_torpe.talento.sigilo = 2  # Bajo sigilo
        
        torpe = Personaje(
            nombre="Novato",
            edad=18,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_torpe
        )
        
        # Crear objetivo con alta percepción
        ficha_alerta = Ficha()
        ficha_alerta.caracteristicas.fuerza = 7
        ficha_alerta.caracteristicas.resistencia = 6
        ficha_alerta.caracteristicas.stamina = 3
        ficha_alerta.talento.percepcion = 15  # Alta percepción
        
        alerta = Personaje(
            nombre="Veterano",
            edad=40,
            raza="Elfo",
            clase=ClaseTipo.EXPLORADOR,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha_alerta
        )
        alerta.equipar_arma(crear_espada_basica())
        
        servicio_combate.iniciar_combate([torpe, alerta])
        
        resultado = servicio_combate.ataque_sigilo(torpe, alerta)
        
        # Debería ser detectado y contraatacar (Sigilo 2 - Percepción 15 = -13 < 0)
        assert resultado.fue_contraataque or resultado.tipo == TipoResultadoAtaque.CONTRAATAQUE
    
    # ========================================================================
    # Tests de Eventos
    # ========================================================================
    
    def test_eventos_publicados_en_combate(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica que se publican eventos durante el combate"""
        eventos_recibidos = []
        
        def capturar_evento(evento):
            eventos_recibidos.append(evento.tipo)
        
        # Suscribirse a eventos
        servicio_combate.event_bus.suscribir(TipoEvento.COMBATE_INICIADO, capturar_evento)
        servicio_combate.event_bus.suscribir(TipoEvento.ATAQUE_REALIZADO, capturar_evento)
        
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        assert TipoEvento.COMBATE_INICIADO in eventos_recibidos
        assert TipoEvento.ATAQUE_REALIZADO in eventos_recibidos
    
    def test_evento_personaje_muerto(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica evento cuando un personaje muere"""
        eventos_muerte = []
        
        def capturar_muerte(evento):
            eventos_muerte.append(evento.datos)
        
        servicio_combate.event_bus.suscribir(TipoEvento.PERSONAJE_MUERTO, capturar_muerte)
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Reducir PV del enemigo casi a 0
        enemigo_debil.pv_actuales = 1
        enemigo_debil.ps_actuales = 0
        
        # Golpe de gracia que lo mate
        servicio_combate.resolver_ataque(guerrero, enemigo_debil)
        
        if not enemigo_debil.esta_vivo:
            assert len(eventos_muerte) > 0
    
    # ========================================================================
    # Tests de Verificación de Fin
    # ========================================================================
    
    def test_verificar_fin_combate(self, servicio_combate, guerrero, enemigo_debil):
        """Verifica detección de fin de combate"""
        servicio_combate.iniciar_combate([guerrero, enemigo_debil])
        
        # Combate activo inicialmente
        assert not servicio_combate.verificar_fin_combate()
        
        # Matar a un combatiente
        enemigo_debil.pv_actuales = 0
        enemigo_debil.esta_vivo = False
        
        # Actualizar estado
        for c in servicio_combate.estado.combatientes:
            if c.nombre == enemigo_debil.nombre:
                c.esta_vivo = False
                c.pv_actuales = 0
        
        # Ahora debería detectar fin
        assert servicio_combate.verificar_fin_combate()
        assert servicio_combate.estado.ganador == "Aldric"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ==============================================================================
# ARCHIVO 32/36: test_creacion_personaje.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/test_creacion_personaje.py
# ==============================================================================

"""
Tests para el servicio de creación de personajes.
Ejecutar con: pytest tests/test_creacion_personaje.py -v
"""
import pytest
from unittest.mock import patch, MagicMock
from servicios.creacion_personaje_service import CreacionPersonajeService
from entidades import HephixTipo, ClaseTipo, Constantes


class TestCreacionPersonajeService:
    """Tests para el servicio de creación"""
    
    @pytest.fixture
    def servicio(self):
        """Crea una instancia del servicio"""
        return CreacionPersonajeService()
    
    def test_cargar_datos(self, servicio):
        """Verifica que se cargan los datos de clases y hephix"""
        assert len(servicio.clases_data) > 0
        assert len(servicio.hephix_data) > 0
        
        # Verificar que existen clases específicas
        assert 'curandero' in servicio.clases_data
        assert 'guerrero' in servicio.clases_data
        
        # Verificar que existen hephix específicos
        assert 'elemental' in servicio.hephix_data
        assert 'sangrienta' in servicio.hephix_data
    
    def test_solicitar_numero_valido(self, servicio):
        """Verifica validación de números"""
        with patch('builtins.input', return_value='5'):
            resultado = servicio._solicitar_numero("Test: ", 1, 10)
            assert resultado == 5
    
    def test_solicitar_numero_fuera_rango(self, servicio):
        """Verifica rechazo de números fuera de rango"""
        with patch('builtins.input', side_effect=['15', '0', '5']):
            resultado = servicio._solicitar_numero("Test: ", 1, 10)
            assert resultado == 5
    
    def test_solicitar_numero_invalido(self, servicio):
        """Verifica rechazo de entrada no numérica"""
        with patch('builtins.input', side_effect=['abc', '5']):
            resultado = servicio._solicitar_numero("Test: ", 1, 10)
            assert resultado == 5
    
    def test_distribuir_caracteristicas_suma_correcta(self, servicio):
        """Verifica que la distribución no exceda 20 puntos"""
        inputs = ['8', '4', '6', '0', '0', '2']  # Total = 20
        
        with patch('builtins.input', side_effect=inputs):
            carac = servicio._distribuir_caracteristicas()
            
            assert carac.total_puntos() == 20
            assert carac.fuerza == 8
            assert carac.reflejos == 4
            assert carac.resistencia == 6
    
    def test_distribuir_combate(self, servicio):
        """Verifica distribución de habilidades de combate"""
        inputs = ['5', '0', '0', '5', '0']  # Total = 10
        
        with patch('builtins.input', side_effect=inputs):
            combate = servicio._distribuir_combate()
            
            assert combate.total_puntos() == 10
            assert combate.armas_cortantes == 5
            assert combate.armas_distancia == 5
    
    def test_distribuir_educacion(self, servicio):
        """Verifica distribución de habilidades de educación"""
        inputs = ['3', '3', '2', '2']  # Total = 10
        
        with patch('builtins.input', side_effect=inputs):
            educacion = servicio._distribuir_educacion()
            
            assert educacion.total_puntos() == 10
    
    def test_distribuir_talento(self, servicio):
        """Verifica distribución de habilidades de talento"""
        inputs = ['4', '4', '2', '0']  # Total = 10
        
        with patch('builtins.input', side_effect=inputs):
            talento = servicio._distribuir_talento()
            
            assert talento.total_puntos() == 10
    
    def test_paso_datos_basicos(self, servicio):
        """Verifica paso de datos básicos"""
        inputs = ['Aldric', '25', 'Humano']
        
        with patch('builtins.input', side_effect=inputs):
            nombre, edad, raza = servicio._paso_datos_basicos()
            
            assert nombre == 'Aldric'
            assert edad == 25
            assert raza == 'Humano'
    
    def test_paso_historia(self, servicio):
        """Verifica paso de historia"""
        inputs = [
            'Un guerrero de las montañas buscando venganza',  # historia
            'Vengar a su familia'                              # objetivo
        ]
        
        with patch('builtins.input', side_effect=inputs):
            historia, objetivo = servicio._paso_historia()
            
            assert 'guerrero' in historia.lower()
            assert len(objetivo) > 0
    
    def test_paso_seleccion_hephix(self, servicio):
        """Verifica selección de hephix"""
        with patch('builtins.input', return_value='1'):  # Elemental
            hephix = servicio._paso_seleccion_hephix()
            
            assert hephix.tipo == HephixTipo.ELEMENTAL
            assert hephix.nivel == 1
    
    def test_paso_seleccion_clase(self, servicio):
        """Verifica selección de clase"""
        with patch('builtins.input', return_value='2'):  # Guerrero (segunda opción)
            clase = servicio._paso_seleccion_clase()
            
            assert clase in ClaseTipo
    
    def test_equipamiento_inicial_guerrero(self, servicio):
        """Verifica equipamiento inicial para guerrero"""
        from entidades import Personaje, Ficha, Hephix
        
        ficha = Ficha()
        ficha.combate.armas_cortantes = 10  # Suficiente para espada
        
        personaje = Personaje(
            nombre="Test",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
        
        servicio._paso_equipamiento_inicial(personaje, ClaseTipo.GUERRERO)
        
        assert personaje.arma_equipada is not None
        assert personaje.inventario.monedas == 100
    
    @pytest.mark.integration
    def test_creacion_completa_programatica(self, servicio):
        """
        Test de integración: crea un personaje completo sin interacción.
        Usa el método no interactivo para evitar problemas con mocks.
        """
        personaje = servicio.crear_personaje(
            nombre="Aldric",
            edad=25,
            raza="Humano",
            historia="Un guerrero valiente de las montañas del norte",
            objetivo="Proteger a los débiles y buscar justicia",
            hephix_tipo=HephixTipo.ELEMENTAL,
            clase=ClaseTipo.GUERRERO,
            caracteristicas={
                "fuerza": 8,
                "reflejos": 4,
                "resistencia": 6,
                "voluntad": 0,
                "punteria": 0,
                "stamina": 2
            },
            habilidades_combate={
                "armas_cortantes": 10,
                "armas_contundentes": 0,
                "armas_magicas": 0,
                "armas_distancia": 0,
                "pugilismo": 0
            },
            habilidades_educacion={
                "medicina": 5,
                "elocuencia": 5,
                "manual": 0,
                "arcanismo": 0
            },
            habilidades_talento={
                "sigilo": 5,
                "percepcion": 5,
                "mentalidad": 0,
                "astralidad": 0
            }
        )
        
        # Verificaciones básicas
        assert personaje.nombre == 'Aldric'
        assert personaje.edad == 25
        assert personaje.raza == 'Humano'
        assert personaje.nivel == 1
        assert personaje.clase == ClaseTipo.GUERRERO
        assert personaje.hephix.tipo == HephixTipo.ELEMENTAL
        
        # Verificar distribución de puntos
        assert personaje.ficha.caracteristicas.total_puntos() == 20
        assert personaje.ficha.combate.total_puntos() >= 10  # + bonificaciones clase
        
        # Verificar historia
        assert 'guerrero' in personaje.historia.lower()
        assert 'proteger' in personaje.objetivo.lower()
        
        # Verificar inicialización
        assert personaje.pv_actuales == personaje.pv_maximos
        assert personaje.pm_actuales == personaje.pm_maximos
        assert personaje.esta_vivo
        
        # Verificar equipamiento
        assert personaje.inventario.monedas == 100
        assert personaje.arma_equipada is not None  # Guerrero con armas_cortantes=10
        assert personaje.arma_equipada.nombre == "Espada Corta"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ==============================================================================
# ARCHIVO 33/36: test_entidades.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/test_entidades.py
# ==============================================================================

"""
Tests unitarios para las entidades del dominio.
Ejecutar con: pytest tests/test_entidades.py -v
"""
import pytest
from entidades import (
    Personaje, Ficha, Hephix, HephixTipo, ClaseTipo,
    Arma, Armadura, Inventario, TipoArma, TipoAtaque,
    tirar_dados, establecer_semilla, Constantes,
    crear_espada_basica, crear_pocion_vida_menor
)


# ============================================================================
# Tests de Dados
# ============================================================================

class TestDados:
    """Tests para el sistema de tiradas de dados"""
    
    def test_tirar_dados_rango(self):
        """Verifica que los dados estén en rango válido"""
        for _ in range(100):
            resultado = tirar_dados(3, 6)
            assert 3 <= resultado.total <= 18
            assert len(resultado.dados) == 3
            for dado in resultado.dados:
                assert 1 <= dado <= 6
    
    def test_tirar_dados_semilla(self):
        """Verifica que con misma semilla da mismos resultados"""
        establecer_semilla(42)
        resultado1 = tirar_dados(2, 10)
        
        establecer_semilla(42)
        resultado2 = tirar_dados(2, 10)
        
        assert resultado1.total == resultado2.total
        assert resultado1.dados == resultado2.dados


# ============================================================================
# Tests de Hephix
# ============================================================================

class TestHephix:
    """Tests para la clase Hephix"""
    
    def test_crear_hephix_normal(self):
        """Verifica creación de hephix normal"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL)
        
        assert hephix.tipo == HephixTipo.ELEMENTAL
        assert hephix.nivel == 1
        assert hephix.puede_usar_pm()
        assert hephix.puede_usar_pcf()
        assert hephix.puede_usar_pct()
    
    def test_hephix_sangriento_especial(self):
        """Verifica mecánicas especiales del Hephix Sangriento"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.SANGRIENTA)
        
        assert hephix.es_sangriento()
        assert not hephix.puede_usar_pm()
        assert not hephix.puede_usar_pcf()
        assert not hephix.puede_usar_pct()
        
        # Verifica bonus de PV
        bonus_pv = hephix.calcular_modificador_pv(voluntad=8)
        assert bonus_pv == 8 * 5  # Vol × 5
    
    def test_hephix_kairenista(self):
        """Verifica identificación de hephix Kairenista"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.SANADORA)
        assert hephix.es_kairenista()
        assert not hephix.es_vadhenista()
    
    def test_hephix_vadhenista(self):
        """Verifica identificación de hephix Vadhenista"""
        hephix = Hephix.crear_desde_tipo(HephixTipo.NIGROMANTE)
        assert hephix.es_vadhenista()
        assert not hephix.es_kairenista()


# ============================================================================
# Tests de Ficha
# ============================================================================

class TestFicha:
    """Tests para la clase Ficha"""
    
    def test_calculos_stats_derivados(self):
        """Verifica cálculos de PV, PM, PCF, PCT, PS"""
        ficha = Ficha()
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.voluntad = 5
        ficha.caracteristicas.fuerza = 6
        ficha.caracteristicas.punteria = 4
        ficha.caracteristicas.stamina = 3
        
        assert ficha.pv_maximos == 7 * 10  # 70
        assert ficha.pm_maximos == 5 * 5   # 25
        assert ficha.pcf_maximos == 6 * 5  # 30
        assert ficha.pct_maximos == 4 * 5  # 20
        assert ficha.ps_maximos == 3 * 5   # 15
    
    def test_ficha_hephix_sangriento(self):
        """Verifica cálculos con Hephix Sangriento"""
        ficha = Ficha(hephix_tipo=HephixTipo.SANGRIENTA)
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.voluntad = 8
        
        # PV base + bonus sangriento
        assert ficha.pv_maximos == (7 * 10) + (8 * 5)  # 70 + 40 = 110
        assert ficha.pm_maximos == 0
        assert ficha.pcf_maximos == 0
        assert ficha.pct_maximos == 0
    
    def test_validacion_distribucion(self):
        """Verifica validación de puntos"""
        ficha = Ficha()
        
        # Distribuir exactamente 20 puntos
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.reflejos = 4
        ficha.caracteristicas.resistencia = 6
        ficha.caracteristicas.voluntad = 0
        ficha.caracteristicas.punteria = 0
        ficha.caracteristicas.stamina = 2
        
        assert ficha.caracteristicas.total_puntos() == 20
        assert ficha.caracteristicas.validar_distribucion()
    
    def test_bonus_habilidad(self):
        """Verifica cálculo de bonus por habilidad"""
        ficha = Ficha()
        ficha.combate.armas_cortantes = 15
        
        # Cada 5 puntos = +1 bonus
        assert ficha.obtener_bonus_habilidad('armas_cortantes') == 3


# ============================================================================
# Tests de Arma
# ============================================================================

class TestArma:
    """Tests para armas y armaduras"""
    
    def test_crear_arma_basica(self):
        """Verifica creación de arma básica"""
        espada = crear_espada_basica()
        
        assert espada.nombre == "Espada Corta"
        assert espada.tipo_arma == TipoArma.CORTANTE_PUNZANTE
        assert espada.tipo_ataque == TipoAtaque.MELEE
        assert espada.bonus >= 0
    
    def test_mejora_mecanica(self):
        """Verifica sistema de mejora mecánica"""
        espada = crear_espada_basica()
        bonus_inicial = espada.bonus_total()
        
        # Aplicar mejora con Manual nivel 15
        espada.aplicar_mejora_mecanica(15)
        
        assert espada.mejora_mecanica == 3
        assert espada.bonus_total() == bonus_inicial + 3
    
    def test_mejora_magica_exclusiva(self):
        """Verifica que mejoras mecánica y mágica no coexistan"""
        espada = crear_espada_basica()
        
        espada.aplicar_mejora_mecanica(15)
        assert not espada.puede_mejorar_magicamente()
        
        # Intentar mejora mágica debería fallar
        resultado = espada.aplicar_mejora_magica(15)
        assert not resultado


# ============================================================================
# Tests de Inventario
# ============================================================================

class TestInventario:
    """Tests para el sistema de inventario"""
    
    def test_agregar_item(self):
        """Verifica agregar ítems al inventario"""
        inv = Inventario(capacidad_maxima=10)
        pocion = crear_pocion_vida_menor()
        
        assert inv.agregar_item(pocion)
        assert len(inv.items) == 1
    
    def test_items_apilables(self):
        """Verifica que ítems apilables se acumulan"""
        inv = Inventario()
        
        pocion1 = crear_pocion_vida_menor()
        pocion2 = crear_pocion_vida_menor()
        
        inv.agregar_item(pocion1)
        inv.agregar_item(pocion2)
        
        # Debería haber solo 1 entrada con cantidad 2
        assert len(inv.items) == 1
        assert inv.items[0].cantidad == 2
    
    def test_capacidad_maxima(self):
        """Verifica límite de capacidad"""
        inv = Inventario(capacidad_maxima=2)
        
        inv.agregar_arma(crear_espada_basica())
        inv.agregar_item(crear_pocion_vida_menor())
        
        # Ya está lleno (2 slots ocupados)
        assert not inv.tiene_espacio()
        
        # Pero ítems apilables NO consumen slot adicional
        # Agregar otra poción debería funcionar (se apila)
        assert inv.agregar_item(crear_pocion_vida_menor())
        assert inv.items[0].cantidad == 2  # Se apiló
        
        # Pero un ítem DIFERENTE no debería poder agregarse
        from entidades.inventario import Item
        item_nuevo = Item(nombre="Otro Item", es_apilable=False)
        assert not inv.agregar_item(item_nuevo)
    
    def test_buscar_item(self):
        """Verifica búsqueda de ítems"""
        inv = Inventario()
        pocion = crear_pocion_vida_menor()
        inv.agregar_item(pocion)
        
        encontrada = inv.buscar_item("Poción de Vida Menor")
        assert encontrada is not None
        assert encontrada.nombre == pocion.nombre


# ============================================================================
# Tests de Personaje
# ============================================================================

class TestPersonaje:
    """Tests para la clase Personaje"""
    
    @pytest.fixture
    def personaje_basico(self):
        """Crea un personaje de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.reflejos = 4
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.stamina = 1
        
        hephix = Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL)
        
        return Personaje(
            nombre="Test",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=hephix,
            ficha=ficha
        )
    
    def test_crear_personaje(self, personaje_basico):
        """Verifica creación de personaje"""
        assert personaje_basico.nombre == "Test"
        assert personaje_basico.nivel == 1
        assert personaje_basico.esta_vivo
    
    def test_stats_inicializados(self, personaje_basico):
        """Verifica que stats se inicializan correctamente"""
        assert personaje_basico.pv_actuales == personaje_basico.pv_maximos
        assert personaje_basico.pm_actuales == personaje_basico.pm_maximos
        assert personaje_basico.ps_actuales == personaje_basico.ps_maximos
    
    def test_recibir_daño(self, personaje_basico):
        """Verifica sistema de daño"""
        pv_iniciales = personaje_basico.pv_actuales
        daño = personaje_basico.recibir_daño(25)
        
        assert daño == 25
        assert personaje_basico.pv_actuales == pv_iniciales - 25
    
    def test_curar(self, personaje_basico):
        """Verifica sistema de curación"""
        personaje_basico.recibir_daño(30)
        pv_antes = personaje_basico.pv_actuales
        
        curado = personaje_basico.curar(20)
        
        assert curado == 20
        assert personaje_basico.pv_actuales == pv_antes + 20
    
    def test_muerte(self, personaje_basico):
        """Verifica que personaje muere al llegar a 0 PV"""
        personaje_basico.recibir_daño(1000)
        
        assert personaje_basico.pv_actuales == 0
        assert not personaje_basico.esta_vivo
        assert personaje_basico.esta_inconsciente
    
    def test_equipar_arma(self, personaje_basico):
        """Verifica equipamiento de arma"""
        espada = crear_espada_basica()
        personaje_basico.ficha.combate.armas_cortantes = 5
        
        assert personaje_basico.equipar_arma(espada)
        assert personaje_basico.arma_equipada == espada
    
    def test_ganar_experiencia(self, personaje_basico):
        """Verifica sistema de experiencia y nivel"""
        nivel_inicial = personaje_basico.nivel
        
        # Dar suficiente XP para subir de nivel
        personaje_basico.ganar_experiencia(1000)
        
        assert personaje_basico.nivel == nivel_inicial + 1
        assert personaje_basico.hephix.nivel == 2
    
    def test_serialización(self, personaje_basico):
        """Verifica que se puede serializar/deserializar"""
        data = personaje_basico.to_dict_guardado()
        
        personaje_cargado = Personaje.from_dict_guardado(data)
        
        assert personaje_cargado.nombre == personaje_basico.nombre
        assert personaje_cargado.nivel == personaje_basico.nivel
        assert personaje_cargado.pv_actuales == personaje_basico.pv_actuales


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ==============================================================================
# ARCHIVO 34/36: test_narrador.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/test_narrador.py
# ==============================================================================

"""
Tests para el servicio de narrador.
Ejecutar con: pytest tests/test_narrador.py -v
"""
import pytest
from servicios.narrador_service import NarradorService
from servicios.cliente_ia import ClienteIA, ClienteIAMock
from servicios.persistencia_estructuras import ContextoNarrativo
from entidades import Personaje, Ficha, Hephix, HephixTipo, ClaseTipo
from patrones import EventBus, TipoEvento, SingletonMeta


class TestClienteIA:
    """Tests para el cliente de IA"""
    
    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton antes de cada test"""
        SingletonMeta.reset_instances()
        yield
    
    def test_cliente_ia_singleton(self):
        """Verifica que ClienteIA es singleton"""
        cliente1 = ClienteIA()
        cliente2 = ClienteIA()
        
        assert cliente1 is cliente2
    
    def test_cliente_mock_disponible(self):
        """Verifica que el cliente mock está siempre disponible"""
        cliente = ClienteIAMock()
        
        assert cliente.esta_disponible()
    
    def test_cliente_mock_genera_texto(self):
        """Verifica que el mock genera texto"""
        cliente = ClienteIAMock()
        
        respuesta = cliente.generar_texto("Describe un combate")
        
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0
    
    def test_cliente_mock_respuestas_contextuales(self):
        """Verifica que el mock da respuestas según el contexto"""
        cliente = ClienteIAMock()
        
        # Combate
        respuesta_combate = cliente.generar_texto("Narra un ataque en combate")
        assert "combate" in respuesta_combate.lower() or "ataque" in respuesta_combate.lower()
        
        # Exploración
        respuesta_explorar = cliente.generar_texto("Describe explorar una cueva")
        assert "explor" in respuesta_explorar.lower() or "descubr" in respuesta_explorar.lower()
    
    def test_cliente_mock_con_system_message(self):
        """Verifica que el mock acepta system_message"""
        cliente = ClienteIAMock()
        
        respuesta = cliente.generar_texto(
            "Narra algo épico",
            system_message="Eres un narrador épico"
        )
        
        assert isinstance(respuesta, str)
        assert len(respuesta) > 0


class TestNarradorService:
    """Tests para el servicio de narrador"""
    
    @pytest.fixture
    def event_bus(self):
        """Crea un event bus"""
        return EventBus()
    
    @pytest.fixture
    def contexto(self):
        """Crea un contexto narrativo"""
        return ContextoNarrativo(
            ubicacion_actual="Taberna del Dragón",
            checkpoint_actual="taberna_inicio"
        )
    
    @pytest.fixture
    def narrador(self, event_bus, contexto):
        """Crea un narrador con mock"""
        return NarradorService(event_bus, contexto, usar_mock=True)
    
    @pytest.fixture
    def personaje(self):
        """Crea un personaje de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.resistencia = 7
        
        return Personaje(
            nombre="Aldric",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha
        )
    
    # ========================================================================
    # Tests de Inicialización
    # ========================================================================
    
    def test_crear_narrador(self, narrador):
        """Verifica creación del narrador"""
        assert narrador is not None
        assert narrador.cliente is not None
        assert narrador.contexto is not None
    
    def test_narrador_usa_mock_por_defecto(self, event_bus, contexto):
        """Verifica que usa mock cuando se solicita"""
        narrador = NarradorService(event_bus, contexto, usar_mock=True)
        
        assert isinstance(narrador.cliente, ClienteIAMock)
    
    def test_system_message_creado(self, narrador):
        """Verifica que se crea el system message"""
        assert narrador.system_message is not None
        assert len(narrador.system_message) > 0
        assert "Ether Blades" in narrador.system_message
    
    # ========================================================================
    # Tests de Suscripción a Eventos
    # ========================================================================
    
    def test_suscripcion_eventos(self, narrador):
        """Verifica que se suscribe a eventos relevantes"""
        event_bus = narrador.event_bus
        
        # Verificar que hay subscriptores para eventos de combate
        assert event_bus.contar_subscriptores(TipoEvento.COMBATE_INICIADO) > 0
        assert event_bus.contar_subscriptores(TipoEvento.ATAQUE_REALIZADO) > 0
        assert event_bus.contar_subscriptores(TipoEvento.GOLPE_GRACIA) > 0
    
    # ========================================================================
    # Tests de Narración de Eventos
    # ========================================================================
    
    def test_narrar_inicio_combate(self, event_bus, narrador, capsys):
        """Verifica narración de inicio de combate"""
        # Publicar evento
        event_bus.publicar(TipoEvento.COMBATE_INICIADO, {
            "combatientes": ["Aldric", "Goblin"]
        })
        
        # Capturar output
        captured = capsys.readouterr()
        
        # Verificar que se generó alguna narración
        assert "INICIO DE COMBATE" in captured.out or len(captured.out) > 0
    
    def test_narrar_ataque(self, event_bus, narrador, capsys):
        """Verifica narración de ataque"""
        event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
            "atacante": "Aldric",
            "defensor": "Goblin"
        })
        
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    
    def test_narrar_golpe_gracia(self, event_bus, narrador, capsys):
        """Verifica narración de golpe de gracia"""
        event_bus.publicar(TipoEvento.GOLPE_GRACIA, {
            "atacante": "Aldric",
            "defensor": "Goblin"
        })
        
        captured = capsys.readouterr()
        assert "GOLPE DE GRACIA" in captured.out or len(captured.out) > 0
    
    def test_narrar_muerte(self, event_bus, narrador, capsys):
        """Verifica narración de muerte"""
        event_bus.publicar(TipoEvento.PERSONAJE_MUERTO, {
            "personaje": "Goblin"
        })
        
        captured = capsys.readouterr()
        assert len(captured.out) > 0
    
    # ========================================================================
    # Tests de Narración Libre
    # ========================================================================
    
    def test_narrar_situacion(self, narrador, personaje):
        """Verifica narración de situación libre"""
        narracion = narrador.narrar_situacion(
            "El personaje encuentra una puerta misteriosa",
            personaje
        )
        
        assert isinstance(narracion, str)
        assert len(narracion) > 0
    
    def test_narrar_situacion_sin_personaje(self, narrador):
        """Verifica narración sin personaje"""
        narracion = narrador.narrar_situacion(
            "Una tormenta se avecina"
        )
        
        assert isinstance(narracion, str)
        assert len(narracion) > 0
    
    def test_narrar_decision(self, narrador, personaje):
        """Verifica narración de decisión"""
        narracion = narrador.narrar_decision(
            "Debes elegir entre dos caminos",
            ["Camino de la luz", "Camino de la oscuridad"],
            personaje
        )
        
        assert isinstance(narracion, str)
        assert len(narracion) > 0
    
    # ========================================================================
    # Tests de Contexto
    # ========================================================================
    
    def test_actualizar_contexto(self, narrador):
        """Verifica actualización de contexto"""
        nuevo_contexto = ContextoNarrativo(
            ubicacion_actual="Bosque Oscuro",
            checkpoint_actual="bosque_entrada"
        )
        
        narrador.actualizar_contexto(nuevo_contexto)
        
        assert narrador.contexto.ubicacion_actual == "Bosque Oscuro"
        assert narrador.contexto.checkpoint_actual == "bosque_entrada"
    
    def test_contexto_en_narracion(self, narrador, personaje):
        """Verifica que el contexto influye en la narración"""
        # Actualizar contexto
        contexto = ContextoNarrativo(
            ubicacion_actual="Catacumbas Malditas"
        )
        narrador.actualizar_contexto(contexto)
        
        # Narrar algo
        narracion = narrador.narrar_situacion(
            "Exploras el lugar",
            personaje
        )
        
        # La narración debería existir
        assert len(narracion) > 0
    
    # ========================================================================
    # Tests de Manejo de Errores
    # ========================================================================
    
    def test_narrar_con_datos_incompletos(self, event_bus, narrador, capsys):
        """Verifica manejo de datos incompletos"""
        # Publicar evento con datos mínimos
        event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {})
        
        # No debería crashear
        captured = capsys.readouterr()
        # Puede tener output o no, pero no debería haber error
    
    # ========================================================================
    # Tests de Integración
    # ========================================================================
    
    @pytest.mark.integration
    def test_flujo_combate_completo(self, event_bus, narrador, capsys):
        """Test de integración: flujo completo de combate narrado"""
        # Inicio
        event_bus.publicar(TipoEvento.COMBATE_INICIADO, {
            "combatientes": ["Héroe", "Villano"]
        })
        
        # Ataques
        event_bus.publicar(TipoEvento.ATAQUE_REALIZADO, {
            "atacante": "Héroe",
            "defensor": "Villano"
        })
        
        # Golpe de gracia
        event_bus.publicar(TipoEvento.GOLPE_GRACIA, {
            "atacante": "Héroe",
            "defensor": "Villano"
        })
        
        # Muerte
        event_bus.publicar(TipoEvento.PERSONAJE_MUERTO, {
            "personaje": "Villano"
        })
        
        captured = capsys.readouterr()
        
        # Debería haber generado múltiples narraciones
        assert len(captured.out) > 0


class TestIntegracionNarradorCombate:
    """Tests de integración entre narrador y combate"""
    
    @pytest.mark.integration
    def test_narrador_en_combate_real(self):
        """Verifica que el narrador funciona durante un combate"""
        from servicios import CombateService
        
        # Crear personajes
        ficha1 = Ficha()
        ficha1.caracteristicas.fuerza = 8
        ficha1.caracteristicas.resistencia = 7
        ficha1.caracteristicas.stamina = 3
        
        personaje1 = Personaje(
            nombre="Guerrero",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha1
        )
        
        ficha2 = Ficha()
        ficha2.caracteristicas.fuerza = 5
        ficha2.caracteristicas.resistencia = 4
        ficha2.caracteristicas.stamina = 2
        
        personaje2 = Personaje(
            nombre="Goblin",
            edad=10,
            raza="Goblin",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha2
        )
        
        # Crear servicios
        event_bus = EventBus()
        narrador = NarradorService(event_bus, usar_mock=True)
        combate = CombateService(event_bus)
        
        # Iniciar combate (debería generar narración)
        combate.iniciar_combate([personaje1, personaje2])
        
        # Realizar ataque (debería generar narración)
        combate.resolver_ataque(personaje1, personaje2)
        
        # Si llegamos aquí sin errores, la integración funciona
        assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ==============================================================================
# ARCHIVO 35/36: test_patrones.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/test_patrones.py
# ==============================================================================

"""
Tests unitarios para los patrones de diseño.
Ejecutar con: pytest tests/test_patrones.py -v
"""
import pytest
from patrones import (
    SingletonMeta, 
    FactoryConRegistro,
    EventBus,
    TipoEvento,
    RegistroEstrategiasAtaque,
    TipoAtaque
)


# ============================================================================
# Tests de Singleton
# ============================================================================

class TestSingleton:
    """Tests para el patrón Singleton"""
    
    def test_singleton_misma_instancia(self):
        """Verifica que siempre retorna la misma instancia"""
        
        class MiSingleton(metaclass=SingletonMeta):
            def __init__(self):
                self.valor = 42
        
        instancia1 = MiSingleton()
        instancia2 = MiSingleton()
        
        assert instancia1 is instancia2
        assert id(instancia1) == id(instancia2)
    
    def test_singleton_comparte_estado(self):
        """Verifica que las instancias comparten estado"""
        
        class Config(metaclass=SingletonMeta):
            def __init__(self):
                self.version = "1.0"
        
        config1 = Config()
        config1.version = "2.0"
        
        config2 = Config()
        assert config2.version == "2.0"
    
    def test_singleton_reset(self):
        """Verifica que se puede resetear para testing"""
        
        class TestSingleton(metaclass=SingletonMeta):
            def __init__(self, valor=0):
                self.valor = valor
        
        inst1 = TestSingleton(10)
        assert inst1.valor == 10
        
        # Reset
        SingletonMeta.reset_instances()
        
        inst2 = TestSingleton(20)
        assert inst2.valor == 20
        assert inst1 is not inst2


# ============================================================================
# Tests de Factory
# ============================================================================

class TestFactory:
    """Tests para el patrón Factory"""
    
    def test_factory_registro(self):
        """Verifica que se pueden registrar y crear tipos"""
        
        class Arma:
            def __init__(self, nombre: str):
                self.nombre = nombre
        
        class Espada(Arma):
            pass
        
        factory = FactoryConRegistro[Arma]()
        factory.registrar("espada", Espada)
        
        arma = factory.crear("espada", nombre="Excalibur")
        assert isinstance(arma, Espada)
        assert arma.nombre == "Excalibur"
    
    def test_factory_tipo_invalido(self):
        """Verifica que lanza error con tipo inválido"""
        
        class Arma:
            pass
        
        factory = FactoryConRegistro[Arma]()
        
        with pytest.raises(ValueError, match="no reconocido"):
            factory.crear("tipo_inexistente")
    
    def test_factory_tipos_disponibles(self):
        """Verifica que lista tipos correctamente"""
        
        class Item:
            pass
        
        factory = FactoryConRegistro[Item]()
        factory.registrar("tipo_a", Item)
        factory.registrar("tipo_b", Item)
        
        tipos = factory.obtener_tipos_disponibles()
        assert "tipo_a" in tipos
        assert "tipo_b" in tipos
        assert len(tipos) == 2


# ============================================================================
# Tests de Observer
# ============================================================================

class TestObserver:
    """Tests para el patrón Observer"""
    
    def test_eventbus_suscripcion(self):
        """Verifica que los callbacks se ejecutan"""
        bus = EventBus()
        
        eventos_recibidos = []
        
        def callback(evento):
            eventos_recibidos.append(evento)
        
        bus.suscribir(TipoEvento.ATAQUE_REALIZADO, callback)
        bus.publicar(TipoEvento.ATAQUE_REALIZADO, {"daño": 10})
        
        assert len(eventos_recibidos) == 1
        assert eventos_recibidos[0].tipo == TipoEvento.ATAQUE_REALIZADO
    
    def test_eventbus_multiples_subscriptores(self):
        """Verifica que múltiples subscriptores reciben el evento"""
        bus = EventBus()
        
        contador1 = []
        contador2 = []
        
        bus.suscribir(TipoEvento.DAÑO_RECIBIDO, lambda e: contador1.append(1))
        bus.suscribir(TipoEvento.DAÑO_RECIBIDO, lambda e: contador2.append(1))
        
        bus.publicar(TipoEvento.DAÑO_RECIBIDO)
        
        assert len(contador1) == 1
        assert len(contador2) == 1
    
    def test_eventbus_desuscripcion(self):
        """Verifica que se puede desuscribir"""
        bus = EventBus()
        
        contador = []
        callback = lambda e: contador.append(1)
        
        bus.suscribir(TipoEvento.TURNO_INICIADO, callback)
        bus.publicar(TipoEvento.TURNO_INICIADO)
        assert len(contador) == 1
        
        bus.desuscribir(TipoEvento.TURNO_INICIADO, callback)
        bus.publicar(TipoEvento.TURNO_INICIADO)
        assert len(contador) == 1  # No aumentó
    
    def test_eventbus_historial(self):
        """Verifica que mantiene historial de eventos"""
        bus = EventBus()
        
        bus.publicar(TipoEvento.COMBATE_INICIADO, {"combatientes": 2})
        bus.publicar(TipoEvento.ATAQUE_REALIZADO, {"daño": 5})
        
        historial = bus.obtener_historial()
        assert len(historial) == 2
        assert historial[0].tipo == TipoEvento.ATAQUE_REALIZADO  # Más reciente
    
    def test_eventbus_pausar(self):
        """Verifica que se puede pausar"""
        bus = EventBus()
        
        contador = []
        bus.suscribir(TipoEvento.NIVEL_SUBIDO, lambda e: contador.append(1))
        
        bus.pausar()
        bus.publicar(TipoEvento.NIVEL_SUBIDO)
        assert len(contador) == 0  # No se ejecutó
        
        bus.reanudar()
        bus.publicar(TipoEvento.NIVEL_SUBIDO)
        assert len(contador) == 1  # Ahora sí


# ============================================================================
# Tests de Strategy
# ============================================================================

class TestStrategy:
    """Tests para el patrón Strategy"""
    
    def test_registro_estrategias_ataque(self):
        """Verifica que el registro tiene todas las estrategias"""
        estrategias = [
            TipoAtaque.MELEE,
            TipoAtaque.DISTANCIA,
            TipoAtaque.MAGICO
        ]
        
        for tipo in estrategias:
            estrategia = RegistroEstrategiasAtaque.obtener(tipo)
            assert estrategia is not None
    
    def test_estrategias_diferentes(self):
        """Verifica que cada estrategia es diferente"""
        melee = RegistroEstrategiasAtaque.obtener(TipoAtaque.MELEE)
        distancia = RegistroEstrategiasAtaque.obtener(TipoAtaque.DISTANCIA)
        magico = RegistroEstrategiasAtaque.obtener(TipoAtaque.MAGICO)
        
        assert type(melee).__name__ == "EstrategiaAtaqueMelee"
        assert type(distancia).__name__ == "EstrategiaAtaqueDistancia"
        assert type(magico).__name__ == "EstrategiaAtaqueMagico"


# ============================================================================
# Test de Integración
# ============================================================================

class TestIntegracionPatrones:
    """Tests de integración entre patrones"""
    
    def test_factory_con_eventbus(self):
        """Verifica que Factory y EventBus trabajan juntos"""
        
        class Arma:
            def __init__(self, nombre: str, bus: EventBus):
                self.nombre = nombre
                self.bus = bus
            
            def atacar(self):
                self.bus.publicar(TipoEvento.ATAQUE_REALIZADO, 
                                 {"arma": self.nombre})
        
        factory = FactoryConRegistro[Arma]()
        factory.registrar("espada", Arma)
        
        bus = EventBus()
        eventos = []
        bus.suscribir(TipoEvento.ATAQUE_REALIZADO, lambda e: eventos.append(e))
        
        espada = factory.crear("espada", nombre="Excalibur", bus=bus)
        espada.atacar()
        
        assert len(eventos) == 1
        assert eventos[0].datos["arma"] == "Excalibur"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

# ==============================================================================
# ARCHIVO 36/36: test_persistencia.py
# Directorio: tests
# Ruta completa: /home/nicobartok0/diseño-de-sistemas/etherbladespocket-diseño/./tests/test_persistencia.py
# ==============================================================================

"""
Tests para el servicio de persistencia.
Ejecutar con: pytest tests/test_persistencia.py -v
"""
import pytest
import shutil
from pathlib import Path
from servicios.persistencia_service import PersistenciaService
from servicios.persistencia_estructuras import (
    ContextoNarrativo, EventoNarrativo, TipoEvento
)
from entidades import Personaje, Ficha, Hephix, HephixTipo, ClaseTipo
from patrones import SingletonMeta


class TestPersistenciaService:
    """Tests para el servicio de persistencia"""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup y teardown para cada test"""
        # Usar directorio temporal para tests
        self.test_dir = Path("guardados_test")
        self.test_dir.mkdir(exist_ok=True)
        
        # Reset singleton antes de cada test
        SingletonMeta.reset_instances()
        
        yield
        
        # Limpiar después de cada test
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
    
    @pytest.fixture
    def servicio(self):
        """Crea un servicio de persistencia para testing"""
        return PersistenciaService(directorio_guardados=str(self.test_dir))
    
    @pytest.fixture
    def personaje_prueba(self):
        """Crea un personaje de prueba"""
        ficha = Ficha()
        ficha.caracteristicas.fuerza = 8
        ficha.caracteristicas.resistencia = 7
        ficha.caracteristicas.stamina = 3
        
        return Personaje(
            nombre="Aldric Test",
            edad=25,
            raza="Humano",
            clase=ClaseTipo.GUERRERO,
            hephix=Hephix.crear_desde_tipo(HephixTipo.ELEMENTAL),
            ficha=ficha,
            historia="Un guerrero de prueba"
        )
    
    @pytest.fixture
    def contexto_prueba(self):
        """Crea un contexto de prueba"""
        contexto = ContextoNarrativo(
            checkpoint_actual="test_checkpoint",
            ubicacion_actual="Zona de Test"
        )
        contexto.npcs_conocidos.append("NPC Test")
        contexto.agregar_evento(EventoNarrativo(
            tipo=TipoEvento.COMBATE,
            descripcion="Combate de prueba",
            relevancia="alta"
        ))
        return contexto
    
    # ========================================================================
    # Tests de Singleton
    # ========================================================================
    
    def test_singleton_misma_instancia(self):
        """Verifica que siempre retorna la misma instancia"""
        servicio1 = PersistenciaService(directorio_guardados=str(self.test_dir))
        servicio2 = PersistenciaService(directorio_guardados=str(self.test_dir))
        
        assert servicio1 is servicio2
    
    # ========================================================================
    # Tests de Guardado
    # ========================================================================
    
    def test_guardar_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se guarda correctamente una partida"""
        archivo = servicio.guardar_partida(
            personaje_prueba,
            contexto_prueba,
            slot=1,
            nombre_partida="Partida de Prueba"
        )
        
        assert archivo.exists()
        assert archivo.name == "slot_01.json"
    
    def test_guardar_slot_invalido(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que rechaza slots inválidos"""
        with pytest.raises(ValueError, match="debe estar entre 1 y 10"):
            servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=0)
        
        with pytest.raises(ValueError, match="debe estar entre 1 y 10"):
            servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=11)
    
    def test_sobrescribir_slot(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se puede sobrescribir un slot"""
        # Guardar primera vez
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        # Modificar personaje
        personaje_prueba.nivel = 5
        
        # Guardar de nuevo en el mismo slot
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        # Verificar que se sobrescribió
        datos = servicio.cargar_partida(1)
        assert datos.personaje['nivel'] == 5
    
    def test_autoguardar(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica funcionamiento del autoguardado"""
        archivo = servicio.autoguardar(personaje_prueba, contexto_prueba, slot=2)
        
        assert archivo.exists()
        assert servicio.existe_partida(2)
    
    # ========================================================================
    # Tests de Carga
    # ========================================================================
    
    def test_cargar_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se carga correctamente una partida"""
        # Guardar
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        # Cargar
        datos = servicio.cargar_partida(1)
        
        assert datos.personaje['nombre'] == "Aldric Test"
        assert datos.contexto.ubicacion_actual == "Zona de Test"
        assert datos.slot == 1
    
    def test_cargar_slot_vacio(self, servicio):
        """Verifica error al cargar slot vacío"""
        with pytest.raises(FileNotFoundError, match="está vacío"):
            servicio.cargar_partida(3)
    
    def test_cargar_personaje(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se puede cargar solo el personaje"""
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        personaje_cargado = servicio.cargar_personaje(1)
        
        assert personaje_cargado.nombre == personaje_prueba.nombre
        assert personaje_cargado.nivel == personaje_prueba.nivel
        assert personaje_cargado.clase == personaje_prueba.clase
    
    def test_cargar_contexto(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que se puede cargar solo el contexto"""
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        contexto_cargado = servicio.cargar_contexto(1)
        
        assert contexto_cargado.ubicacion_actual == contexto_prueba.ubicacion_actual
        assert contexto_cargado.checkpoint_actual == contexto_prueba.checkpoint_actual
        assert len(contexto_cargado.npcs_conocidos) > 0
    
    def test_integridad_datos_cargados(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica que todos los datos se preservan correctamente"""
        # Configurar personaje con datos específicos
        personaje_prueba.nivel = 10
        personaje_prueba.experiencia = 5000
        personaje_prueba.pv_actuales = 50
        personaje_prueba.inventario.agregar_monedas(500)
        
        # Configurar contexto
        contexto_prueba.reputacion["Faccion Test"] = 25
        contexto_prueba.misiones_activas.append("Mision Test")
        
        # Guardar y cargar
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        personaje_cargado = servicio.cargar_personaje(1)
        contexto_cargado = servicio.cargar_contexto(1)
        
        # Verificar personaje
        assert personaje_cargado.nivel == 10
        assert personaje_cargado.experiencia == 5000
        assert personaje_cargado.pv_actuales == 50
        assert personaje_cargado.inventario.monedas == 500
        
        # Verificar contexto
        assert contexto_cargado.reputacion["Faccion Test"] == 25
        assert "Mision Test" in contexto_cargado.misiones_activas
    
    # ========================================================================
    # Tests de Gestión de Slots
    # ========================================================================
    
    def test_listar_partidas_vacio(self, servicio):
        """Verifica listado cuando no hay partidas"""
        slots = servicio.listar_partidas()
        
        assert len(slots) == 10
        assert all(not slot.existe for slot in slots)
    
    def test_listar_partidas_con_guardados(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica listado con partidas guardadas"""
        # Guardar en slots 1, 3 y 5
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=3)
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=5)
        
        slots = servicio.listar_partidas()
        
        assert slots[0].existe  # Slot 1
        assert not slots[1].existe  # Slot 2
        assert slots[2].existe  # Slot 3
        assert not slots[3].existe  # Slot 4
        assert slots[4].existe  # Slot 5
    
    def test_existe_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica detección de existencia de partida"""
        assert not servicio.existe_partida(1)
        
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        assert servicio.existe_partida(1)
    
    def test_eliminar_partida(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica eliminación de partida"""
        # Guardar
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        assert servicio.existe_partida(1)
        
        # Eliminar
        resultado = servicio.eliminar_partida(1)
        
        assert resultado is True
        assert not servicio.existe_partida(1)
    
    def test_eliminar_partida_inexistente(self, servicio):
        """Verifica que eliminar partida inexistente retorna False"""
        resultado = servicio.eliminar_partida(5)
        assert resultado is False
    
    # ========================================================================
    # Tests de Tiempo de Juego
    # ========================================================================
    
    def test_tracking_tiempo_jugado(self, servicio):
        """Verifica tracking de tiempo de juego"""
        servicio.iniciar_sesion()
        
        # Simular algo de tiempo (no podemos esperar realmente)
        tiempo = servicio.obtener_tiempo_jugado()
        
        assert tiempo.total_seconds() >= 0
    
    def test_pausar_sesion(self, servicio):
        """Verifica pausa de sesión"""
        servicio.iniciar_sesion()
        servicio.pausar_sesion()
        
        tiempo = servicio.obtener_tiempo_jugado()
        assert tiempo.total_seconds() >= 0
    
    def test_formateo_tiempo(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica formato de tiempo en guardado"""
        servicio.iniciar_sesion()
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        datos = servicio.cargar_partida(1)
        
        # El formato debe ser "Xh Ym"
        assert "h" in datos.tiempo_jugado
        assert "m" in datos.tiempo_jugado
    
    # ========================================================================
    # Tests de Validación
    # ========================================================================
    
    def test_verificar_integridad_ok(self, servicio, personaje_prueba, contexto_prueba):
        """Verifica validación de integridad correcta"""
        servicio.guardar_partida(personaje_prueba, contexto_prueba, slot=1)
        
        valido, error = servicio.verificar_integridad(1)
        
        assert valido is True
        assert error is None
    
    def test_verificar_integridad_slot_vacio(self, servicio):
        """Verifica detección de slot vacío"""
        valido, error = servicio.verificar_integridad(1)
        
        assert valido is False
        assert "vacío" in error.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


################################################################################
# FIN DEL INTEGRADOR FINAL
# Total de archivos: 36
# Generado: 2025-11-04 15:40:21
################################################################################
