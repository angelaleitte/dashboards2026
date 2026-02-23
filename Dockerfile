# Imagem base Python (slim para menor tamanho)
FROM python:3.11-slim

# Evitar buffering de stdout (logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (se necessário)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY app.py .
COPY assets/ ./assets/

# Porta padrão do Dash
EXPOSE 8050

# Gunicorn para produção (worker para apps assíncronos como Dash)
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "1", "--threads", "4", "app:server"]
