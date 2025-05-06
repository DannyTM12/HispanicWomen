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

def connection_example(cadena):
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

def revisar_credenciales(driver,username,password):
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
        WebDriverWait(driver, 15).until(EC.url_contains("/home"))
        return True
    except TimeoutException:
        return False
    

def ingresar_caja(driver):
    """
        Al iniciar sesion, se despliega un modal para la seleccion de 
        la caja. Se ingresa un pin y se seleccionan la caja disponible
        para continuar.
    """
    # buscar el modal para seleccionar caja
    modalCaja = encontrar_componentes.encontrarModalCaja(driver)

    if modalCaja and modalCaja.is_displayed():

        # encontramos el componente selector para sucursal
        componenteSelectorSucursal = encontrar_componentes.encontrarSelector(modalCaja, "selectSucursal")

        if componenteSelectorSucursal:
            selectorSucursal = Select(componenteSelectorSucursal)
            
            selectorSucursal.select_by_index(1)
            time.sleep(2)

            # driver.quit()
            return "seleccionado!"

        else:
            return "No se encontro selectorSucursal"

    return "modal caja desplegado"

def connection_login(username,password):
    """
        Recibe el username y la contrasena del usuario.
    """
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

    url_login = url + "/login"
    driver.get(url_login)
    
    if revisar_credenciales(driver,username, password):

        ingresar_caja(driver)

    else: 
        driver.quit()
        return "Credenciales incorrectas."
    


    # Cerrar navegador al final
    # driver.quit()
    return "Login, finalizado!"