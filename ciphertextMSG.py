import message

class CiphertextMSG(message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            super().__init__(rsaEncrypt(text))
        if encryptionType == 'cesar':
            super().__init__(cesarEncrypt(text))

    def rsaEncrypt(text):
        #do RSA encryption
        pass

    def cesarEncrypt(text):
        #do cesar cypher encryption
        pass

