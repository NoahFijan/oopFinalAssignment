import message

class CiphertextMSG(message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            super().message = rsaEncrypt(text)
        if encryptionType == 'cesar':
            super().message = cesarEncrypt(text)

    def rsaEncrypt(text):
        #do RSA encryption
        pass

    def cesarEncrypt(text):
        #do cesar cypher encryption
        pass

