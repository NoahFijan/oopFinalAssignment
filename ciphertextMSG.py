from message import Message
import json


class CiphertextMSG(Message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            plaintext = self.rsaDecrypt(text)
            super().__init__(plaintext)
        elif encryptionType == 'Playfair':
            plaintext = self.playfairDecrypt(text)
            super().__init__(plaintext)
        elif encryptionType == 'Transposition':
            plaintext = self.transpositionDecrypt(text)
            super().__init__(plaintext)
        elif encryptionType == 'Product':
            plaintext = self.productDecrypt(text)
            super().__init__(plaintext)
        elif encryptionType == 'Caesar':
            plaintext = self.caesarDecrypt(text)
            super().__init__(plaintext)
        elif encryptionType == 'Substitution':
            plaintext = self.substitutionDecrypt(text)
            super().__init__(plaintext)
            
    def readPrivKey(self):
        """
        Reads private key components from a the private key file generated in the
        PlaintextMSG.py file and returns them
        """
        f = open('priv.txt', 'r')
        n = f.readline()
        d = f.readline()
        f.close()
        return int(n), int(d)

    def rsaDecrypt(self, text):
        """
        Takes the encrypted message as input and and returns the decrypted message
        """
        n, d = self.readPrivKey()  # get private key

        dec = [chr((char ** d) % n) for char in text]

        return ''.join(dec)

    def playfairDecrypt(self, text):
        # SEE PLAYFAIR ENCRYPT FOR DOCUMENTATION, repeated process for decryption with some minor changes
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
                if (pair[0] in key[row]) & (pair[1] in key[row]):
                    rCheck = True
                    for item in key[row]:
                        if pair[0] == item:
                            pos1 = key[row].index(
                                item) - 1  # choose the position shifted to the left (opposite to encryption)
                            if pos1 < 0: pos1 += 5
                        if pair[1] == item:
                            pos2 = key[row].index(
                                item) - 1  # choose the position shifted to the left (opposite to encryption)
                            if pos2 < 0: pos2 += 5
                    listPair.append((key[row][pos1], key[row][pos2]))
                    listEncrPair.pop(0)
            for z in range(len(key)):
                pos1 = -1
                pos2 = -1
                for row in range(len(key)):
                    if pair[0] == key[row][z]:
                        pos1 = row - 1  # choose the position shifted upwards (opposite to encryption)
                        if pos1 < 0: pos1 += 5
                    if pair[1] == key[row][z]:
                        pos2 = row - 1  # choose the position shifted upwards (opposite to encryption)
                        if pos2 < 0: pos2 += 5
                    if (pos1 > -1) & (pos2 > -1):
                        cCheck = True
                        listPair.append((key[pos1][z], key[pos2][z]))
                        listEncrPair.pop(0)
                        break
            if not (rCheck + cCheck) & (len(listEncrPair) > 0):
                # same process from encryption, since method applies the same in reverse
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
                if char != 'Z':
                    decryptString += char

        return decryptString

    def productDecrypt(self, text):
        """
        applies RSA decryption then transposition decryption to decrypt string
        """
        pt1 = self.rsaDecrypt(text)
        pt2 = self.transpositionDecrypt(pt1)
        return pt2

    def transpositionDecrypt(self, text):
        # SEE TRANSPOSITION ENCRYPTION FOR DOCUMENTATION, exact same process for decryption.
        newString = text.split(" ")
        decryptStringList = []
        decryptString = ""
        for word in newString:
            for i in range(len(word), 0, -1):
                decryptStringList.append(word[i - 1])
            decryptStringList.append(" ")

        for char in decryptStringList:
            decryptString += char

        return decryptString

    # Substitution Decryption
    def substitutionDecrypt(self, text):
        decrypted_msg = ""
        base_val = ord('a')

        # Reading the substitution key from the file and assigning it to a variable, substitution_mapping
        with open('substitutionKey.txt') as substitutionFile:
            substitution_mapping = json.load(substitutionFile)
        substitutionFile.close()

        # Loop to decrypt each character in the string
        for c in text:
            # If the character is between 'a' and 'z'
            if 'a' <= c <= 'z':
                x = substitution_mapping.index(ord(c) - base_val)
                y = x + base_val
                decrypted_msg += chr(y)
            # If the character is not in the range of 'a' to 'z', then leave that character alone
            else:
                decrypted_msg += c

        # Return the encrypted message
        return decrypted_msg

    # Caesar Decrypt
    def caesarDecrypt(self, text):
        # Defining the key, message as string and the base value as the Ascii of 'a'
        caesar_mapping = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        decrypted_msg = ""
        base_val = ord('a')

        # Loop to decrypt text
        for c in text:
            # If the character is between 'a' and 'z'
            if 'a' <= c <= 'z':
                x = caesar_mapping.index(ord(c) - base_val)
                y = x + base_val
                decrypted_msg += chr(y)
            # If the character is not in the range of 'a' to 'z', then leave that character alone
            else:
                decrypted_msg += c

        # Return the encrypted message
        return decrypted_msg


if __name__ == '__main__':
    a = CiphertextMSG([4700, 3061, 4493, 4493, 7622, 5915, 4178, 7622, 2202, 4493, 5869, 7533], 'RSA')
    print(a.message)
    pt = CiphertextMSG([5869, 4493, 2202, 7622, 2253, 7622, 4493, 4493, 3061, 2742, 5915], 'Product')
    print(pt.message)
