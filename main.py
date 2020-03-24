from message import Message
from ciphertextMSG import CiphertextMSG
from plaintextMSG import PlaintextMSG
import random

if __name__ == '__main__':
    encryptionTypes = ['RSA', 'Playfair', 'Transposition', 'Product', 'Caesar', 'Substitution']
    texts = []
    
    while True:
        print('if you would like to stop running the program, type "stop"')
        text = input('enter a message you would like to encrypt: ')
        if text == 'stop':
            break
        encType = random.choice(encryptionTypes)
        encMessage = PlaintextMSG(text, encType)
        decMessage = CiphertextMSG(encMessage.message, encType)
        texts.append((encMessage, decMessage, encType))
    
    while len(texts) != 0:
        m = texts.pop(0)
        print(f'message {m[1].message} was encrypted using {m[2]} and the encrypted message was {m[0].message}')



