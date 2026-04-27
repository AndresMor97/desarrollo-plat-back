# MyMoney - API de Gestión de Finanzas Personales

API REST construida con Flask para la gestión de finanzas personales. Permite registrar ingresos, gastos, consultar saldo y obtener estadísticas de gastos por categoría.

---

## Tabla de Contenidos

1. [Características](#características)
2. [Arquitectura](#arquitectura)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Requisitos](#requisitos)
5. [Despliegue](#despliegue)
   - [Variables de Entorno](#variables-de-entorno)
   - [Base de Datos](#base-de-datos)
   - [Ejecución Local](#ejecución-local)
   - [Despliegue en Producción](#despliegue-en-producción)
6. [Autenticación](#autenticación)
7. [Endpoints de la API](#endpoints-de-la-api)

---

## Características

- **Registro de usuarios** con contraseña segura (hash bcrypt)
- **Inicio de sesión** con token JWT
- **Registro de transacciones** (ingresos y gastos)
- **Consulta de saldo** en tiempo real
- **Historial de transacciones** ordenado por fecha
- **Estadísticas de gastos** agrupadas por categoría
- **Gestión de categorías** para clasificar movimientos
- **Eliminación de transacciones**

---

## Arquitectura

El proyecto sigue el patrón **MVC (Model-View-Controller)** adaptado para APIs REST:

```
├── src/
│   ├── controllers/    # Lógica de negocio
│   ├── models/         # Definición de entidades de base de datos
│   ├── routes/         # Definición de endpoints (Blueprints)
│   ├── dtos/           # Validación y serialización de datos
│   └── utils/          # Middlewares y helpers
├── app.py              # Punto de entrada
├── config.py           # Configuración de la aplicación
└── requirements.txt    # Dependencias Python
```

---

## Estructura del Proyecto

```
proyecto_des_plat/
├── app.py                      # Aplicación Flask
├── config.py                   # Configuración (DB, SECRET_KEY)
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
├── src/
│   ├── __init__.py             # Factory de la app
│   ├── controllers/
│   │   ├── auth_controller.py       # Registro y login
│   │   ├── usuario_controller.py    # Listar usuarios
│   │   ├── transaccion_controller.py # Transacciones, saldo, estadísticas
│   │   └── categoria_controller.py  # Listar categorías
│   ├── models/
│   │   ├── usuario_model.py         # Modelo Usuario
│   │   ├── transaccion_model.py     # Modelo Transaccion
│   │   └── categoria_model.py       # Modelo Categoria
│   ├── routes/
│   │   ├── auth_routes.py           # /api/auth/*
│   │   ├── usuario_routes.py        # /api/usuarios
│   │   ├── transaccion_routes.py    # /api/transacciones, /api/saldo
│   │   └── categoria_routes.py      # /api/categorias
│   ├── dtos/
│   │   ├── usuario_dto.py           # Schema usuario
│   │   ├── transaccion_dto.py       # Schema transacción
│   │   ├── saldo_dto.py             # Schema saldo
│   │   └── categoria_dto.py        # Schema categoría
│   └── utils/
│       ├── auth_middleware.py       # Decorador @token_required
│       └── response_helper.py      # Helper de respuestas estándar
```

---

## Requisitos

- Python 3.11+
- MySQL 8.0+

---

## Despliegue

### Variables de Entorno

Editar `config.py` con las credenciales de la base de datos:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://usuario:password@localhost/nombre_base'
    SECRET_KEY = 'tu_clave_secreta_minimo_32_caracteres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Base de Datos

1. Crear la base de datos en MySQL:
```sql
CREATE DATABASE MyMoney CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. La aplicación usa `SQLALCHEMY_TRACK_MODIFICATIONS = False`, por lo que las tablas se crean automáticamente al iniciar (para desarrollo). Para producción se recomienda usar migraciones con Flask-Migrate.

3. Tablas necesarias:
   - `usuarios` (id_usuario, nombre, email, password_hash, creado_en)
   - `transacciones` (id_transaccion, id_usuario, monto, descripcion, tipo, id_categoria, fecha_transaccion)
   - `categorias` (id_categoria, nombre, tipo)

### Ejecución Local

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd proyecto_des_plat

# 2. Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos en config.py

# 5. Ejecutar la aplicación
python app.py
```

La API estará disponible en `http://localhost:5000`

### Despliegue en Producción

**Con Gunicorn (WSGI):**

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:app"
```

**Con Docker:**

Crear `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Construir y ejecutar:
```bash
docker build -t mymoney-api .
docker run -d -p 5000:5000 --name mymoney mymoney-api
```

**Consideraciones de seguridad para producción:**
- Cambiar `SECRET_KEY` por una clave segura y única
- Usar conexiones SSL para MySQL (`mysql+mysqlconnector://.../?ssl_ca=...`)
- Configurar CORS restringido en lugar de `*`
- Usar variables de entorno para secretos
- Implementar rate limiting

---

## Autenticación

La API usa **JWT (JSON Web Tokens)** para autenticar solicitudes protegidas.

### Flujo de autenticación:

1. **Registro:** `POST /api/auth/registro`
2. **Login:** `POST /api/auth/login` → Recibe `token`
3. **Solicitudes protegidas:** Incluir header `Authorization: Bearer <token>`

### Ejemplo con curl:

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "contraseña"}'

# Solicitud protegida
curl -X GET http://localhost:5000/api/saldo \
  -H "Authorization: Bearer <tu_token>"
```

---

## Endpoints de la API

### Base URL: `/api`

---

### Auth

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/auth/registro` | Registrar nuevo usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |

#### POST /api/auth/registro

**Request:**
```json
{
  "nombre": "Juan Pérez",
  "email": "juan@ejemplo.com",
  "password": "miContraseña123"
}
```

**Response (201):**
```json
{
  "status": "success",
  "message": "Usuario registrado con éxito",
  "data": {
    "id": 1
  }
}
```

#### POST /api/auth/login

**Request:**
```json
{
  "email": "juan@ejemplo.com",
  "password": "miContraseña123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Login exitoso",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "nombre": "Juan Pérez"
  }
}
```

---

### Transacciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/transacciones` | Crear transacción | Sí |
| GET | `/transacciones` | Listar historial | Sí |
| GET | `/saldo` | Consultar saldo | Sí |
| GET | `/estadisticas/gastos` | Estadísticas por categoría | Sí |
| DELETE | `/transacciones/<id>` | Eliminar transacción | Sí |

#### POST /api/transacciones

**Request:**
```json
{
  "monto": 150.50,
  "descripcion": "Suscripción Netflix",
  "tipo": "gasto",
  "id_categoria": 6
}
```

| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| monto | float | Sí | Mayor a 0 |
| descripcion | string | Sí | 1-255 caracteres |
| tipo | string | Sí | "ingreso" o "gasto" |
| id_categoria | int | No | ID de categoría existente |

**Response (201):**
```json
{
  "status": "success",
  "message": "Registro exitoso",
  "data": {
    "id": 42
  }
}
```

#### GET /api/transacciones

**Response (200):**
```json
{
  "status": "success",
  "message": "Historial obtenido con éxito",
  "data": [
    {
      "id": 42,
      "monto": 150.50,
      "descripcion": "Suscripción Netflix",
      "tipo": "gasto",
      "fecha": "2026-04-27",
      "categoria": "Entretenimiento"
    }
  ]
}
```

#### GET /api/saldo

**Response (200):**
```json
{
  "status": "success",
  "message": "Saldo calculado",
  "data": {
    "id_usuario": 1,
    "total_ingresos": 5000.00,
    "total_gastos": 2340.50,
    "saldo_actual": 2659.50
  }
}
```

#### GET /api/estadisticas/gastos

**Response (200):**
```json
{
  "status": "success",
  "message": "Estadísticas obtenidas",
  "data": [
    {
      "categoria": "Alimentación",
      "total": 850.00
    },
    {
      "categoria": "Transporte",
      "total": 200.00
    }
  ]
}
```

#### DELETE /api/transacciones/{id}

**Response (200):**
```json
{
  "status": "success",
  "message": "Transacción eliminada con éxito",
  "data": null
}
```

---

### Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/usuarios` | Listar todos los usuarios | Sí |

#### GET /api/usuarios

**Response (200):**
```json
{
  "status": "success",
  "message": "Lista de usuarios obtenida",
  "data": [
    {
      "id_usuario": 1,
      "nombre": "Juan Pérez",
      "email": "juan@ejemplo.com",
      "creado_en": "2026-04-01T10:30:00"
    }
  ]
}
```

---

### Categorías

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/categorias` | Listar categorías | No |
| GET | `/categorias?tipo=gasto` | Filtrar por tipo | No |

#### GET /api/categorias

**Query params (opcional):**
- `tipo`: "ingreso" o "gasto"

**Response (200):**
```json
{
  "status": "success",
  "message": "Categorías obtenidas con éxito",
  "data": [
    {
      "id_categoria": 1,
      "nombre": "Alimentación",
      "tipo": "gasto"
    },
    {
      "id_categoria": 2,
      "nombre": "Salario",
      "tipo": "ingreso"
    }
  ]
}
```

---

## Códigos de Estado

| Código | Descripción |
|--------|-------------|
| 200 | Solicitud exitosa |
| 201 | Recurso creado |
| 400 | Error de validación |
| 401 | No autenticado / Token inválido |
| 404 | Recurso no encontrado |
| 500 | Error interno del servidor |

---

## Tecnologías

- **Backend:** Flask 3.0, Python 3.11
- **ORM:** SQLAlchemy, Flask-SQLAlchemy
- **Validación:** Marshmallow, Flask-Marshmallow
- **Auth:** PyJWT, Werkzeug (password hashing)
- **Base de datos:** MySQL 8.0
- **CORS:** Flask-CORS