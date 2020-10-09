def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    ciphertext = ""
    rawtext = list(plaintext) # Превращаем шифруемый текст в список символов
    rawkey = list(keyword.lower()) # Превращаем ключесвое слово в список символов (переводим в нижний регистр для удобста работы, т. к. одна и та же буква в разных регистрах даёт одинаковый сдвиг)
    length = len(rawkey) # Находим длину ключевого слова
    i = 0 # Это индекс по которому мы будем обращаться в цикле к каждой букве в ключевом слове
    for letter in rawtext: # Цикл, который будет идти последовательно по букве, стоящей на месте i
        letter = ord(letter) # Изменяем значение переменной с буквенного на цифровое (номер символа в юникоде) 
        if (letter >= ord('A') and letter <= ord('Z')) or (letter >= ord('a') and letter <= ord('z')): # Здесь отделяем буквы от "небукв", т. к. шифроваться должны только буквы
            if (letter >= ord('A')) and (letter <= ord('Z')): # Отделяем буквы в верхнем регистре
                if (letter > (ord('Z') - (ord(rawkey[i]) - 97))) and (letter <= ord('Z')): # (Сложно понять, но постарайся) Т. к. буква, стоящая в конце алфавита при шифровании должна перепрыгнуть в начало, здесь мы указываем промежуток индексов юникода, для которых необходимо вернуться на 26 символов (один алфавит) назад
                    letter -= 26
                letter += (ord(rawkey[i]) - 97) # Сдвиг по букве, стоящей на месте i (Вычитаем 97, т. к. именно под этим числом у нас в юникоде стоит строчная буква а, от которой идёт отсчёт)
            elif (letter >= ord('a')) and (letter <= ord('z')): # Отделяем буквы в нижнем регистре (то же самое, что и в верхнем)
                if (letter > (ord('z') - (ord(rawkey[i]) - 97))) and (letter <= ord('z')):
                    letter -= 26
                letter += (ord(rawkey[i]) - 97)
            letter = chr(letter) # Переводим числовое значение юникода обратно в буквенное
            ciphertext = ciphertext + letter # Добавляем полученную букву в шифруемое слово (как бусинки на нитку)
        else: # Этот блок просто добавляет "небуквы" к шифруемому слову, никуда не сдвигая
            letter = chr(letter)
            ciphertext = ciphertext + letter
        i += 1 # Увеличиваем i на один, соответственно следующая итерация цикла будет производиться со следующей буквой ключевого слова
        if i == (length): # Если ключ короче шифруемого слова, надо чтобы после работы с последним i значение опять переходило к первой букве ключевого слова (нулевой индекс = первая буква)
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
