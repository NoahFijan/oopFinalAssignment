from message import Message

class CiphertextMSG(Message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            plaintext = self.rsaDecrypt(text)
            super().__init__(plaintext)

        if encryptionType == 'cesar':
            super().__init__(self.cesarEncrypt(text))
    

    def readPrivKey(self):
        '''
        Reads private key components from a the private key file generated in the 
        PlaintextMSG.py file and returns them 
        '''
        f = open('priv.txt', 'r')
        n = f.readline()
        d = f.readline()
        f.close()
        return int(n), int(d)

    
    def rsaDecrypt(self, text):
        '''
        Takes the encrypted message as input and and returns the decrypted message
        '''
        n, d = self.readPrivKey() #get private key

        dec = [chr((char ** d) % n) for char in text]
    
        return ''.join(dec)

    def cesarEncrypt(self, text):
        #do cesar cypher encryption
        pass

    def playfairEcrypt(self, text):
        #noah playfair
        pass

    def transpositionEncrypt(self, text):
        #noah transp
        pass

    def productCipher(self, text):
        #do product cipher
        pass


if __name__ == '__main__':
    a = CiphertextMSG([1050, 1283, 807, 807, 2905, 3576, 1683, 2905, 50, 807, 174, 3096], 'RSA')
    print(a.message)

