# 1. Usamos Python 3.12 (como el tuyo, pero ligero)
FROM python:3.12-slim

# 2. Evitamos archivos basura y aseguramos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo
WORKDIR /app

# 4. Instalamos dependencias del sistema (necesarias para algunas librerías de IA)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 5. Instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo tu código (app.py, procesados, .env, etc.)
COPY . .

# 7. Exponemos el puerto de Streamlit
EXPOSE 8501

# 8. LANZAMOS LA WEB (Esto es lo que cambia respecto al tuyo)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]