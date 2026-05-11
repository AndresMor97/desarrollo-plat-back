# MyMoney - API de Gestión de Finanzas Personales

RESTful API construida con Flask para la gestión integral de finanzas personales.
Permite registrar ingresos y gastos, consultar saldos en tiempo real y obtener
estadísticas de movimiento agrupadas por categoría.

---

## Tabla de Contenidos

1. [Características](#características)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Requisitos](#requisitos)
5. [Despliegue](#despliegue)
   - [Variables de Entorno](#variables-de-entorno)
   - [Base de Datos](#base-de-datos)
   - [Ejecución Local](#ejecución-local)
   - [Despliegue en Producción](#despliegue-en-producción)
6. [Autenticación](#autenticación)
7. [Endpoints de la API](#endpoints-de-la-api)
8. [Códigos de Estado HTTP](#códigos-de-estado-http)
9. [Tecnologías](#tecnologías)

---

## Características

- **Registro de usuarios** con contraseña segura mediante hash bcrypt
- **Inicio de sesión** con autenticación mediante token JWT
- **Registro de transacciones** (ingresos y gastos) asociadas a categorías
- **Consulta de saldo** en tiempo real con desglose de totales
- **Historial de transacciones** ordenado cronológicamente
- **Estadísticas de gastos** agrupadas por categoría con totales
- **Gestión de categorías** para clasificar movimientos financieros
- **Eliminación de transacciones** con validación de propiedad

---

## Arquitectura del Sistema

El sistema implementa una **arquitectura por capas** adaptada al paradigma REST:

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                      │
│  (Routes / Blueprints - Definición de endpoints y HTTP)       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                    │
│  (Controllers - Orquestación de lógica de negocio)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                            │
│  (Models / DTOs - Entidades ORM y serialización)             │
└─────────────────────────────────────────────────────────────┘
```

### Principios de Diseño

- **Separación de responsabilidades**: Cada capa tiene una función específica
- **Inversión de dependencias**: Los módulos de alto nivel no dependen de implementaciones concretas
- **Single Responsibility**: Cada módulo tiene una única razón para cambiar
- **Registro abstracto**: Los blueprints delegan la lógica a controladores especializados

---

## Estructura del Proyecto

```
proyecto_des_plat/
│
├── app.py                          # Punto de entrada - Instanciación de la app Flask
├── config.py                       # Configuración centralizada (DB, SECRET_KEY)
├── requirements.txt                # Dependencias Python
├── README.md                       # Documentación del proyecto
│
└── src/                            # Paquete principal de la aplicación
    │
    ├── __init__.py                 # Factory de aplicación - Configuración de Flask
    │
    ├── controllers/                # Capa de lógica de negocio
    │   ├── auth_controller.py      # Lógica de autenticación (registro/login)
    │   ├── usuario_controller.py   # Lógica de gestión de usuarios
    │   ├── transaccion_controller.py  # Lógica de transacciones, saldo y estadísticas
    │   └── categoria_controller.py # Lógica de gestión de categorías
    │
    ├── models/                     # Capa de acceso a datos - Entidades ORM
    │   ├── usuario_model.py        # Modelo Usuario (tabla: usuarios)
    │   ├── transaccion_model.py    # Modelo Transaccion (tabla: transacciones)
    │   └── categoria_model.py      # Modelo Categoria (tabla: categorias)
    │
    ├── routes/                     # Capa de presentación - Blueprints Flask
    │   ├── auth_routes.py          # Endpoints: /api/auth/*
    │   ├── usuario_routes.py       # Endpoints: /api/usuarios
    │   ├── transaccion_routes.py   # Endpoints: /api/transacciones, /api/saldo, /api/estadisticas/*
    │   └── categoria_routes.py     # Endpoints: /api/categorias
    │
    ├── dtos/                       # Data Transfer Objects - Serialización y validación
    │   ├── usuario_dto.py          # Schema de serialización para Usuario
    │   ├── transaccion_dto.py      # Schema de serialización para Transaccion
    │   ├── saldo_dto.py            # Schema de serialización para Saldo
    │   └── categoria_dto.py       # Schema de serialización para Categoria
    │
    └── utils/                      # Utilidades y middlewares compartidos
        ├── auth_middleware.py      # Decorador @token_required - Validación JWT
        └── response_helper.py     # Helper de respuestas estandarizadas
```

### Flujo de una Solicitud HTTP

```
Cliente HTTP
     │
     ▼
Routes (Blueprint) ──────► auth_middleware (@token_required)
     │                              │
     ▼                              ▼
Controllers ◄────────── JWT Validation
     │
     ▼
Models (SQLAlchemy) ◄────► MySQL Database
     │
     ▼
DTOs (Marshmallow) ─────► Response JSON
     │
     ▼
Response Helper ──────► Cliente HTTP
```

---

## Requisitos

- **Python**: 3.11 o superior
- **Base de datos**: MySQL 8.0 o superior
- **Servidor web**: Gunicorn (producción) o servidor de desarrollo Flask

---

## Despliegue

### Variables de Entorno

La configuración se gestiona en `config.py`. Parametrizar según el entorno:

```python
class Config:
    # URI de conexión a MySQL con autenticación
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://usuario:password@localhost/nombre_base'
    # Clave secreta para firma de tokens JWT (mínimo 32 caracteres)
    SECRET_KEY = 'tu_clave_secreta_minimo_32_caracteres'
    # Desactivar tracking de modificaciones de SQLAlchemy (optimización)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### Base de Datos

#### Creación de la Base de Datos

Ejecutar el siguiente comando SQL en MySQL:

```sql
CREATE DATABASE MyMoney
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
```

#### Esquema de Tablas

El ORM SQLAlchemy crea las tablas automáticamente al iniciar la aplicación
(en entorno de desarrollo). Para producción se recomienda utilizar Flask-Migrate.

**Tabla: usuarios**
| Columna | Tipo | Constraints |
|---------|------|-------------|
| id_usuario | INT | PRIMARY KEY, AUTO_INCREMENT |
| nombre | VARCHAR(100) | NOT NULL |
| email | VARCHAR(150) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| creado_en | DATETIME | DEFAULT CURRENT_TIMESTAMP |

**Tabla: transacciones**
| Columna | Tipo | Constraints |
|---------|------|-------------|
| id_transaccion | INT | PRIMARY KEY |
| id_usuario | INT | NOT NULL, FOREIGN KEY → usuarios |
| id_categoria | INT | NULLABLE, FOREIGN KEY → categorias |
| monto | DECIMAL(12,2) | NOT NULL |
| descripcion | VARCHAR(255) | NOT NULL |
| fecha_transaccion | DATE | DEFAULT CURRENT_DATE |
| tipo | ENUM('ingreso','gasto') | NOT NULL |

**Tabla: categorias**
| Columna | Tipo | Constraints |
|---------|------|-------------|
| id_categoria | INT | PRIMARY KEY, AUTO_INCREMENT |
| id_usuario | INT | NULLABLE, FOREIGN KEY → usuarios |
| nombre | VARCHAR(50) | NOT NULL |

### Ejecución Local

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd proyecto_des_plat

# 2. Crear y activar entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar credenciales de base de datos en config.py

# 5. Ejecutar la aplicación
python app.py
```

La API estará disponible en `http://localhost:5000`.

### Despliegue en Producción

#### Con Gunicorn (WSGI)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:app"
```

#### Con Docker

`Dockerfile`:

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

#### Consideraciones de Seguridad para Producción

- **SECRET_KEY**: Generar una clave única y segura para cada entorno
- **SSL/TLS**: Usar conexiones cifradas para MySQL
  (`mysql+mysqlconnector://.../?ssl_ca=...`)
- **CORS**: Restringir orígenes permitidos en lugar de usar `*`
- **Variables de entorno**: Gestionar secretos mediante environment variables
- **Rate limiting**: Implementar limitación de peticiones para prevenir ataques
- **Validación de entrada**: Todos los DTOs validan datos de entrada automáticamente

---

## Autenticación

El sistema implementa autenticación mediante **JWT (JSON Web Tokens)**.

### Flujo de Autenticación

```
1. Registro:    POST /api/auth/registro
2. Login:       POST /api/auth/login  ──────► Recibe token JWT
3. Consumo:     Authorization: Bearer <token>
```

### Ejemplo con cURL

```bash
# Login - Obtener token
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "contraseña"}'

# Solicitud protegida - Consultar saldo
curl -X GET http://localhost:5000/api/saldo \
  -H "Authorization: Bearer <tu_token>"
```

---

## Endpoints de la API

### Base URL: `/api`

---

### Auth

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| POST | `/auth/registro` | Registrar nuevo usuario | No |
| POST | `/auth/login` | Iniciar sesión | No |

#### POST /api/auth/registro

Registra un nuevo usuario en el sistema.

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

Autentica un usuario y retorna un token JWT.

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

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| POST | `/transacciones` | Crear nueva transacción | Sí |
| GET | `/transacciones` | Listar historial completo | Sí |
| GET | `/saldo` | Consultar saldo con totales | Sí |
| GET | `/estadisticas/gastos` | Estadísticas de gastos por categoría | Sí |
| DELETE | `/transacciones/{id}` | Eliminar transacción | Sí |

#### POST /api/transacciones

Crea una nueva transacción para el usuario autenticado.

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
| monto | float | Sí | Valor mayor a 0 |
| descripcion | string | Sí | Longitud entre 1 y 255 caracteres |
| tipo | string | Sí | Valores permitidos: "ingreso" o "gasto" |
| id_categoria | integer | No | ID de categoría existente en el sistema |

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

Obtiene el historial completo de transacciones del usuario autenticado.

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

Calcula y retorna el saldo actual del usuario autenticado con desglose de totales.

**Response (200):**

```json
{
  "status": "success",
  "message": "Saldo calculado",
  "data": {
    "id_usuario": 1,
    "total_ingresos": 5000.00,
    "total_gastos": 2340.50,
    "saldo_actual": 2659.50,
    "saldos_por_categoria": [
      {
        "categoria": "Alimentación",
        "total_ingresos": 0.00,
        "total_gastos": 850.00
      },
      {
        "categoria": "Salario",
        "total_ingresos": 5000.00,
        "total_gastos": 0.00
      }
    ]
  }
}
```

#### GET /api/estadisticas/gastos

Retorna estadísticas de gastos agrupadas por categoría.

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

Elimina una transacción existente del usuario autenticado.

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

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| GET | `/usuarios` | Listar todos los usuarios | Sí |

#### GET /api/usuarios

Retorna la lista de usuarios registrados en el sistema.

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

| Método | Endpoint | Descripción | Requiere Auth |
|--------|----------|-------------|---------------|
| GET | `/categorias` | Listar todas las categorías | No |
| GET | `/categorias?tipo=gasto` | Filtrar categorías por tipo | No |

#### GET /api/categorias

Retorna las categorías disponibles. Admite filtrado opcional por tipo de movimiento.

**Parámetros de consulta (opcional):**
- `tipo`: "ingreso" o "gasto"

**Response (200):**

```json
{
  "status": "success",
  "message": "Categorías obtenidas con éxito",
  "data": [
    {
      "id_categoria": 1,
      "nombre": "Alimentación"
    },
    {
      "id_categoria": 2,
      "nombre": "Salario"
    }
  ]
}
```

**Nota**: El atributo `tipo` de movimiento se gestiona en la entidad `Transaccion`,
no en `Categoria`. Esto permite mayor flexibilidad en la clasificación de movimientos.

---

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 | Solicitud procesada exitosamente |
| 201 | Recurso creado exitosamente |
| 400 | Error de validación en los datos de entrada |
| 401 | No autenticado o token JWT inválido/expirado |
| 404 | Recurso no encontrado |
| 500 | Error interno del servidor |

---

## Tecnologías

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Framework web | Flask | 3.0.0 |
| ORM | SQLAlchemy + Flask-SQLAlchemy | 3.1.1 |
| Serialización | Marshmallow + Flask-Marshmallow | 1.2.0 |
| Autenticación | PyJWT | 2.8.0 |
| Hashing passwords | Werkzeug | (incluido en Flask) |
| Base de datos | MySQL | 8.0 |
| Driver MySQL | mysql-connector-python | 8.2.0 |
| CORS | Flask-CORS | 4.0.0 |
| Servidor WSGI | Gunicorn | (producción) |

---

*Documentación generada para MyMoney API v1.0*