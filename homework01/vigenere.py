def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    rawtext = list(plaintext)
    rawkey = list(keyword.lower())
    length = len(rawkey)
    i = 0
    for letter in rawtext:
        letter = ord(letter)
        if ord('A') <= letter <= ord('Z') or letter >= ord('a') <= letter <= ord('z'):
            if ord('A') <= letter <= ord('Z'):
                if ord('Z') - (ord(rawkey[i]) - 97) < letter <= ord('Z'):
                    letter -= 26
                letter += (ord(rawkey[i]) - 97)
            elif letter >= ord('a') <= letter <= ord('z'):
                if ord('z') - (ord(rawkey[i]) - 97) < letter <= ord('z'):
                    letter -= 26
                letter += (ord(rawkey[i]) - 97)
            letter = chr(letter)
            ciphertext += letter
        else:
            letter = chr(letter)
            ciphertext += letter
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
        if ord('A') <= letter <= ord('Z') or ord('a') <= letter <= ord('z'):
            if ord('A') <= letter <= ord('Z'):
                if ord('A') <= letter < ord('A') + (ord(rawkey[i]) - 97):
                    letter += 26
                letter -= (ord(rawkey[i]) - 97)
            elif ord('a') <= letter <= ord('z'):
                if ord('a') <= letter < ord('a') + (ord(rawkey[i]) - 97):
                    letter += 26
                letter -= (ord(rawkey[i]) - 97)
            letter = chr(letter)
            plaintext += letter
        else:
            letter = chr(letter)
            plaintext += letter
        i += 1
        if i == (length):
            i = 0
    return plaintext
