#!/bin/bash

echo "=== Aplicando correcciones al proyecto variant_alert ==="

# Backup de archivos originales
echo "1. Haciendo backup de archivos originales..."
cp pyproject.toml pyproject.toml.original 2>/dev/null || echo "No se pudo hacer backup de pyproject.toml"
cp Dockerfile Dockerfile.original 2>/dev/null || echo "No se pudo hacer backup de Dockerfile"
cp docker-compose.yml docker-compose.yml.original 2>/dev/null || echo "No se pudo hacer backup de docker-compose.yml"

# Aplicar pyproject.toml corregido
echo "2. Aplicando pyproject.toml corregido..."
if [ -f "pyproject_fixed.toml" ]; then
    cp pyproject_fixed.toml pyproject.toml
    echo "✓ pyproject.toml actualizado"
else
    echo "✗ No se encontró pyproject_fixed.toml"
fi

# Aplicar Dockerfile corregido
echo "3. Aplicando Dockerfile corregido..."
if [ -f "Dockerfile_fixed" ]; then
    cp Dockerfile_fixed Dockerfile
    echo "✓ Dockerfile actualizado"
else
    echo "✗ No se encontró Dockerfile_fixed"
fi

# Aplicar docker-compose.yml corregido
echo "4. Aplicando docker-compose.yml corregido..."
if [ -f "docker-compose_fixed.yml" ]; then
    cp docker-compose_fixed.yml docker-compose.yml
    echo "✓ docker-compose.yml actualizado"
else
    echo "✗ No se encontró docker-compose_fixed.yml"
fi

# Limpiar archivos temporales
echo "5. Limpiando archivos temporales..."
rm -f poetry.lock 2>/dev/null

echo "=== Correcciones aplicadas ==="
echo "Archivos corregidos:"
ls -la *_fixed* 2>/dev/null || echo "No hay archivos *_fixed"
echo ""
echo "Para probar:"
echo "1. poetry install"
echo "2. docker-compose build"
echo "3. docker-compose up"
