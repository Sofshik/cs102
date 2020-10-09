def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    rawtext = list(plaintext)
    rawkey = list(keyword.lower())
    length = len(rawkey)
    i = 0
    for letter in rawtext:
        letter = ord(letter)
        if (letter >= ord('A') and letter <= ord('Z')) or (letter >= ord('a') and letter <= ord('z')):
            if (letter >= ord('A')) and (letter <= ord('Z')):
                if (letter > (ord('Z') - (ord(rawkey[i]) - 97))) and (letter <= ord('Z')):
                    letter -= 26
                letter += (ord(rawkey[i]) - 97)
            elif (letter >= ord('a')) and (letter <= ord('z')):
                if (letter > (ord('z') - (ord(rawkey[i]) - 97))) and (letter <= ord('z')):
                    letter -= 26
                letter += (ord(rawkey[i]) - 97)
            letter = chr(letter)
            ciphertext = ciphertext + letter
        else:
            letter = chr(letter)
            ciphertext = ciphertext + letter
        i += 1
        if i == (length):
            i = 0
    return ciphertext

def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    plaintext = ""
    rawtext = list(ciphertext)
    rawkey = list(keyword.lower())
    length = len(rawkey)
    i = 0
    for letter in rawtext:
        letter = ord(letter)
        if (letter >= ord('A') and letter <= ord('Z')) or (letter >= ord('a') and letter <= ord('z')):
            if (letter >= ord('A')) and (letter <= ord('Z')):
                if (letter >= ord('A')) and (letter < (ord('A') + (ord(rawkey[i]) - 97))):
                    letter += 26
                letter -= (ord(rawkey[i]) - 97)
            elif (letter >= ord('a')) and (letter <= ord('z')):
                if (letter >= ord('a')) and (letter < (ord('a') + (ord(rawkey[i]) - 97))):
                    letter += 26
                letter -= (ord(rawkey[i]) - 97)
            letter = chr(letter)
            plaintext = plaintext + letter
        else:
            letter = chr(letter)
            plaintext = plaintext + letter
        i += 1
        if i == (length):
            i = 0
    return plaintext
