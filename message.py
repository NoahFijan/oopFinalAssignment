class Message:
    def __init__(self, text):
        '''
        this innitalizes the message object
        '''
        self.message = text

    @proporty
    def message(self):
        return self._text

    @message.setter
    def value(self, text):
        self._text = text

    
