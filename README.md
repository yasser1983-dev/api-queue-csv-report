


## Requisitos para ejecutar el proyecto 

### Correr el worker
```bash
  python manage.py rqworker
```

### Revisar si la conexión a la base de datos es correcta

```bash
    python manage.py check --database default
```

### Generar datos falsos en las tablas de las base de datos
```bash
  python populate_db.py
```

### Levantar los servicios de base de datos y Redis con Docker
```bash
  docker-compose up -d
```

### Crear un super usuario para entrar a la sección administrativa
```bash
  python manage.py createsuperuser 
```