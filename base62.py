# base62 encoder/decoder
# reference: https://stackoverflow.com/questions/742013/how-do-i-create-a-url-shortener

# character set:  0-9 + uppercase letters + lowercase letters
ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

'''
Base62 converter takes num(interger) as paramter, 
and the mapping is 0 -> 0 ... 10 -> A ... 36 -> a ... 61 -> z

if num is 0:
    return the string 0
else create a list: 
    while num is greater than 0:
        append the remainder of (num % 62) to the list
        divide num by 62 
    since the converter works in reverse order, 
    the list is reversed to get the right order
    then, use '' (empty) string to join the elements in the list to get the string
    
For example: if num = 38562, 
                38562 % 62 = 60 -> ['y'] -> num = 621
                621 % 62 = 1 -> ['y','1'] -> num = 10
                10 % 62 = 10 -> ['y','1','A'] -> num = 0
             ['y','1','A'] -> reverse=['A','y','1'] -> join the elements -> 'A1y'
             => thus 'A1y' is the base62 string for input num 38562
'''
def base62_encoder(num, alphabet=ALPHABET):
    """  
    Args:
        num (int): Base10 integer 
        alphabet (str): character set

    Returns:
        str: Base62 string
    """
    if (num == 0):
        return '0'
    arr = []
    while num:
        remainder = num % 62
        arr.append(alphabet[remainder])
        num = num // 62
    arr.reverse()
    return ''.join(arr)