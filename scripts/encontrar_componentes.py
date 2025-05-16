from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def encontrarModalCaja(driver):
    """
        Busca el modal utilizado para la seleccion de caja e ingreso del pin.
        Retorna el objeto del modal si es encontrado, de lo contrario sera null.
    """

    try:
        # examinar si se encuentra pantalla de registro de caja
        modalCaja = driver.find_element(By.ID, "seleccionarTienda")
        return modalCaja
    except NoSuchElementException:
        return None
    
def encontrarComponenteID(Padre,cadena_id):
    """
        A partir del padre, busca el componente por ID. Si la encuentra retorna el componente, 
        de lo contrario None.
    """
    try:
        componente = Padre.find_element(By.ID, cadena_id)
        return componente
    except NoSuchElementException:
        return None