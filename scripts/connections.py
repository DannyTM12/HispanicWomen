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
from clases.cls_driverwait import AtributoCambio

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
        options.add_argument("--disable-notifications")
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
                "profile.password_manager_leak_detection": False 
                # with 2 should disable notifications
            },
        )
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    
    except Exception as e:
        return None

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
        WebDriverWait(driver, 10).until(EC.url_contains("/home"))
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

# ---------------------- Ingresar Cajas --------------------------------------------
def obtener_componentes_caja(driver):
    """
        Al iniciar sesion, se despliega un modal para la seleccion de 
        la caja. Se obtienen los valores de los selectores.
        En caso de no encontrar el modal ser retorna None.
    """
    # esperamos a que se encuentre en home
    WebDriverWait(driver, 10).until(EC.url_contains("/home"))
    # buscar el modal para seleccionar caja
    modalCaja = encontrar_componentes.encontrarModalCaja(driver)

    if modalCaja:

        # almacenamos los valores de los selectores
        valoresSelectores = {}

        # obtenemos el componente selector sucursal
        componenteSelectorSucursal = encontrar_componentes.encontrarComponenteID(modalCaja, "selectSucursal")

        if componenteSelectorSucursal:
            
            # indicamos como selector sucursal
            selectorSucursal = Select(componenteSelectorSucursal)

            for index_sucursal,opcion_sucursal in enumerate(selectorSucursal.options):

                valoresSelectores[opcion_sucursal.text] = {"index_sucursal": index_sucursal, "opciones": []}

                # seleccionamos la sucursal actual

                selectorSucursal.select_by_index(index_sucursal)

                # obtenemos el componente selector caja

                componenteSelectorCaja = encontrar_componentes.encontrarComponenteID(modalCaja, "selectCaja")

                if componenteSelectorCaja:

                    # indicamos componente como selector caja

                    selectorCaja = Select(componenteSelectorCaja)

                    for index_caja, opcion_caja in enumerate(selectorCaja.options):

                        if opcion_caja.get_attribute("disabled"):
                            continue

                        valoresSelectores[opcion_sucursal.text]["opciones"].append({"caja": opcion_caja.text, "index_caja": index_caja})

            # solo dejaremos las sucursales con opciones disponibles
            valoresSelectoresDisponibles = {}

            for clave,valor in valoresSelectores.items():

                if len(valor["opciones"]) > 0:
                    valoresSelectoresDisponibles[clave] = valor

            return valoresSelectoresDisponibles

    # no se encontro el modal para ingresar caja
    return None

def validar_pin(driver, modalCaja, pin):
    """
        Verifica si el pin ingresado fue aceptado. Para esto, revisa
        si el boton Validar cambia el estado a "btn-success", para este 
        caso retorna True, de lo contrario False.
    """
    
    botonValidar = modalCaja.find_element(By.CLASS_NAME, "btn-secondary")

    if botonValidar:
        # ingresamos pin
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inlineFormInputGroup"))).send_keys(pin)
        # presionamos boton validar
        botonValidar.click()
        # esperamos a que cambie el boton
        time.sleep(2)

        # obtenemos botonValidar despues de cambios (success)
        cambioBotonValidar = modalCaja.find_element(By.CLASS_NAME, "btn-success")

        # revisamos si el boton se encuentra
        if cambioBotonValidar:

            if cambioBotonValidar.get_attribute("disabled"):
                # obtenemos el botones del modal
                botonesModal = modalCaja.find_elements(By.CLASS_NAME, "bg-button-general")

                botonGuardar = None
                # buscamos el boton que contenga el texto Guardar
                for boton in botonesModal:

                    if boton.text == "Guardar":
                        botonGuardar = boton
                        break

                if botonGuardar:
                    # si hay boton guardar
                    botonGuardar.click()
                    return {"resultado": True, "mensaje": "Credenciales validadas con exito!"}
                
                else:
                    return {"resultado": False, "mensaje": "CNo se encontro boton Guardar."}
            
            # si el boton validar no esta deshabilitado
            else:
                return {"resultado": False, "mensaje": "Pin incorrecto."}
    
    return {"resultado": False, "mensaje": "Hubo un problema al validar el pin. Intente de nuevo."}

def validar_caja(driver, sucursal, caja, pin):
    """
        Se ingresa el registro de caja.
    """
    # buscar el modal para seleccionar caja
    modalCaja = encontrar_componentes.encontrarModalCaja(driver)
    # encontramos el componente selector para sucursal
    componenteSelectorSucursal = encontrar_componentes.encontrarComponenteID(modalCaja, "selectSucursal")
    # buscamos el componente una vez seleccionado la sucursal
    componenteSelectorCaja = encontrar_componentes.encontrarComponenteID(modalCaja, "selectCaja")

    # implementamos select para los componentes
    selectSucursal = Select(componenteSelectorSucursal)
    # seleccionamos la opcion sucursal
    selectSucursal.select_by_index(sucursal)

    selectCaja = Select(componenteSelectorCaja)
    # seleccionamos la opcion caja
    selectCaja.select_by_index(caja)

    # se obtiene el resultado de ingresar el pin y un mensaje
    return validar_pin(driver, modalCaja, pin)



def elemnto_clickleable(driver, componente):
    try:
        componente.click()
        return componente.get_attribute('class')
    except Exception:
        return None
    
# ----------------- Liberar Cajas -------------------

def liberar_caja(driver):
    """
        Con todo respeto, esta mierda bloquea la sesion de la caja si 
        haces logout unicamente, entonces hay que liberar la caja
        antes de cerrar la sesion del navegador.

        La siguiente funcion, ubica el modal de cambio de caja, ingresa
        el pin y presiona liberar caja.
    """
    
    WebDriverWait(driver, 10).until(EC.url_contains("/home"))

    # obtenemos el boton para cambiar caja
    componenteBtnCambiarCaja = driver.find_elements(By.XPATH, "//nav//a")

    if componenteBtnCambiarCaja:
        clases = []

        for componente in componenteBtnCambiarCaja:
            clases.append(elemnto_clickleable(driver, componente))

        return clases

    return "No se encontro el elemento"




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