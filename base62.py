# base62 encoder/decoder
# reference: https://stackoverflow.com/questions/742013/how-do-i-create-a-url-shortener

ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def base62_encoder(num, alphabet=ALPHABET):
    if (num == 0):
        return '0'
    arr = []
    while num:
        remainder = num % 62
        arr.append(alphabet[remainder])
        num = num // 62
    arr.reverse()
    return ''.join(arr)