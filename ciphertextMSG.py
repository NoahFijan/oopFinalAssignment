from message import Message

class CiphertextMSG(Message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            plaintext = self.rsaDecrypt(text)
            super().__init__(plaintext)

        if encryptionType == 'cesar':
            super().__init__(self.cesarEncrypt(text))

        if encryptionType == 'playfair':
            super().__init__(self.playfairEcrypt(text))
    

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

    def playfairDecrypt(self, text):
        text = text.replace(" ", "")
        text = text.upper()
        listEncrPair = []
        c = 0
        while c < len(text):
            if c + 1 < len(text):
                if text[c] == text[c + 1]:
                    listEncrPair.append((text[c], 'X'))
                    c += 1
                    continue
                listEncrPair.append((text[c], text[c + 1]))
                c += 2
                continue
            listEncrPair.append((text[c], 'X'))
            c += 1

        key = [["P", "L", "A", "Y", "F"],
               ["I", "R", "E", "J", "M"],
               ["B", "C", "D", "G", "H"],
               ["K", "N", "O", "Q", "S"],
               ["T", "U", "V", "W", "Z"]]
        listPair = []
        while (len(listEncrPair)) > 0:
            rCheck = False
            cCheck = False
            pair = listEncrPair[0]
            pos1 = -1
            pos2 = -1
            for row in range(len(key)):
                if (pair[0] in key[row]) & (pair[1] in key[row]):  # FOR SURE R0W CHECK
                    rCheck = True
                    for item in key[row]:
                        if pair[0] == item:
                            pos1 = key[row].index(item) - 1
                            if pos1 < 0: pos1 += 5
                        if pair[1] == item:
                            pos2 = key[row].index(item) - 1
                            if pos2 < 0: pos2 += 5
                    listPair.append((key[row][pos1], key[row][pos2]))
                    listEncrPair.pop(0)
            for z in range(len(key)):
                pos1 = -1
                pos2 = -1
                for row in range(len(key)):
                    if pair[0] == key[row][z]:
                        pos1 = row - 1
                        if pos1 < 0: pos1 += 5
                    if pair[1] == key[row][z]:
                        pos2 = row - 1
                        if pos2 < 0: pos2 += 5
                    if (pos1 > -1) & (pos2 > -1):
                        cCheck = True
                        listPair.append((key[pos1][z], key[pos2][z]))
                        listEncrPair.pop(0)
                        break
            if not (rCheck + cCheck) & (len(listEncrPair) > 0):
                x1, y1 = -1, -1
                x2, y2 = -1, -1
                for y in range(len(key)):
                    for x in range(len(key[y])):
                        if pair[0] == key[y][x]:
                            x1 = x
                            y1 = y
                        if pair[1] == key[y][x]:
                            x2 = x
                            y2 = y
                listPair.append((key[y1][x2], key[y2][x1]))
                listEncrPair.pop(0)
        decryptString = ""
        for tpl in listPair:
            for char in tpl:
                if char != 'X':
                    decryptString += char

        return decryptString


if __name__ == '__main__':
    a = CiphertextMSG([1050, 1283, 807, 807, 2905, 3576, 1683, 2905, 50, 807, 174, 3096], 'RSA')
    print(a.message)

