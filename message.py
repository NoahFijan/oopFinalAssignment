class Message:
    def __init__(self, text):
        self.message = text

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, text):
        self._message = text
    
