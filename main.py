# Noah Fijan, 100749828
# Noah Morin, 100740090
# Blake Whiting, 100743587
"""
March 27, 2020
Object Oriented Programming, FINAL PROJECT
This program allows the user to enter a string, the program then randomly selects from 1 of 6 encryption methods
and encrypts, then decrypts the message.
"""

from message import Message
from ciphertextMSG import CiphertextMSG
from plaintextMSG import PlaintextMSG
import random
import string

if __name__ == '__main__':
    encryptionTypes = ['RSA', 'Playfair', 'Transposition', 'Product', 'Caesar', 'Substitution']
    texts = []

    print(" | THE ENCRYPTION GAME |---------   ")
    print(" | By Noah. M, Noah. F, and Blake")
    while True:
        print('\nif you would like to stop running the program, type "stop"')
        print('the only valid characters are the lower case ascii a-z')
        text = input('enter a message you would like to encrypt >>> ')
        if text == 'stop':
            break
        try:
            for c in text:
                if not c in string.ascii_lowercase:
                    raise TypeError  # certain ciphers (playfair, caesar) only account for lowercase ascii, therefore we have to make sure all inputs match this criteria as it could raise an error
        except TypeError:
            print('Error: please ensure you only enter lowercase letters')
            continue
        encType = random.choice(encryptionTypes)  # randomly pick an encryption type
        encMessage = PlaintextMSG(text, encType)  # encrypt the message
        decMessage = CiphertextMSG(encMessage.message, encType)  # decrypt the message
        texts.append((encMessage, decMessage, encType))  # append enc message, dec message, and enc type to array

    while len(
            texts) != 0:  # loop through array and print out all the decrypted and encypted strings along with the encryption method
        m = texts.pop(0)
        print(f'message "{m[1].message}" was encrypted using {m[2]} and the encrypted message was "{m[0].message}"')
