def transpositionCipher(text):
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


def transpositionDecrypt(text):
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


def main():
    encryptstring = printtranspositionCipher("This is a simple sentance")
    print(transpositionDecrypt(encryptstring))


main()
