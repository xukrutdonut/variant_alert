FROM python:3.9-slim

# Variables de entorno
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Dependencias de sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ make libbz2-dev liblzma-dev zlib1g-dev \
    libcurl4-openssl-dev curl git && \
    rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de gestión de dependencias
COPY pyproject.toml poetry.lock* /app/

# Actualizar pysam a >=0.17 (sin usar opciones obsoletas)
RUN poetry add "pysam^0.17"

# Bloquear dependencias de manera reproducible
RUN poetry lock --no-update

# Instalar solo dependencias main
RUN poetry install --no-root --only main

# Copiar resto del proyecto
COPY . /app

# Comando por defecto
CMD ["poetry", "run", "python", "main.py"]
