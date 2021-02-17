# Функция перевода в биты
def decode_to_binary(plaintext: str) -> str:
    binary_text = ''
    byte_len = 8
    for letter in plaintext:
        binary_temp = bin(ord(letter))[2:]
        if len(binary_temp) < byte_len:
            count_of_nulls = byte_len - len(binary_temp)
            binletter = count_of_nulls * '0' + binary_temp
            binary_text += binletter
        else:
            binary_text += binary_temp
    return binary_text


# Деление по 32 бита
def divide_bin(binary_text: str) -> tuple:
    left_part = binary_text[0:32]
    right_part = binary_text[32:]
    return (left_part, right_part)

# Xor левой и правой части открытого текста
def xor_dif_parts(left_part: str, right_part: str) -> str:
    xor_result = ''
    for left_bit, right_bit in zip(left_part, right_part):
        xor_result += str(int(left_bit) ^ int(right_bit))
    return xor_result
a = 'hellohel'
bina = decode_to_binary(a)
temp = divide_bin(bina)
print(temp)
print(len(temp[0]))
print(len(temp[1]))
y = xor_dif_parts(temp[0], temp[1])
print(y)
print(len(y))
