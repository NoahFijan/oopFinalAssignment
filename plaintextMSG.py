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
        '''
        returns the lowest common multiple of 2 numbers
        '''
        return abs(a * b) // math.gcd(a, b)

    def modInverse(self, a, m):
        '''
        returns the modular multiplicitive inverse of e and lambdaN
        '''
        a = a % m;
        for x in range(1, m):
            if ((a * x) % m == 1):
                return x
        return 1

    def isPrime(self, num):
        '''
        Checks if a number is prime
        '''
        for i in range(2,int(num/2)):
            if num % i == 0:
                return False
        return True

    def writeKeys(self, n, e, d):
        '''
        writes the generated rsa keys to a file so that we do not generate new keys 
        everytime we run the program
        '''
        f = open('pub.txt','w')
        f.writelines([str(n)+'\n', str(e)])
        f.close()
        f = open('priv.txt','w')
        f.writelines([str(n)+'\n', str(d)])
        f.close()

    def readPubKey(self):
        '''
        reads the public key so that we can encrypt the message 
        '''
        f = open('pub.txt', 'r')
        n = f.readline()
        e = f.readline()
        f.close()
        return int(n), int(e)

    def generateKeys(self):
        '''
        Generates the RSA keys to be used for encryption
        '''
        print('generating RSA keys')
        minP = 30 #minimum number for prime generation
        maxP = 100 #maximum number for prime generation
        setOfPrimes = [i for i in range(minP, maxP) if self.isPrime(i)] #generate all primes in range minP, maxP

        p = random.choice(setOfPrimes) #choose random prime from generated list
        q = random.choice(setOfPrimes)

        while q == p: #ensure both primes are different numbers
            q = random.choice(setOfPrimes)
        lambdaN = self.lcm(p-1,q-1) #Carmichael's totient function
        n = p*q
        e = 3
        while math.gcd(e,lambdaN)!=1: #part of public key generarion
            e +=1
        d = self.modInverse(e,lambdaN) #modular multiplicitive inverse
        self.writeKeys(n, e, d) #save keys to file



    def rsaEncrypt(self, text):
        '''
        encrypts the plaintext message 
        '''
        n, e = self.readPubKey() #get public key

        c = [(ord(char) ** e) % n for char in text] #for each char in message encrypt it

        return c

    def playfairEncrypt(self, text):
        text = text.replace(" ", "")
        text = text.upper()
        listPair = []
        c = 0
        while c < len(text):
            if c + 1 < len(text):
                if text[c] == text[c + 1]:
                    listPair.append((text[c], 'X'))
                    c += 1
                    continue
                listPair.append((text[c], text[c + 1]))
                c += 2
                continue
            listPair.append((text[c], 'X'))
            c += 1

        key = [["P", "L", "A", "Y", "F"],
               ["I", "R", "E", "J", "M"],
               ["B", "C", "D", "G", "H"],
               ["K", "N", "O", "Q", "S"],
               ["T", "U", "V", "W", "Z"]]
        listEncrPair = []
        while (len(listPair)) > 0:
            rCheck = False
            cCheck = False
            pair = listPair[0]
            pos1 = -1
            pos2 = -1
            for row in range(len(key)):
                if (pair[0] in key[row]) & (pair[1] in key[row]):  # FOR SURE R0W CHECK
                    rCheck = True
                    for item in key[row]:
                        if pair[0] == item:
                            pos1 = key[row].index(item) + 1
                            if pos1 > 4: pos1 -= 5
                        if pair[1] == item:
                            pos2 = key[row].index(item) + 1
                            if pos2 > 4: pos2 -= 5
                    listEncrPair.append((key[row][pos1], key[row][pos2]))
                    listPair.pop(0)
            for z in range(len(key)):
                pos1 = -1
                pos2 = -1
                for row in range(len(key)):
                    if pair[0] == key[row][z]:
                        pos1 = row + 1
                        if pos1 > 4: pos1 -= 5
                    if pair[1] == key[row][z]:
                        pos2 = row + 1
                        if pos2 > 4: pos2 -= 5
                    if (pos1 > -1) & (pos2 > -1):
                        cCheck = True
                        listEncrPair.append((key[pos1][z], key[pos2][z]))
                        listPair.pop(0)
                        break
            if not (rCheck + cCheck) & (len(listPair) > 0):
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
                listEncrPair.append((key[y1][x2], key[y2][x1]))
                listPair.pop(0)

        encryptedString = ""
        for tpl in listEncrPair:
            for char in tpl:
                if char != 'X':
                    encryptedString += char

        return encryptedString

    def transpositionCipher(self, text):
        newString = text.split(" ")
        encryptStringList = []
        encryptString = ""
        for word in newString:
            for i in range(len(word), 0, -1):
                encryptStringList.append(word[i - 1])
            encryptStringList.append(" ")

        for char in encryptStringList:
            encryptString += char
        return encryptString


if __name__ == '__main__':
    ct = PlaintextMSG('Hello World!', 'RSA')
    print(ct.message)


       
