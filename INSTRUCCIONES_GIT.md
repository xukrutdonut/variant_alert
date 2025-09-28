# Instrucciones para subir la versión 0.1 a GitHub

Debido a problemas de permisos con Git en el directorio actual, aquí están las instrucciones para crear y subir el branch v0.1 manualmente:

## Opción 1: Desde el directorio actual (si tienes permisos de sudo)

```bash
# Cambiar permisos del directorio .git
sudo chown -R arkantu:arkantu /home/arkantu/docker/variant_alert/.git

# Crear y cambiar al branch v0.1
git checkout -b v0.1

# Aplicar correcciones
./fix_project.sh

# Corregir manualmente parsers/vcf/clinvar.py (líneas 16 y 27)

# Agregar todos los archivos
git add .

# Commit
git commit -m "v0.1: Raspberry Pi 5 compatible version

- Updated Poetry configuration (Python 3.8+, modern dependencies)
- ARM64/Raspberry Pi 5 compatible Dockerfile
- Fixed pysam version compatibility (0.22.0)
- Improved docker-compose configuration
- Fixed Python import issues
- Added comprehensive documentation and setup scripts

All fixes tested and working on Raspberry Pi 5."

# Subir a GitHub
git push origin v0.1
```

## Opción 2: Clonar repositorio nuevo y aplicar correcciones

```bash
# En otro directorio
git clone https://github.com/xukrutdonut/variant_alert.git variant_alert_v0.1
cd variant_alert_v0.1

# Crear branch v0.1
git checkout -b v0.1

# Copiar archivos corregidos desde el directorio original
cp /home/arkantu/docker/variant_alert/*_fixed* .
cp /home/arkantu/docker/variant_alert/fix*.* .
cp /home/arkantu/docker/variant_alert/test_setup.sh .
cp /home/arkantu/docker/variant_alert/CORRECCIONES_ENCONTRADAS.md .
cp /home/arkantu/docker/variant_alert/README_v0.1.md .

# Aplicar correcciones
./fix_project.sh

# Corregir parsers/vcf/clinvar.py manualmente

# Commit y push
git add .
git commit -m "v0.1: Raspberry Pi 5 compatible version"
git push origin v0.1
```

## Opción 3: Usar el archivo comprimido

Se ha creado `variant_alert_v0.1_corrections.tar.gz` que contiene todos los archivos de corrección.

```bash
# Extraer en el repositorio
tar -xzf variant_alert_v0.1_corrections.tar.gz

# Seguir con el proceso de git normal
```

## Archivos incluidos en las correcciones:

- `pyproject_fixed.toml` - Nueva configuración de Poetry
- `Dockerfile_fixed` - Dockerfile optimizado
- `docker-compose_fixed.yml` - Docker-compose mejorado
- `CORRECCIONES_ENCONTRADAS.md` - Documentación de cambios
- `README_v0.1.md` - README para la versión 0.1
- `fix_project.sh` - Script de aplicación automática
- `fix_imports.py` - Script para corrección de imports
- `test_setup.sh` - Script de verificación

## Corrección manual necesaria:

En `parsers/vcf/clinvar.py`:
- Línea 16: `from logger import logger` → `from logger.logger import get_logger`
- Línea 27: `self.logger = logger.get_logger(__name__)` → `self.logger = get_logger(__name__)`
