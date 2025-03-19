import requests
from bs4 import BeautifulSoup

# URLs del login y la página de cuentas por cobrar
login_url = "https://mujerhispana.maspunto.online/login"
home_url = "https://mujerhispana.maspunto.online/home"
cuentas_url = "https://mujerhispana.maspunto.online/cuentas-por-cobrar"  # Ajusta la URL real

# Datos de inicio de sesión (ajusta los nombres de los campos)
payload = {
    "username": "tu_usuario",
    "password": "tu_contraseña"
}

# Crear una sesión
session = requests.Session()

# Hacer login
response = session.post(login_url, data=payload, allow_redirects=True)

# Verificar si el login fue exitoso
if response.status_code == 200 and "Dashboard" in response.text:
    print("✅ Login exitoso")

    # Acceder a la página de cuentas por cobrar
    cuentas_response = session.get(cuentas_url)

    # Analizar el HTML
    soup = BeautifulSoup(cuentas_response.text, "html.parser")

    # Extraer datos de cuentas por cobrar (ajusta el selector)
    cuentas = soup.find_all("div", class_="nombre-de-la-clase")  # Cambia por la clase real

    for cuenta in cuentas:
        print(cuenta.text)

else:
    print("❌ Error en el login")
