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