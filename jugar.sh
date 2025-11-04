#!/bin/bash
# Script para iniciar Ether Blades fácilmente

echo "⚔️  Iniciando Ether Blades..."
echo ""

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ No se encontró el entorno virtual."
    echo "   Ejecuta: python -m venv venv"
    exit 1
fi

# Activar entorno virtual
source venv/bin/activate

# Ejecutar juego
python main.py

# Desactivar al salir
deactivate