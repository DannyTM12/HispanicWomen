    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    # Configurar el navegador (usa Chrome, Edge o Firefox)
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Abrir en pantalla completa
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # URL del sistema
    url = "https://mujerhispana.maspunto.online/login"
    driver.get(url)

    # 1. Iniciar sesión
    usuario = "caja1@app"
    password = "caja1"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(usuario)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password + Keys.RETURN)

    # Esperar a que cargue el dashboard
    WebDriverWait(driver, 10).until(EC.url_contains("/home"))

    # Navegar a la sección de "Cuentas por cobrar"
    driver.get("https://mujerhispana.maspunto.online/cuentacobrars")

    # Esperar a que cargue la sección
    WebDriverWait(driver, 10).until(EC.url_contains("/cuentacobrars"))

    # 2. Hacer clic en el campo de búsqueda de clientes para abrir la lista
    select_cliente = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "vs__search")))
    select_cliente.click()

    # 3. Esperar a que aparezca la lista de clientes
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vs1_listbox")))

    # 4. Extraer los nombres de los clientes
    clientes = driver.find_elements(By.XPATH, "//ul[@id='vs1_listbox']/li")

    # Guardar en una lista
    lista_clientes = [cliente.text for cliente in clientes if cliente.text.strip()]
    print("Lista de clientes disponibles:")
    print(lista_clientes)
    
    '''
    for cliente in clientes:
        print(f" Buscando datos de {cliente}...")

        #  3. Interactuar con el campo de selección de clientes
        select_cliente = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "vs__search")))
        select_cliente.clear()  # Limpiar antes de escribir
        select_cliente.send_keys(cliente)
        time.sleep(1)  # Esperar a que aparezca la lista

        # Seleccionar el primer resultado de la lista
        select_cliente.send_keys(Keys.RETURN)

        #  4. Hacer clic en "Aplicar" para filtrar
        aplicar_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aplicar')]")))
        aplicar_btn.click()

        #  5. Esperar a que carguen los datos
        time.sleep(3)  # Ajusta el tiempo según la carga

        #  6. Extraer la información de "Total cuentas por cobrar"
        total_cobrar = driver.find_element(By.XPATH, "//div[contains(text(), 'Total cuentas por cobrar')]/following-sibling::div").text
        print(f" Total cuentas por cobrar de {cliente}: {total_cobrar}\n")
    '''
    
    # Cerrar navegador al final
    driver.quit()
