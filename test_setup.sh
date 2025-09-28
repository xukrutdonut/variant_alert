#!/bin/bash

echo "=== Test del setup de variant_alert ==="

# Verificar que Poetry está instalado
echo "1. Verificando Poetry..."
if command -v poetry &> /dev/null; then
    echo "✓ Poetry está instalado: $(poetry --version)"
else
    echo "✗ Poetry no está instalado"
    exit 1
fi

# Verificar que Docker está disponible
echo "2. Verificando Docker..."
if command -v docker &> /dev/null; then
    echo "✓ Docker está disponible: $(docker --version)"
else
    echo "✗ Docker no está disponible"
    exit 1
fi

# Verificar archivos corregidos
echo "3. Verificando archivos corregidos..."
files=("pyproject_fixed.toml" "Dockerfile_fixed" "docker-compose_fixed.yml")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file existe"
    else
        echo "✗ $file no encontrado"
    fi
done

echo ""
echo "=== Instrucciones para continuar ==="
echo "1. Aplica las correcciones:"
echo "   ./fix_project.sh"
echo ""
echo "2. Corrige manualmente el archivo parsers/vcf/clinvar.py:"
echo "   - Línea 16: from logger import logger → from logger.logger import get_logger"
echo "   - Línea 27: logger.get_logger(__name__) → get_logger(__name__)"
echo ""
echo "3. Instala dependencias:"
echo "   poetry install"
echo ""
echo "4. Construye el contenedor:"
echo "   docker-compose build"
echo ""
echo "5. Prueba el contenedor:"
echo "   docker-compose up"
