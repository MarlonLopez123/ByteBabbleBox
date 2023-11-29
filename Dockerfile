# Usa una imagen de Python
FROM python:3.8-slim

# Copia los archivos del servidor y del cliente al contenedor
COPY server.py /app/server.py
COPY client.py /app/client.py

# Establece el directorio de trabajo
WORKDIR /app

# Ejecuta el servidor por defecto cuando se inicia el contenedor
CMD ["python", "server.py"]
