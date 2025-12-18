# Usar imagen oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para cachear dependencias)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Crear carpetas necesarias
RUN mkdir -p documentos_generados plantillas_word

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_ENV=production
ENV PORT=5000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "2", "app.main:app"]
