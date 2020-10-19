package caesar

import "fmt"

func main() {
	EncryptCaesar("python", 3)
}

func EncryptCaesar(plaintext string, shift int) string {
	var ciphertext string
	for letter := 0; letter < len(plaintext); letter++ {
		i := plaintext[letter]
		byteShift := []byte(shift)
		if i >= 'a' && i <= 'z' || i >= 'A' && i <= 'Z' {
			i = i + byteShift
			if i > 'z' || i > 'Z' {
				i = i - 26
			}
			fmt.Printf("%i", i)
		}
	}
	return ciphertext
}

func DecryptCaesar(ciphertext string, shift int) string {
	var plaintext string

	// PUT YOUR CODE HERE

	return plaintext
}
