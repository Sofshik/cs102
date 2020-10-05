import typing as tp


def encrypt_caesar(plaintext: str, shift: int) -> str:
    ciphertext = ""
    rawtext = list(plaintext)
    for letter in rawtext:
        letter = ord(letter)
        if (letter >= ord('A') and letter <= ord('Z')) or (letter >= ord('a') and letter <= ord('z')):
            if (letter > (ord('Z') - shift)) and (letter <= ord('Z')):
                letter -= 26
            elif (letter > (ord('z') - shift)) and (letter <= ord('z')):
                letter -= 26
            letter += shift
            letter = chr(letter)
            ciphertext = ciphertext + letter 
        else:
            letter = chr(letter)
            ciphertext = ciphertext + letter 
    return ciphertext

def decrypt_caesar(ciphertext: str, shift: int) -> str:
    plaintext = ""
    rawtext = list(ciphertext)
    for letter in rawtext:
        letter = ord(letter)
        if (letter >= ord('A') and letter <= ord('Z')) or (letter >= ord('a') and letter <= ord('z')):
            if (letter >= ord('A')) and (letter < (ord('A') + shift)):
                letter += 26 
            elif (letter >= ord('a')) and (letter < (ord('a') + shift)):
                letter += 26
            letter -= shift
            letter = chr(letter)
            plaintext = plaintext + letter
        else:
            letter = chr(letter)
            plaintext = plaintext + letter
    return plaintext

d = {"python", "java", "ruby"}
def caesar_breaker(ciphertext: str, dictionary: tp.Set[str]) -> int:
    best_shift = 0
    rawtext = list(ciphertext.lower())
    for element in dictionary:
        rawelement = list(element)
        sub1 = ord(rawtext[0]) - ord(rawelement[0])
        sub2 = ord(rawtext[1]) - ord(rawelement[1])
        if sub1 < 0:
            sub1 += 26
        if sub2 < 0:
            sub2 += 26
        if sub1 == sub2:
            best_shift = sub1
    return best_shift
