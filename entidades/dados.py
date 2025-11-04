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