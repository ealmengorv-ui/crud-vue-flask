# CRUD Vue 3 + Axios + Flask

Aplicación de ventas para Windows con CRUD de **clientes, productos y pedidos**.

## Tecnologías

- Frontend: Vue 3, Vue Router, Axios y Vite.
- Backend: Flask, Flask-SQLAlchemy, Flask-Migrate y Flask-CORS.
- Base de datos de desarrollo: SQLite.
- Pruebas: pytest.

## Estructura

```text
crud-vue-flask/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── extensions.py
│   │   └── models.py
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
└── frontend/
    ├── src/
    │   ├── api/
    │   ├── assets/
    │   ├── components/
    │   ├── router/
    │   ├── views/
    │   ├── App.vue
    │   └── main.js
    ├── .env.example
    ├── package.json
    └── vite.config.js
```

### Organización

- `backend/app/models.py`: define las tablas y relaciones con SQLAlchemy.
- `backend/app/api/`: contiene los endpoints REST por recurso.
- `frontend/src/api/`: centraliza Axios y las llamadas HTTP.
- `frontend/src/components/`: componentes reutilizables.
- `frontend/src/views/`: páginas asociadas a las rutas.
- `frontend/src/router/`: navegación con Vue Router.

## 1. Ejecutar backend en Windows

En PowerShell:

```powershell
cd backend
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
Copy-Item .env.example .env
flask --app run.py db upgrade
flask --app run.py run --debug
```

Backend: `http://localhost:5000`

Prueba rápida:

```powershell
Invoke-RestMethod http://localhost:5000/health
```

## 2. Ejecutar frontend en Windows

Abrir otra terminal PowerShell:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Frontend: normalmente `http://localhost:5173`

## 3. Pruebas backend

```powershell
cd backend
.venv\Scripts\Activate.ps1
pytest
```

## Funcionalidad

### Clientes
- Crear, listar, editar y eliminar.
- Nombre y correo obligatorios.
- Correo único.
- No se permite eliminar clientes con pedidos.

### Productos
- Crear, listar, editar y eliminar.
- Nombre, precio y stock obligatorios.
- Precio y stock no pueden ser negativos.
- No se permite eliminar productos con pedidos.

### Pedidos
- Crear y listar pedidos.
- Cada pedido usa un cliente y un producto.
- La cantidad debe ser mayor que cero y no puede superar el stock.
- Al crear un pedido se descuenta stock.
- El estado puede ser `pendiente`, `pagado`, `enviado` o `cancelado`.
- Solo se eliminan pedidos cancelados.

## Nota de diseño

Para mantener el ejercicio simple, cada pedido contiene un solo producto. En una aplicación comercial real convendría usar una tabla de detalle de pedidos para admitir varios productos por pedido y guardar el precio histórico.
