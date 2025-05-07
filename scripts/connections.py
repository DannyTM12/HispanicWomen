from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
import time

from flask import jsonify

from . import encontrar_componentes

# Configurar el navegador (usa Chrome, Edge o Firefox)
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

url = "https://mujerhispana.maspunto.online"

# ---------------------------- Driver -------------------------------

def iniciar_driver():
    """
        Inicia las configuraciones del driver. Retorna el driver.
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
                # with 2 should disable notifications
            },
        )

        options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2}) 

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        return driver, "Driver iniciado!"
    except Exception as e:
        return None, f"Ha ocurrido un error: {e}"

# ------------------------------- Login ------------------------------

def revisar_credenciales(driver, username, password):
    """
        Ingresa las credenciales para ingresar a home.
        Se espera que se pueda ingresar a home hasta cierto tiempo
        en caso de no lograrlo, se considera que las credenciales
        son incorrectas o hubo un error.
    """
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password + Keys.RETURN)
        # Esperar a que cargue el dashboard
        WebDriverWait(driver, 20).until(EC.url_contains("/home"))
        return True
    except TimeoutException:
        return False

def ingresar_login(driver, username, password):
    """
        Recibe el username y la contrasena del usuario. Inicia sesion,
        si es valido retorna True, de lo contrario,
        retorna False y el valor del driver es None.
    """
    url_login = url + "/login"
    driver.get(url_login)
    
    if revisar_credenciales(driver,username, password):
        return True

    else: 
        driver.quit()
        return False

# ---------------------- Cajas --------------------------------------------
def obtener_componentes_caja(driver):
    """
        Al iniciar sesion, se despliega un modal para la seleccion de 
        la caja. Se obtienen los valores de los selectores.
        En caso de no encontrar el modal ser retorna None.
    """
    # buscar el modal para seleccionar caja
    modalCaja = encontrar_componentes.encontrarModalCaja(driver)

    if modalCaja and modalCaja.is_displayed():

        # almacenamos los valores de los selectores
        valoresSelectores = {}

        # encontramos el componente selector para sucursal
        componenteSelectorSucursal = encontrar_componentes.encontrarComponenteID(modalCaja, "selectSucursal")

        # si encuentra el selector sucursal
        if componenteSelectorSucursal:

            selectSucursal = Select(componenteSelectorSucursal)

            for index, opcion_sucursal in enumerate(selectSucursal.options):

                # almacenamos la opcion
                valoresSelectores[f"{opcion_sucursal.text}"] = []

                # seleccionamos la opcion actual
                selectSucursal.select_by_index(index)

                # encontramos el selector de caja con las opciones para esta sucursal
                componenteSelectorCaja = encontrar_componentes.encontrarComponenteID(modalCaja, "selectCaja")

                # si encuentra el selector caja
                if componenteSelectorCaja:

                    selectCaja = Select(componenteSelectorCaja)

                    for opcion_caja in selectCaja:

                        if opcion_caja.get_attribute("disabled"):
                            # si la opcion no esta disponible
                            continue

                        # agregamos la opcion de caja a la variable de la sucursal
                        valoresSelectores[f"{opcion_sucursal.text}"].append(opcion_caja.text)

        return valoresSelectores

    # no se encontro el modal para ingresar caja
    return None

# -------------------------- Ejemplo de conexion -----------------------------------
    
def connection_example(cadena):
    """
         Ejemplo de conexion. 
    """
    # Configuración de opciones para el navegador (modo headless)
    options = Options()
    # options.add_argument('--headless')  # Ejecuta el navegador en segundo plano
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Inicialización del controlador del navegador (ChromeDriver)
    driver = webdriver.Chrome(options=options)

    # Navegación a Google
    driver.get('https://www.google.com')

    # Encontrar el campo de búsqueda y escribir una consulta
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(cadena)
    search_box.send_keys(Keys.RETURN)

    # Esperar unos segundos para que se carguen los resultados
    time.sleep(5)

    # Imprimir el título de la página de resultados
    titulo = driver.title

    # Cerrar el navegador
    driver.quit()

    return titulo