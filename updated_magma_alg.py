import json
import random
import string
from typing import Union
from binascii import hexlify, unhexlify


# Функция перевода в биты
def get_textblocks(text: str, size: int) -> list:
    count = 0
    text_blocks = []
    for i in range(len(text)):
        if (count + size) <= len(text):
            text_blocks.append(text[count: count + size])
            count += size
        else:
            break
    return text_blocks


def text_decode_to_binary(text: Union[str, bytes], block_len: int, text_type: str) -> str:
    if type(text) is bytes:
        hex_str = hexlify(text).decode()
        int_str = int(hex_str, 16)
    elif type(text) is int:
        int_str = text
    else:
        try:
            int_str = int(text, 16)
        except:
            hex_str = hexlify(text.encode()).decode()
            int_str = int(hex_str, 16)
    bin_str = bin(int_str)[2:]
    if text_type == 'key' and len(bin_str) > 256:
        raise Exception("Длина ключа > 256 бит")
    length = len(bin_str)
    if (length % block_len) != 0:
        need_to_add = block_len - (length % block_len)
        bin_str = bin_str.zfill(length + need_to_add)
    return bin_str


# Xor левой и правой части открытого текста
def xor_dif_parts(left_part: str, right_part: str) -> str:
    xor_result = ''
    for left_bit, right_bit in zip(left_part, right_part):
        xor_result += str(int(left_bit) ^ int(right_bit))
    return xor_result


def get_round_keys(key: str) -> list:
    key = text_decode_to_binary(key, 256, 'key')
    round_keys = get_textblocks(key, 32)
    return round_keys


def get_s_blocks_inputs(bin_data: str) -> list:
    S_block_inputs = get_textblocks(bin_data, 4)
    return S_block_inputs


def mod_32(text_block: str, round_key: str) -> str:
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


def Feistel_scheme(text_block: str, round_keys: list, round_keys_queue: list, rounds_number: int):
    text_part = ''
    left_part, right_part = get_textblocks(text_block, 32)
    for i in range(rounds_number):
        if i == 31:
            f_function_result = f_function(right_part, round_keys[round_keys_queue[i]])
            xor_result = xor_dif_parts(left_part, f_function_result)
            text_part = xor_result + right_part
        else:
            f_function_result = f_function(right_part, round_keys[round_keys_queue[i]])
            xor_result = xor_dif_parts(left_part, f_function_result)
            left_part, right_part = right_part, xor_result
    return text_part


def decode_from_bin_to_ascii(bin_str: str) -> Union[str, bytes]:
    int_str = int(bin_str, 2)
    hex_str = hex(int_str)[2:]
    try:
        ascii_str = unhexlify(hex_str).decode()
    except:
        ascii_str = hex_str
    return ascii_str

def decode_from_bin_to_hex(bin_str: str) -> Union[str, bytes]:
    int_str = int(bin_str, 2)
    hex_str = hex(int_str)[2:]
    return hex_str


def encode(plaintext: str, key: Union[str, int]) -> str:
    ciphertext = ''
    n = 32
    bin_plaintext = text_decode_to_binary(plaintext, 64, 'plaintext')
    plaintext_blocks = get_textblocks(bin_plaintext, 64)
    for plaintext_block in plaintext_blocks:
        round_keys = get_round_keys(key)
        round_keys_queue = [0, 1, 2, 3, 4, 5, 6, 7] * 3 + [7, 6, 5, 4, 3, 2, 1, 0]
        ciphertext_part = Feistel_scheme(plaintext_block, round_keys, round_keys_queue, n)
        ciphertext += ciphertext_part
    return ciphertext


def decode(ciphertext: Union[str,bytes], key: Union[str, int]) -> str:
    plaintext = ''
    n = 32
    if type(ciphertext) is not str:
        ciphertext = text_decode_to_binary(ciphertext, 64, 'ciphertext')
    else:
        try:
            int(ciphertext, 2)
        except ValueError:
            ciphertext = text_decode_to_binary(ciphertext, 64, 'ciphertext')
    ciphertext_blocks = get_textblocks(ciphertext, 64)
    for ciphertext_block in ciphertext_blocks:
        round_keys_queue = [0, 1, 2, 3, 4, 5, 6, 7] * 3 + [7, 6, 5, 4, 3, 2, 1, 0]
        round_keys_queue.reverse()
        round_keys = get_round_keys(key)
        plaintext_part = Feistel_scheme(ciphertext_block, round_keys, round_keys_queue, n)
        plaintext += plaintext_part
    return decode_from_bin_to_ascii(plaintext)


def tests(N: int, text_len: int) -> bool:
    success = False
    key_len = 16
    count = 0
    for i in range(N):
        plaintext = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(text_len))
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_len))
        first = encode(plaintext, key)
        decode_res = decode(decode_from_bin_to_hex(first), key)
        if decode_res == plaintext:
            count += 1
    if count == N:
        success = True
    return success




# mode = input('''
# Режим работы:
# 1) Зашифровать
# 2) Расшифровать
# Ответ:
# ''')
# if mode == '1':
#     pt = input('pt: ')
#     key = int(input('key: '))
#     try:
#         result = encode(pt, key)
#         print('ciphertext:', decode_from_bin_to_hex(result))
#         print(decode(result, key))
#     except Exception as e:
#        print(str(e))
# elif mode == '2':
#     ct = input('ct: ')
#     key = int(input('key: '))
#     try:
#         result = decode(ct, key)
#         print(decode_from_bin_to_ascii(result))
#     except Exception as e:
#         print(str(e))
a = encode('Привкйцуйу', 123)
if (tests(100, 129)):
    print('ok')