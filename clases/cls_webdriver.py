from scripts.connections import iniciar_driver

class WebDriverManager:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = iniciar_driver()
        return cls._driver

    @classmethod
    def close_driver(cls):
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None