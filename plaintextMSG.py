from message import Message
import random
import math
import os


class PlaintextMSG(Message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            if not os.path.exists('./pub.txt') or not os.path.exists('./priv.txt'):
                self.generateKeys()

            ciphertext = self.rsaEncrypt(text)
            super().__init__(ciphertext)

    def lcm(self, a, b):
        """
        returns the lowest common multiple of 2 numbers
        """
        return abs(a * b) // math.gcd(a, b)

    def modInverse(self, a, m):
        """
        returns the modular multiplicitive inverse of e and lambdaN
        """
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return 1

    def isPrime(self, num):
        """
        Checks if a number is prime
        """
        for i in range(2, int(num / 2)):
            if num % i == 0:
                return False
        return True

    def writeKeys(self, n, e, d):
        """
        writes the generated rsa keys to a file so that we do not generate new keys
        everytime we run the program
        """
        f = open('pub.txt', 'w')
        f.writelines([str(n) + '\n', str(e)])
        f.close()
        f = open('priv.txt', 'w')
        f.writelines([str(n) + '\n', str(d)])
        f.close()

    def readPubKey(self):
        """
        reads the public key so that we can encrypt the message
        """
        f = open('pub.txt', 'r')
        n = f.readline()
        e = f.readline()
        f.close()
        return int(n), int(e)

    def generateKeys(self):
        """
        Generates the RSA keys to be used for encryption
        """
        print('generating RSA keys')
        minP = 30  # minimum number for prime generation
        maxP = 100  # maximum number for prime generation
        setOfPrimes = [i for i in range(minP, maxP) if self.isPrime(i)]  # generate all primes in range minP, maxP

        p = random.choice(setOfPrimes)  # choose random prime from generated list
        q = random.choice(setOfPrimes)

        while q == p:  # ensure both primes are different numbers
            q = random.choice(setOfPrimes)
        lambdaN = self.lcm(p - 1, q - 1)  # Carmichael's totient function
        n = p * q
        e = 3
        while math.gcd(e, lambdaN) != 1:  # part of public key generarion
            e += 1
        d = self.modInverse(e, lambdaN)  # modular multiplicitive inverse
        self.writeKeys(n, e, d)  # save keys to file

    def rsaEncrypt(self, text):
        """
        encrypts the plaintext message
        """
        n, e = self.readPubKey()  # get public key

        c = [(ord(char) ** e) % n for char in text]  # for each char in message encrypt it

        return c

    def playfairEncrypt(self, text):
        """
        encrypts the plaintext message using the playfair cipher method
        """
        text = text.replace(" ", "")
        text = text.upper()
        # remove the spaces from the provided text, convert the remaining string to uppercase
        listPair = []
        c = 0
        # create an empty list, init a counter variable

        # WHILE LOOP to split the string into a list of character pairs following the syntax of the playfair encryption
        while c < len(text):  # while the counter variable is less then the length of the string
            if c + 1 < len(text):  # if the counter variable + 1 is less than the length of the string
                if text[c] == text[c + 1]:
                    listPair.append((text[c], 'X'))
                    c += 1
                    continue
                # if the character being looked at is equal to the next character, append the character and an x,
                # add 1 to the counter, continue the code
                listPair.append((text[c], text[c + 1]))
                c += 2
                continue
                # add the character being looked at and then next character to the list, add 2 to the counter variable
            listPair.append((text[c], 'X'))
            c += 1
            # add the character being looked at and an x to the list if the last pair is 1 character

        key = [["P", "L", "A", "Y", "F"],
               ["I", "R", "E", "J", "M"],
               ["B", "C", "D", "G", "H"],
               ["K", "N", "O", "Q", "S"],
               ["T", "U", "V", "W", "Z"]]
        # initilize key used to decrypt
        listEncrPair = []

        # WHILE LOOP used to conver the list of character pairs into encrypted character pairs
        while (len(listPair)) > 0:  # while the length of the list of character pairs is greater than 0
            rCheck = False
            cCheck = False
            #  encryption types checkers
            pair = listPair[0]  # pair is equal to a tuple of the
            pos1 = -1
            pos2 = -1
            # FOR LOOP that cycles through the rows in the key
            for row in range(len(key)):
                if (pair[0] in key[row]) & (pair[1] in key[row]):  # if the characters in the pair are in the same row
                    rCheck = True  # row check is equal to true
                    for item in key[row]:  # FOR LOOP through items in the rows of the key
                        if pair[0] == item:
                            pos1 = key[row].index(item) + 1
                            if pos1 > 4: pos1 -= 5
                        # if the first character in the pair is equal to the item, note it's position + 1,
                        # if the item is at the end of the row, make it the first item in the row
                        if pair[1] == item:
                            pos2 = key[row].index(item) + 1
                            if pos2 > 4: pos2 -= 5
                        # if the second character in the pair is equal to the item, note it's position + 1,
                        # if the item is at the end of the row, make it the first item in the row
                    listEncrPair.append((key[row][pos1], key[row][pos2]))
                    listPair.pop(0)
                    # add the value of the positions found in the previous step to the encrypted list, pop the pair from the list.
                    # ROW METHOD works by shifting the position 1 over from the item, e.g P,A encrypted is L,Y
            # FOR LOOP that cycles through the column in the key
            for col in range(len(key)):
                pos1 = -1
                pos2 = -1
                for row in range(len(key)):  # FOR LOOP cycles through the rows in the key
                    if pair[0] == key[row][col]:
                        pos1 = row + 1
                        if pos1 > 4: pos1 -= 5
                    # if the first char in the pair is equal to the column element in the current row,
                    # if the position is at the bottom of the column, make it the top of the column
                    if pair[1] == key[row][col]:
                        pos2 = row + 1
                        if pos2 > 4: pos2 -= 5
                    # if the second char in the pair is equal to the same column element in the current row,
                    # if the position is at the bottom of the column, make it the top of the column
                    if (pos1 > -1) & (pos2 > -1):
                        cCheck = True
                        listEncrPair.append((key[pos1][col], key[pos2][col]))
                        listPair.pop(0)
                        break
                    # if both positions have been updated (not -1), set column check to true, append the encrypted
                    # characters to the encrypted list, pop the pair from the list
                    # COLUMN METHOD works by shifting the column elements down by 1. e.g P,B encrypted is I,K
            # IF row check and collumn check are false, and the length of the list is greater than 0
            if not (rCheck + cCheck) & (len(listPair) > 0):
                x1, y1 = -1, -1
                x2, y2 = -1, -1
                # initialize x,y coords 1,2 to -1
                # FOR LOOP to cycle through the columns in the key
                for y in range(len(key)):
                    for x in range(len(key[y])):  # FOR LOOP to cycle through the rows in the key
                        if pair[0] == key[y][x]:
                            x1 = x
                            y1 = y
                        # if the first char in the pair is equal to the element being looked at, note it's x,y
                        if pair[1] == key[y][x]:
                            x2 = x
                            y2 = y
                        # if the second char in the pair is equal to the element being looked at, note it's x,y
                listEncrPair.append((key[y1][x2], key[y2][x1]))
                listPair.pop(0)
                #  append the encrypted characters to the encrypted list, pop the pair from the list
                # RECTANGLE METHOD works by creating a rectangle with each char making up a corner, the encrypted
                # characters are the opposing corners, e.g R,Q encrypted is J,N
        encryptedString = ""
        for tpl in listEncrPair:
            for char in tpl:
                if char != 'X':
                    encryptedString += char
        # cycle through each char in the list of pairs, if the character is not "X" append the character to the string

        return encryptedString
        # return the string

    def transpositionEncrypt(self, text):
        newString = text.split(" ")  # split the sentence into a list of words
        encryptStringList = []
        encryptString = ""
        # FOR LOOP that cycles through each word in the newString list
        for word in newString:
            for i in range(len(word), 0, -1):  # FOR LOOP that cycles through the length of the word in reverse
                encryptStringList.append(word[i - 1])  # encrypt the character to the encrypted string list
            encryptStringList.append(" ")  # append a space to the list

        for char in encryptStringList:
            encryptString += char
        # FOR LOOP cycles through each char in the encrypted string list, appending it to the encrypted string
        return encryptString
    
    
    def substitutionEncrypt(text):
        substitution_mapping = list(range(26))
        random.shuffle(substitution_mapping)
        encrypted_msg = ""
        base_val = ord('a')

        for c in text:
            if (c >= 'a' and c <= 'z'):
                encrypted_msg += chr(substitution_mapping[ord(c) - base_val] + base_val)
            else:
                encrypted_msg += c

        return encrypted_msg, substitution_mapping
    
    
    def caesarEncrypt(self, text):
        caesar_mapping = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        encrypted_msg = ""
        base_val = ord('a')

        for c in text:
            if (c >= 'a' and c <= 'z'):
                encrypted_msg += chr(caesar_mapping[ord(c) - base_val] + base_val)
            else:
                encrypted_msg += c

        return encrypted_msg, caesar_mapping


if __name__ == '__main__':
    ct = PlaintextMSG('Hello World!', 'RSA')
    print(ct.message)
