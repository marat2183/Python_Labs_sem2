import json

# Функция перевода в биты
def get_textblocks(text:str, size: int) -> list:
    count = 0
    text_blocks = []
    for i in range(len(text)):
        if (count + size) <= len(text):
            text_blocks.append(text[count: count + size])
            count += size
        else:
            break
    return text_blocks

def decode_to_binary(plaintext: str) -> str:
    with open('test.json', encoding='utf-8') as f:
        data = json.load(f)
    binary_text = ''
    for letter in plaintext:
        binary_temp = bin(data[letter])[2:].zfill(8)
        # binary_temp = bin(rus_alphabet[letter])[2:]
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
    key = decode_to_binary(key)
    count = 0
    round_keys = []
    for i in range(len(key)):
        if (count + 32) <= len(key):
            round_keys.append(key[count: count + 32])
            count += 32
        else:
            break
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
    with open('S_blocks_matrix.json') as f:
        data = json.load(f)
    S_blocks = data['matrix']
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


def encode(plaintext:str, key:str) -> str:
    ciphertext = ''
    n = 32
    bin_plaintext = decode_to_binary(plaintext)
    plaintext_blocks = get_textblocks(bin_plaintext, 64)
    for plaintext_block in plaintext_blocks:
        ciphertext_part = ''
        binary_data = plaintext_block
        left_part, right_part = divide_bin(binary_data)
        round_keys = get_round_keys(key)
        index_to_reverse = 7
        for i in range(n):
            if i == 31:
                f_function_result = f_function(right_part, round_keys[index_to_reverse])
                xor_result = xor_dif_parts(left_part, f_function_result)
                ciphertext_part = xor_result + right_part
            elif i <= 23:
                f_function_result = f_function(right_part, round_keys[i % 8])
                xor_result = xor_dif_parts(left_part, f_function_result)
                left_part, right_part = right_part, xor_result
            else:
                f_function_result = f_function(right_part, round_keys[index_to_reverse])
                xor_result = xor_dif_parts(left_part, f_function_result)
                left_part, right_part = right_part, xor_result
                index_to_reverse -= 1
        ciphertext += ciphertext_part
    return ciphertext

def decode(ciphertext:str, key:str) -> str:
    plaintext = ''
    n = 32
    ciphertext_blocks = get_textblocks(ciphertext, 64)
    for ciphertext_block in ciphertext_blocks:
        binary_data = ciphertext_block
        left_part, right_part = divide_bin(binary_data)
        round_keys = get_round_keys(key)
        index_to_reverse = 7
        plaintext_part = ''
        for i in range(n):
            if i == 31:
                f_function_result = f_function(right_part, round_keys[index_to_reverse])
                xor_result = xor_dif_parts(left_part, f_function_result)
                plaintext_part = xor_result + right_part
            elif i > 7:
                f_function_result = f_function(right_part, round_keys[i % 8])
                xor_result = xor_dif_parts(left_part, f_function_result)
                left_part, right_part = right_part, xor_result
            else:
                f_function_result = f_function(right_part, round_keys[index_to_reverse])
                xor_result = xor_dif_parts(left_part, f_function_result)
                left_part, right_part = right_part, xor_result
                index_to_reverse -= 1
        plaintext += plaintext_part
        print(plaintext)
    return plaintext


plaintext = 'hihihihi.hihihih'
key = '12341234123412341234123412341234'
print(decode_to_binary(plaintext))
first = encode(plaintext, key)
decode_res = decode(first, key)
print(decode_res)
if decode_res == decode_to_binary(plaintext):
    print('ok')
else:
    print('fail')


