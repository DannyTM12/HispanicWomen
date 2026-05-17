# Dashboard Mujer Hispana - Autoevaluación y Web Scraping

Una aplicación web desarrollada con **Flask** diseñada para automatizar el inicio de sesión, la validación de cajas y la extracción de datos (Web Scraping) del sistema de punto de venta de Mujer Hispana mediante **Selenium WebDriver**.

## 🚀 Características Principales

* **Automatización Web:** Uso de Selenium para interactuar con la plataforma `maspunto.online` en segundo plano (headless mode) y extraer información relevante como cuentas por cobrar.
* **Gestión de Sesiones en Punto de Venta:** Scripts dedicados para validar sucursales, cajas y pines de acceso de forma automatizada.
* **Sistema de Usuarios y Autenticación:** Registro e inicio de sesión seguro (contraseñas hasheadas) utilizando `Flask-Login` y `Werkzeug`.
* **Roles de Usuario:** Perfiles definidos (Ej. Administrador, Analista) para controlar los privilegios de los usuarios.
* **Base de Datos:** Integración con SQLite a través de `Flask-SQLAlchemy` para guardar registros de extracción y perfiles de usuario.
* **Contenedorización:** Listo para desplegarse en cualquier entorno utilizando Docker.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.9, Flask, Blueprint routing.
* **Base de Datos:** SQLite, SQLAlchemy, Flask-Migrate.
* **Web Scraping:** Selenium WebDriver, WebDriver Manager.
* **Frontend:** HTML5, Jinja2, Bootstrap 5, JavaScript puro.
* **Despliegue:** Docker.

## 📂 Estructura del Proyecto

* `/clases`: Clases de soporte para el manejo y esperas del WebDriver (Selenium).
* `/endpoints`: Controladores de rutas modulares (ej. autenticación `auth.py`).
* `/scripts`: Lógica central de conexión, interacciones web y búsqueda de componentes HTML con Selenium.
* `/templates`: Vistas HTML renderizadas con Jinja2 (Dashboards, formularios de login, selectores de caja).
* `/static`: Archivos estáticos como JavaScript (`selectores.js`) y estilos.
* `app.py`: Archivo principal que inicializa el servidor Flask y define las rutas principales.
* `models.py`: Modelos de la base de datos (User, Profile, Extraccion, Registro).

## ⚙️ Requisitos Previos

Si deseas ejecutar el proyecto de manera local (sin Docker), asegúrate de tener instalado:
* Python 3.9 o superior.
* Google Chrome (o Chromium) instalado en tu sistema.

## 💻 Instalación y Uso Local

1. **Clonar el repositorio** e ingresar al directorio del proyecto.
2. **Crear un entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
