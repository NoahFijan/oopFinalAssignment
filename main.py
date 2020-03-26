from message import Message
from ciphertextMSG import CiphertextMSG
from plaintextMSG import PlaintextMSG
import random

if __name__ == '__main__':
    encryptionTypes = ['RSA', 'Playfair', 'Transposition', 'Product', 'Caesar', 'Substitution']
    texts = []

    print(" | THE ENCRYPTION GAME |---------   ")
    print(" | By Noah. M, Noah. F, and Blake")
    while True:
        print('\nif you would like to stop running the program, type "stop"')
        text = input('enter a message you would like to encrypt >>> ')
        if text == 'stop':
            break
        encType = random.choice(encryptionTypes)
        encMessage = PlaintextMSG(text, encType)
        decMessage = CiphertextMSG(encMessage.message, encType)
        texts.append((encMessage, decMessage, encType))
    
    while len(texts) != 0:
        m = texts.pop(0)
<<<<<<< HEAD
        print(f'message "{m[1].message}" was encrypted using {m[2]} and the encrypted message was "{m[0].message}"')
=======
        print(f'Message "{m[1].message}" was encrypted using the {m[2]} Cipher and the encrypted message was "{m[0].message}"')
>>>>>>> 4b27444dbfe1584138f575f534848060d45ec22e



