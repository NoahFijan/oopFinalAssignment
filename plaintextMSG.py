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


if __name__ == '__main__':
    ct = PlaintextMSG('Hello World!', 'RSA')
    print(ct.message)


       
