# Correcciones necesarias para variant_alert en Raspberry Pi 5

## Problemas identificados y solucionados:

### 1. **pyproject.toml obsoleto**
**Problema**: Configuración de Poetry obsoleta y dependencias desactualizadas
**Solución**: Usar `pyproject_fixed.toml`

**Cambios principales**:
- Python version: `^3.6` → `^3.8`
- pysam: `=0.15.3` → `^0.22.0` (compatible con ARM64)
- click: `^7.0` → `^8.0`
- Migrar `dev-dependencies` → `group.dev.dependencies`
- Actualizar build-backend a `poetry.core.masonry.api`

### 2. **Dockerfile mejorado para Raspberry Pi 5**
**Problema**: Imagen base y configuración no optimizada para ARM64
**Solución**: Usar `Dockerfile_fixed`

**Mejoras**:
- Imagen base: `python:3.9-slim` → `python:3.11-slim`
- Añadidas variables de entorno para Poetry
- Dependencias de sistema más completas para pysam
- Proceso de instalación más robusto
- Compatible con arquitectura ARM64

### 3. **docker-compose.yml mejorado**
**Problema**: Configuración básica sin persistencia adecuada
**Solución**: Usar `docker-compose_fixed.yml`

**Mejoras**:
- Volúmenes para datos y logs
- Comando por defecto más útil
- Configuración para uso interactivo

### 4. **Problemas de importación en Python**
**Problema**: Import incorrecto en `parsers/vcf/clinvar.py` línea 16
```python
from logger import logger  # ✗ Incorrecto
```
**Solución**: 
```python
from logger.logger import get_logger  # ✓ Correcto
```

Y cambiar línea 27:
```python
self.logger = get_logger(__name__)  # En lugar de logger.get_logger(__name__)
```

## Instrucciones de aplicación:

### Opción 1: Script automático
```bash
chmod +x fix_project.sh
./fix_project.sh
```

### Opción 2: Manual
1. Copiar archivos corregidos:
```bash
cp pyproject_fixed.toml pyproject.toml
cp Dockerfile_fixed Dockerfile  
cp docker-compose_fixed.yml docker-compose.yml
```

2. Corregir importación en `parsers/vcf/clinvar.py`:
   - Línea 16: `from logger import logger` → `from logger.logger import get_logger`
   - Línea 27: `logger.get_logger(__name__)` → `get_logger(__name__)`

3. Regenerar dependencias:
```bash
rm poetry.lock
poetry install
```

4. Construir y probar:
```bash
docker-compose build
docker-compose up
```

## Verificación del funcionamiento:

1. **Instalar dependencias**:
```bash
poetry install
```

2. **Probar comando**:
```bash
poetry run variant-alert --help
```

3. **Construir Docker**:
```bash
docker-compose build --no-cache
```

4. **Ejecutar contenedor**:
```bash
docker-compose up
```

## Notas adicionales:

- El proyecto está diseñado para comparar archivos VCF de ClinVar
- Requiere archivos VCF de entrada como argumentos
- Compatible con Raspberry Pi 5 (ARM64)
- Todas las dependencias actualizadas a versiones modernas y estables
