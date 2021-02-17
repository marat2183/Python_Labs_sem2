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

def get_round_keys(key: str) -> list:
    count = 0
    round_keys = []
    for i in range(len(key)):
        if (count + 4) <= len(key):
            round_keys.append(key[count: count + 4])
            count += 4
        else:
            break
    for i in range(len(round_keys)):
        round_keys[i] = decode_to_binary(round_keys[i])
    return round_keys

def get_s_blocks_inputs(bin_data: str) -> list:
    count = 0
    S_block_inputs = []
    for i in range(len(bin_data)):
        if (count + 4) <= len(bin_data):
            S_block_inputs.append(bin_data[count: count + 4])
            count += 4
        else:
            break

    return S_block_inputs

def mod_32(text_block:str, round_key: str) -> str:
    first_number = int(text_block, 2)
    second_number = int(round_key, 2)
    sum = first_number + second_number
    if sum < 2 ** 32:
        result = bin(sum)[2:].zfill(32)
        return result
    else:
        temp = sum - 2 ** 32
        result = bin(temp)[2:].zfill(32)
        return result


def cyclic_shift_to_left(data: str, number: int) -> str:
    result = data[number:] + data[0:number]
    return result


def f_function(text_block: str, round_key: str) -> str:
    S_blocks = [
        [12,4,6,2,10,5,11,9,14,8,13,7,0,3,15,1],
        [6,8,2,3,9,10,5,12,1,14,4,7,11,13,0,15],
        [11,3,5,8,2,15,10,13,14,1,7,4,12,9,6,0],
        [12,8,2,1,13,4,15,6,7,0,10,5,3,14,9,11],
        [7,15,5,10,8,1,6,13,0,9,3,14,11,4,2,12],
        [5,13,15,6,9,2,12,10,11,7,8,1,4,3,14,0],
        [8,14,2,5,6,9,1,12,15,4,11,0,13,10,3,7],
        [1,7,14,13,0,5,8,3,4,15,10,6,9,12,11,2]
    ]
    mod_32_result = mod_32(text_block, round_key)
    S_blocks_inputs = get_s_blocks_inputs(mod_32_result)

    result = ''
    for i in range(len(S_blocks_inputs)):
        col = int(S_blocks_inputs[i], 2)
        row = i
        temp = bin(S_blocks[row][col])[2:].zfill(4)
        result += temp
    result = cyclic_shift_to_left(result, 11)
    return result

def decode_bin_to_ascii(text: str) -> str:
    count = 0
    bytes = []
    result = ''
    for i in range(len(text)):
        if (count + 8) <= len(text):
            bytes.append(text[count: count + 8])
            count += 8
        else:
            break
    for byte in bytes:
        letter = chr(int(byte, 2))
        result += letter
    return result


def encode(plaintext_block:str, key:str) -> str:
    ciphertext = ''
    n = 32
    binary_data = decode_to_binary(plaintext_block)
    left_part, right_part = divide_bin(binary_data)
    round_keys = get_round_keys(key)
    index_to_reverse = 7
    for i in range(n):
        if i == 31:
            f_function_result = f_function(right_part, round_keys[index_to_reverse])
            xor_result = xor_dif_parts(left_part, f_function_result)
            ciphertext = xor_result + right_part
        elif i <= 23:
            f_function_result = f_function(right_part, round_keys[i % 8])
            xor_result = xor_dif_parts(left_part, f_function_result)
            left_part, right_part = right_part, xor_result
        else:
            f_function_result = f_function(right_part, round_keys[index_to_reverse])
            xor_result = xor_dif_parts(left_part, f_function_result)
            left_part, right_part = right_part, xor_result
            index_to_reverse -= 1

    return ciphertext

def decode(ciphertext:str, key:str) -> str:
    plaintext = ''
    n = 32
    binary_data = ciphertext
    left_part, right_part = divide_bin(binary_data)
    round_keys = get_round_keys(key)
    index_to_reverse = 7
    for i in range(n):
        if i == 31:
            f_function_result = f_function(right_part, round_keys[index_to_reverse])
            xor_result = xor_dif_parts(left_part, f_function_result)
            plaintext = xor_result + right_part
        elif i > 7:
            f_function_result = f_function(right_part, round_keys[i % 8])
            xor_result = xor_dif_parts(left_part, f_function_result)
            left_part, right_part = right_part, xor_result
        else:
            f_function_result = f_function(right_part, round_keys[index_to_reverse])
            xor_result = xor_dif_parts(left_part, f_function_result)
            left_part, right_part = right_part, xor_result
            index_to_reverse -= 1

    return decode_bin_to_ascii(plaintext)

first = encode('hihihihi', 'armaarmaarmaarmaarmaarmaarmaarma')
print(decode(first, 'armaarmaarmaarmaarmaarmaarmaarma'))

