from secrets import GPU_FIEND

class Product:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.seller = url.split("/")[2]

    def toNotificationText(self):
        return f'''{GPU_FIEND}: {self.name} is available at {self.seller}!\n{self.url}'''