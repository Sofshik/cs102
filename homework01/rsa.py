import random
import typing as tp


def is_prime(n: int) -> bool:
    if n == 1:
        return False
    elif n != 2:
        for i in range(2, n):
            if n % i == 0:
                return False
            else:
                continue
        return True
    else:
        return True

def gcd(a: int, b: int) -> int:
    if a == 0 and b == 0:
        return 0
    elif a == 0 and b != 0:
        return b
    elif a != 0 and b == 0:
        return a
    else:
        for i in range(1, b):
            if (a % i == 0) and (b % i == 0):
                divider = i
            else:
                continue
        return divider

def generate_keypair(p: int, q: int):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    elif p == q:
        raise ValueError("p and q cannot be equal")
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    while (is_prime(e) != True) or (e >= phi) or (gcd(e, phi) != 1):
        e = random.randrange(1, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))

def multiplicative_inverse(e: int, phi: int) -> int:
    p, s, q, r = 1, 1, 0, 0
    a = e
    b = phi
    while a != 0 and b != 0:
        if a >= b:
            a = a - b
            p = p - r
            q = q - s
        else:
            b = b - a
            r = r - p
            s = s - q
    if a != 0:
        x = p
        d = x % phi
        return d
    else:
        x = r
        d = x % phi
        return d

def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))