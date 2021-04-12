import json
import random
import string
from binascii import hexlify, unhexlify
from typing import Union
import time
from termcolor import colored
import os


dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + '\\S_blocks_matrix.json') as f:
    data = json.load(f)
s_blocks = data['matrix']


def get_text_blocks(text: str, size: int) -> list:
    count = 0
    text_blocks = []
    for i in range(len(text)):
        if (count + size) <= len(text):
            text_blocks.append(text[count: count + size])
            count += size
        else:
            break
    return text_blocks


def padding(bin_text: str, text_type: str, text_block_len: int):
    length = len(bin_text)
    if text_type == 'key' and length > 256:
        raise ValueError("Длина ключа > 256 бит")
    if (length % text_block_len) != 0:
        need_to_add = text_block_len - (length % text_block_len)
        bin_text = bin_text.zfill(length + need_to_add)
    return bin_text


def text_decode_to_binary(text: Union[str, int], operation: str) -> str:
    if operation == 'decode':
        int_str = int(text, 16)
        bin_str = bin(int_str)[2:]
    elif operation == 'key':
        if type(text) is int:
            bin_str = bin(text)[2:]
        else:
            hex_str = hexlify(text.encode()).decode()
            int_str = int(hex_str, 16)
            bin_str = bin(int_str)[2:]
    else:
        hex_str = hexlify(text.encode()).decode()
        int_str = int(hex_str, 16)
        bin_str = bin(int_str)[2:]
    return bin_str


def xor(left_part: str, right_part: str) -> str:
    xor_result = ''
    for left_bit, right_bit in zip(left_part, right_part):
        xor_result += str(int(left_bit) ^ int(right_bit))
    return xor_result


def get_round_keys(key: str) -> list:
    key = text_decode_to_binary(key, 'key')
    key = padding(key, 'key', 256)
    round_keys = get_text_blocks(key, 32)
    return round_keys * 3 + list(reversed(round_keys))


def get_s_blocks_inputs(bin_data: str) -> list:
    s_block_inputs = get_text_blocks(bin_data, 4)
    return s_block_inputs


def mod_32(text_block: str, round_key: str) -> str:
    first_number = int(text_block, 2)
    second_number = int(round_key, 2)
    temp = first_number + second_number
    result = bin(temp % 2 ** 32)[2:].zfill(32)
    return result


def cyclic_shift_to_left(text: str, number: int) -> str:
    result = text[number:] + text[0:number]
    return result


def f_function(text_block: str, round_key: str) -> str:
    mod_32_result = mod_32(text_block, round_key)
    s_blocks_inputs = get_s_blocks_inputs(mod_32_result)
    result = ''
    for i in range(len(s_blocks_inputs)):
        col = int(s_blocks_inputs[i], 2)
        row = i
        temp = bin(s_blocks[row][col])[2:].zfill(4)
        result += temp
    result = cyclic_shift_to_left(result, 11)
    return result


def feistel_scheme(text_block: str, round_keys: list, rounds_number: int) -> str:
    text_part = ''
    left_part, right_part = get_text_blocks(text_block, 32)
    for i in range(rounds_number):
        if i == 31:
            f_function_result = f_function(right_part, round_keys[i])
            xor_result = xor(left_part, f_function_result)
            text_part = xor_result + right_part
        else:
            f_function_result = f_function(right_part, round_keys[i])
            xor_result = xor(left_part, f_function_result)
            left_part, right_part = right_part, xor_result
    return text_part


def decode_from_bin_to_hex(bin_str: str) -> Union[str, bytes]:
    int_str = int(bin_str, 2)
    hex_str = hex(int_str)[2:]
    return hex_str


def encode(plaintext: str) -> str:
    key = 12312312312312123123123123123123123131231231231312312123123
    cipher_text = ''
    n = 32
    bin_plaintext = text_decode_to_binary(plaintext, 'encode')
    bin_plaintext = padding(bin_plaintext, 'plaintext', 64)
    plaintext_blocks = get_text_blocks(bin_plaintext, 64)
    for plaintext_block in plaintext_blocks:
        round_keys = get_round_keys(key)
        cipher_text_part = feistel_scheme(plaintext_block, round_keys, n)
        cipher_text += cipher_text_part
    return decode_from_bin_to_hex(cipher_text)


def decode(cipher_text: str) -> str:
    key = 12312312312312123123123123123123123131231231231312312123123
    plaintext = ''
    n = 32
    cipher_text = text_decode_to_binary(cipher_text, 'decode')
    cipher_text = padding(cipher_text, 'cipher_text', 64)
    cipher_text_blocks = get_text_blocks(cipher_text, 64)
    for cipher_text_block in cipher_text_blocks:
        round_keys = get_round_keys(key)
        round_keys.reverse()
        plaintext_part = feistel_scheme(cipher_text_block, round_keys, n)
        plaintext += plaintext_part
    hex_result = decode_from_bin_to_hex(plaintext)
    plaintext = unhexlify(hex_result).decode()
    return plaintext


def tests(n: int, text_len: int) -> bool:
    success = False
    key_len = 16
    count = 0
    for i in range(n):
        plaintext = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(text_len))
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_len))
        first = encode(plaintext, key)
        decode_res = decode(first, key)
        if decode_res == plaintext:
            count += 1
    if count == n:
        success = True
    return success


# def main():
#     mode = input('''
# Режим работы:
# 1) Зашифровать
# 2) Расшифровать
# Ответ: ''')
#
#     if mode == '1':
#         # start_time = time.time()
#         # with open('plaintext', 'r', encoding='utf-8') as f:
#         #     pt = f.read()
#         # with open('key', 'r', encoding='utf-8') as f:
#         #     key = int(f.read())
#         try:
#             pt = input('Открытый текст: ')
#             key = input('Ключ: ')
#             if not (pt and key):
#                 raise ValueError("Ключ или строка пустые")
#             if key.isdecimal():
#                 key = int(key)
#             else:
#                 raise ValueError("Ключ не число")
#             result = encode(pt, key)
#             print('Шифротекст:', result)
#             # with open('ciphertext', 'w', encoding='utf-8') as f:
#             #     f.write(result)
#         except ValueError as e:
#             print(colored(str(e), 'red'))
#         except Exception:
#             print(colored("Произошла непредвиденная ошибка", 'red'))
#         # print(f'time: {time.time() - start_time}')
#     elif mode == '2':
#         # start_time = time.time()
#         # with open('ciphertext', 'r', encoding='utf-8') as f:
#         #     ct = f.read()
#         # with open('key', 'r', encoding='utf-8') as f:
#         #     key = int(f.read())
#         try:
#             ct = input('Шифротекст: ')
#             key = input('Ключ: ')
#             if not(ct and key):
#                 raise ValueError("Ключ или строка пустые")
#             if key.isdecimal():
#                 key = int(key)
#             else:
#                 raise ValueError("Ключ не число")
#             result = decode(ct, key)
#             print('Открытый текст:', result)
#             # with open('plaintext', 'w', encoding='utf-8') as f:
#             #     f.write(result)
#         except ValueError as e:
#             print(colored(str(e), 'red'))
#         except Exception:
#             print(colored("Произошла непредвиденная ошибка", 'red'))
#         # print(f'time: {(time.time() - start_time)}')
#     else:
#         print(colored('Выбран несуществующий режим работы', 'red'))

