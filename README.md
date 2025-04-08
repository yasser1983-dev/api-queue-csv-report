
# Proyecto API con Django con Redis y Docker. Prceso de despliegue

## Requisitos para ejecutar el proyecto 

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

# Realizar pruebas con datos falsos

Generar datos falsos en las tablas de las base de datos utilizando el siguiente script
```bash
  python populate_db.py
```