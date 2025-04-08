
# Proyecto API con Django con Redis y Docker. Proceso de despliegue

## Despliegue automático del proyecto

### 1 Clonar el repositorio
Usa actions/checkout para obtener el código fuente.
```bash
    git clone git@github.com:yasser1983-dev/api-queue-csv-report.git
```
### 2 Configurar Python
Instala Python y las dependencias necesarias desde requirements.txt.
```bash
  pip install -r requirements.txt
```

### 3 Construir y publicar la imagen Docker
Construye la imagen Docker utilizando docker compose definido en docker-compose.yml y publica la imagen en Docker Hub.
```bash
  docker-compose up -d
```

### 4 Desplegar en el servidor

Usa ssh-action para conectarte al servidor, actualizar la imagen y reiniciar los servicios con docker-compose.


## Requisitos para ejecutar el proyecto manualmente o localmente

### Correr el worker
```bash
  python manage.py rqworker
```

### Levantar los servicios de base de datos y Redis con Docker
```bash
  docker-compose up -d
```

### Revisar si la conexión a la base de datos es correcta

Para la conexión  a base de datos se debe crear un fichero .env utilizando el archivo de ejemplo que trae las variables
necesarias para la conexión a la base de datos. 

Una vez configurado, puede probar la conexión a la base de datos con el siguiente comando:

```bash
    python manage.py check --database default
```

### Migrar la base de datos
```bash
  python manage.py migrate
```

### Crear un super usuario para entrar a la sección administrativa
```bash
  python manage.py createsuperuser 
```

### Para pruebas con datos falsos

Generar datos falsos en las tablas de las base de datos utilizando el siguiente script
```bash
  python populate_db.py
```

