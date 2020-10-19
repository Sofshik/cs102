import typing as tp


def encrypt_caesar(plaintext: str, shift: int) -> str:
    ciphertext = ""
    rawtext = list(plaintext)
    for letter in rawtext:
        letter = ord(letter)
        if ord('A') <= letter <= ord('Z') or ord('a') <= letter <= ord('z'):
            if ord('Z') - shift < letter <= ord('Z'):
                letter -= 26
            elif ord('z') - shift < letter <= ord('z'):
                letter -= 26
            letter += shift
            letter = chr(letter)
            ciphertext += letter 
        else:
            letter = chr(letter)
            ciphertext += letter 
    return ciphertext
    
def decrypt_caesar(ciphertext: str, shift: int) -> str:
    plaintext = ""
    rawtext = list(ciphertext)
    for letter in rawtext:
        letter = ord(letter)
        if ord('A') <= letter <= ord('Z') or ord('a') <= letter <= ord('z'):
            if ord('A') <= letter < ord('A') + shift:
                letter += 26 
            elif ord('a') <= letter < ord('a') + shift:
                letter += 26
            letter -= shift
            letter = chr(letter)
            plaintext += letter
        else:
            letter = chr(letter)
            plaintext += letter
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
