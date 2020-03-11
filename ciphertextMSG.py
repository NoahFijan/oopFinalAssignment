from message import Message
import random
import math
import sympy
import os

class CiphertextMSG(Message):
    def __init__(self, text, encryptionType):
        if encryptionType == 'RSA':
            if not os.path.exists('./pub.txt') or not os.path.exists('./priv.txt'):
                self.generateKeys()

            ciphertext = self.rsaEncrypt(text)
            super().__init__(ciphertext)

        if encryptionType == 'cesar':
            super().__init__(self.cesarEncrypt(text))

    def lcm(self, a, b):
        return abs(a * b) // math.gcd(a, b)

    def modInverse(self, a, m): 
        a = a % m;  
        for x in range(1, m): 
            if ((a * x) % m == 1): 
                return x 
        return 1

    def writeKeys(self, n, e, d):
        f = open('pub.txt','w')
        f.writelines([str(n)+'\n', str(e)])
        f.close()
        f = open('priv.txt','w')
        f.write(str(d))
        f.close()

    def readPubKey(self):
        f = open('pub.txt', 'r')
        n = f.readline()
        e = f.readline()
        f.close()
        f = open('priv.txt', 'r')
        d = f.readline()
        f.close()
        return int(n), int(e), int(d)

    def generateKeys(self):
        print('generating RSA keys')
        minP = 1000
        maxP = 10000
        setOfPrimes = [i for i in range(minP, maxP) if sympy.isprime(i)]
        p = random.choice(setOfPrimes)
        q = random.choice(setOfPrimes)
        while q == p:
            q = random.choice(setOfPrimes) 
        lambdaN = self.lcm(p-1,q-1)
        n = p*q 
        e = 3 
        while math.gcd(e,lambdaN)!=1:
            e +=1 
            if e>lambdaN:
                e = 3 
        d = self.modInverse(e,lambdaN)
        self.writeKeys(n, e, d)
        

    
    def rsaEncrypt(self, text):
        #do RSA encryption
        #step 2 work on ascii conversion so that messages can be encrypted, not just numbers
        #step 3 work on decryption
        n, e, d = self.readPubKey()

        m = 10000
        print(f'message = {m}')
        c = (m**e)%n
        print(f'encrypted message = {c}')

        dec = (c**d)%n

        print(f'decrypted message: {dec}')

    def cesarEncrypt(self, text):
        #do cesar cypher encryption
        pass

if __name__ == '__main__':
    ct = CiphertextMSG('m', 'RSA')
    

