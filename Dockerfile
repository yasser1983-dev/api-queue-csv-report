# Usa una imagen base oficial de Python
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de dependencias (requirements.txt) al contenedor
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código del proyecto Django al contenedor
COPY . /app/

# Expón el puerto en el que Django correrá (generalmente el 8000)
EXPOSE 8000

# Comando para ejecutar la aplicación Django cuando el contenedor arranque
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
