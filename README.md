# 💰 MyMoney - Gestión de Finanzas Personales
> "Toma el control de tu dinero, un registro a la vez."

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=flat&logo=flask&logoColor=white)
![Angular](https://img.shields.io/badge/angular-%23DD0031.svg?style=flat&logo=angular&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=flat&logo=mysql&logoColor=white)

---

## 🌟 Características
* ✅ **Registro Rápido:** Ingresa tus gastos e ingresos en segundos.
* 📊 **Saldo en Tiempo Real:** Visualiza cuánto dinero tienes disponible mediante cálculos precisos.
* 🏷️ **Categorización:** Clasifica tus movimientos (Comida, Transporte, Salario, etc.).
* 🛡️ **Seguridad:** Arquitectura robusta siguiendo el patrón **MVC**.

---

## 🏗️ Arquitectura del Sistema (MVC)
El proyecto está estructurado para separar la lógica de los datos de la interfaz de usuario:

* **Modelos:** Gestión de la base de datos con SQLAlchemy.
* **Vistas (Rutas):** Definición de la API REST mediante Blueprints.
* **Controladores:** Lógica de negocio y cálculos matemáticos.
* **DTOs:** Validación de datos con Marshmallow.

---

## 🛠️ Configuración del Entorno

### 1. Clonar y Preparar
```bash
git clone [https://github.com/tu-usuario/MyMoney.git](https://github.com/tu-usuario/MyMoney.git)
cd MyMoney/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Base de Datos
Asegúrate de tener MySQL corriendo y crear la base de datos MyMoney.

💡 Tip: No olvides configurar tus credenciales en el archivo config.py.


📑 Documentación de la API
Método,Endpoint,Descripción,Status
POST,/api/transacciones,Registra un nuevo movimiento.,201 Created
GET,/api/saldo,Consulta el saldo total del usuario.,200 OK

Ejemplo de petición (HU 1):
{
  "id_usuario": 1,
  "monto": 150.50,
  "descripcion": "Suscripción Netflix",
  "tipo": "gasto",
  "id_categoria": 6
}

🚀 Hoja de Ruta (Roadmap)
[x] Sprint 1: MVP - Registro y Saldo.

[ ] Sprint 2: Historial y Categorías.

[ ] Sprint 3: Gráficos Estadísticos.