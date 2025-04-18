
# Proyecto API con Django con Redis y Docker. Proceso de despliegue

## Despliegue automático del proyecto

### 1 Clonar el repositorio
Usa actions/checkout para obtener el código fuente.
```bash
    git clone git@github.com:yasser1983-dev/api-queue-csv-report.git
```
### 2 Configurar el pipeline de Github para despliegue
  Ir al archivo deploy.yml y configurar las variables de entorno necesarias para el despliegue automático del proyecto.
    - `SERVER_HOST`: Dirección IP del servidor donde se desplegará el proyecto.
    - `SERVER_USER`: Usuario del servidor donde se desplegará el proyecto.
    - `SERVER_SSH_KEY`: Llave SSH para acceder al servidor.

### 3 Ejecución Manual
a. Ir a l repositorio en GitHub

b. Haz clic en la pestaña "Actions"

c. Busca el workflow

d. Haz clic en el botón "Run workflow"

e.Selecciona la rama (por ejemplo: main)

f. Dale a "Run workflow"

### Desplegar el proyecto
  Para desplegar el proyecto, se debe ejecutar el siguiente comando en la terminal:
```bash
  gh auth login
  gh workflow run deploy.yml
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

### Ejecutar las pruebas

```bash
  python manage.py test
```