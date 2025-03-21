# Usa una imagen base de Python (puedes elegir la versión que necesites)
FROM python:3.9-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos (si los tienes)
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de tu aplicación al contenedor
COPY . .

# Puerto para uso del contenedor
ENV PORT=9000

# Expone el puerto en el que tu aplicación se ejecutará (si aplica)
EXPOSE 9000

# Define el comando que se ejecutará cuando el contenedor arranque
CMD ["python", "app.py"]