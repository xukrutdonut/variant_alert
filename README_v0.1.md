# Variant Alert v0.1 - Raspberry Pi 5 Compatible

Esta versión ha sido actualizada y corregida para funcionar correctamente en Raspberry Pi 5 con Docker.

## Archivos de corrección incluidos:

- `pyproject_fixed.toml` - Configuración moderna de Poetry
- `Dockerfile_fixed` - Optimizado para ARM64/Raspberry Pi 5
- `docker-compose_fixed.yml` - Con volúmenes y configuración mejorada
- `CORRECCIONES_ENCONTRADAS.md` - Documentación completa de cambios
- `fix_project.sh` - Script de aplicación automática
- `fix_imports.py` - Script para corregir importaciones Python
- `test_setup.sh` - Script de verificación del entorno

## Instalación rápida:

```bash
# 1. Aplicar correcciones
./fix_project.sh

# 2. Corregir manualmente parsers/vcf/clinvar.py:
#    Línea 16: from logger import logger → from logger.logger import get_logger
#    Línea 27: logger.get_logger(__name__) → get_logger(__name__)

# 3. Instalar y construir
poetry install
docker-compose build
docker-compose up
```

## Cambios principales:

- Actualización de Python 3.6 → 3.8+
- Actualización de pysam 0.15.3 → 0.22.0
- Compatibilidad con arquitectura ARM64
- Migración a Poetry moderno
- Corrección de problemas de importación
- Dockerfile optimizado para Raspberry Pi

Esta versión es completamente funcional en Raspberry Pi 5.
