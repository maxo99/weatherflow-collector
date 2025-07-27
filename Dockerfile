FROM ghcr.io/astral-sh/uv:0.8-python3.13-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt update && apt install -y \
    g++ \ 
    build-essential \ 
    python3-dev \ 
    libffi-dev \ 
    libjpeg-dev \ 
    libatlas-base-dev \ 
    libblas-dev \ 
    liblapack-dev && \
    rm -rf /var/lib/apt/lists/*

COPY src /app/
COPY pyproject.toml /app/

WORKDIR /app
RUN uv sync

# Run your Python script
CMD ["uv", "run", "weatherflow-collector.py"]
