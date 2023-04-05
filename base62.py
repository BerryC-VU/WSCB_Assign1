# base62 encoder/decoder

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num, alphabet=ALPHABET):
    if (num == 0):
        return '0'
    arr = []
    while num:
        rem = num % 62
        arr.append(alphabet[rem])
        num = num // 62
    arr.reverse()
    return ''.join(arr)

def base62_decode(string, alphabet=ALPHABET):
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (62 ** power)
        idx += 1

    return num
