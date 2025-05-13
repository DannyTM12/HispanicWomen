

class AtributoCambio(object):
    """
        Revisa si un atributo especifico del elemento ha cambiado.
    """
    def __init__(self, elemento, attribute, previous_value):
        self.elemento = elemento
        self.attribute = attribute
        self.previous_value = previous_value

    def __call__(self, driver):
        try:
            current_value = self.elemento.get_attribute(self.attribute)
            return current_value != self.previous_value
        except Exception:
            return False