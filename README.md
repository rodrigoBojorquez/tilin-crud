# Tilin CRUD

Tilin CRUD es una demo de desarrollo de un monolito con Python utilizando FastAPI para el backend y Jinja para los templates del frontend. Este proyecto muestra cómo construir un CRUD básico con estas tecnologías.

## Requisitos

- Python 3.8+
- MySQL (u otro sistema de gestión de bases de datos compatible)

## Instalación y Ejecución

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/tilin-crud.git
cd tilin-crud
```

### Paso 2: Crear un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
```

### Paso 3: Instalar las dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Configurar las variables de entorno

Renombra el archivo `.env.example` a `.env` y completa la información de tu base de datos:

```plaintext
DB_HOST="localhost"
DB_USER="root"
DB_PASSWORD="root"
DB_NAME="nombre_de_tu_base_de_datos"
```

### Paso 5: Ejecutar el script de base de datos

Antes de iniciar la aplicación, ejecuta el script de base de datos que se encuentra en `src/data/database.py` para crear las tablas necesarias:

```bash
python src/data/database.py
```

### Paso 6: Iniciar la aplicación

```bash
fastapi dev main.py
```

La aplicación estará disponible en `http://127.0.0.1:8000`.


## Uso

### Crear un usuario

Accede a `http://127.0.0.1:8000/users/create` y completa el formulario para crear un nuevo usuario.

### Listar usuarios

Accede a `http://127.0.0.1:8000/users` para ver una lista de usuarios.

## Contribución

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.