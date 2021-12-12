class Product:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def toNotificationText(self):
        return f'''<@&919645969270841364>: {self.name} is available!\n{self.url}'''