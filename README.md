# Dashboard Mujer Hispana

![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=flat-square&logo=selenium&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

---

## Contexto

**Mujer Hispana** es una cadena de tiendas de crédito con múltiples sucursales en Aguascalientes. Su sistema de punto de venta (`maspunto.online`) no expone una API pública para consultar cuentas por cobrar — la única forma de acceder a esa información era navegando manualmente por el sistema, sucursal por sucursal.

Este proyecto automatiza ese proceso: inicia sesión en el POS, selecciona sucursal y caja, extrae los registros de cuentas por cobrar y los presenta en un dashboard web con roles de usuario.

---

## ¿Qué hace?

- **Automatización del POS:** login headless con Selenium, validación de sucursal + caja + PIN, extracción de cuentas por cobrar
- **Dashboard web:** interfaz Flask con autenticación propia y roles (Administrador / Analista)
- **Registro de extracciones:** cada extracción queda guardada en base de datos con fecha y usuario responsable
- **Despliegue containerizado:** imagen Docker lista para cualquier entorno

---

## Arquitectura

```
Usuario
   │
   ▼
Flask App (auth + dashboard)
   │
   ├── Flask-Login  →  autenticación de usuarios con roles
   ├── SQLAlchemy   →  SQLite (User, Profile, Extraccion, Registro)
   │
   └── Selenium WebDriver (headless Chromium)
          │
          └── maspunto.online (POS Mujer Hispana)
                 ├── /login          → credenciales POS
                 ├── /home           → modal sucursal/caja/pin
                 └── /cuentacobrars  → extracción de datos AR
```

**Flujo de extracción:**
1. El usuario se autentica en el dashboard
2. Selecciona sucursal, caja e ingresa el PIN del POS
3. Selenium inicia sesión en `maspunto.online` en segundo plano
4. Extrae los registros de cuentas por cobrar y los guarda como `Extraccion` + `Registro` en SQLite
5. El dashboard presenta los datos al usuario según su perfil

---

## Stack

| Capa | Tecnología |
|---|---|
| Backend | Python 3.9 · Flask 3.1 · Blueprint routing |
| Autenticación | Flask-Login · Werkzeug (password hashing) |
| Base de datos | SQLite · SQLAlchemy · Flask-Migrate |
| Scraping | Selenium WebDriver · WebDriver Manager · Chromium headless |
| Frontend | Jinja2 · Bootstrap 5 · JavaScript |
| Despliegue | Docker |

---

## Quickstart

### Con Docker (recomendado)

```bash
git clone https://github.com/DannyTM12/HispanicWomen.git
cd HispanicWomen

# Crea un archivo .env con tus variables
echo "SECRET_KEY=tu_clave_secreta" > .env

docker build -t hispanic-women .
docker run -p 9000:9000 --env-file .env hispanic-women
```

Accede en `http://localhost:9000`.

### Local (sin Docker)

**Requisitos:** Python 3.9+ · Google Chrome o Chromium instalado

```bash
git clone https://github.com/DannyTM12/HispanicWomen.git
cd HispanicWomen

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

---

## Estructura del proyecto

```
HispanicWomen/
├── clases/
│   ├── cls_webdriver.py      # Singleton WebDriverManager
│   └── cls_driverwait.py     # Custom expected condition para Selenium
├── endpoints/
│   └── auth.py               # Blueprint de autenticación y dashboard
├── scripts/
│   ├── connections.py        # Lógica de automatización del POS
│   └── encontrar_componentes.py  # Helpers para localizar elementos DOM
├── templates/                # Vistas Jinja2 (login, registro, dashboard, caja)
├── static/
│   └── acceso/selectores.js  # Selector dinámico sucursal → caja
├── app.py                    # Entry point, rutas principales
├── models.py                 # User · Profile · Extraccion · Registro
├── forms.py                  # WTForms (registro, login)
├── config.py                 # Configuración desde variables de entorno
├── requirements.txt
└── Dockerfile
```

---

## Variables de entorno

| Variable | Descripción | Default |
|---|---|---|
| `SECRET_KEY` | Clave secreta Flask | — (requerida) |
| `DATABASE_URL` | URI de base de datos | `sqlite:///site.db` |

---

## Modelos de datos

```
User ──< user_profiles >── Profile
 │
 └──< Extraccion >──< Registro
```

- **User:** usuario del dashboard con contraseña hasheada y uno o más perfiles
- **Profile:** rol de acceso (Administrador, Analista)
- **Extraccion:** registro de cada sesión de scraping (fecha, usuario)
- **Registro:** fila extraída del POS (folio, tienda, total, abonado, debe, vencimiento)

---

## Notas técnicas

- El WebDriver se gestiona como singleton (`WebDriverManager`) para evitar instancias duplicadas entre requests
- La selección de caja es dinámica: al cambiar sucursal se filtran las cajas disponibles vía JS sin recargar página
- Selenium usa `AtributoCambio` como expected condition personalizada para detectar la validación del PIN (cambio de clase `btn-secondary` → `btn-success`)
- El sistema libera la caja antes de cerrar sesión para evitar bloqueos en el POS

---

## Licencia

Proyecto desarrollado para uso interno. No afiliado oficialmente con Mujer Hispana ni con maspunto.online.