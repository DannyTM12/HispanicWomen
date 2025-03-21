from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def connection_example(cadena):
    # Configuración de opciones para el navegador (modo headless)
    options = Options()
    options.add_argument('--headless')  # Ejecuta el navegador en segundo plano
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