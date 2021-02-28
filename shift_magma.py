import json
import random
import string
import time
#OK
def get_text_blocks(text):
    res = []
    for x in range(0, len(text), 8):
        temp = text[x:x + 8]
        if len(temp) != 8:
            need_to_add = 8 - (len(temp) % 8)
            temp = b'\x00' * need_to_add + temp
        res.append(temp)
    return res

def get_s_blocks_input(text):
    res = []
    for i in range(8):
        temp = text & 0b1111
        res.append(temp)
        text = text >> 4
    res.reverse()
    return res

def xor(left, right):
    return left ^ right

#OK
def mod32(text, key):
    return (text + key) % 2**32

def cyclic_shift_to_left(text, shift):
    temp = bin(text)[2:].zfill(32)
    res = temp[shift:] + temp[:shift]
    return int(res, 2)

#OK
def get_round_keys(key):
    if key.bit_length() > 256:
        raise Exception('Ключ больше 256 бит')
    res = []
    for i in range(8):
        temp = key & 0xFFFFFFFF
        res.append(temp)
        key = key >> 32
    res.reverse()
    return res


def f_function(text, key):
    global S_blocks
    result = 0
    mod_32_result = mod32(text, key)
    s_blocks_inputs = get_s_blocks_input(mod_32_result)
    for i in range(8):
        col = s_blocks_inputs[i]
        row = i
        temp = S_blocks[row][col]
        result = result << 4
        result = result | temp
    result = cyclic_shift_to_left(result, 11)
    return result


def fiestel_scheme(int_plain_text, round_keys, round_keys_list):
    res = 0
    right_part = int_plain_text & 0xFFFFFFFF
    int_plain_text = int_plain_text >> 32
    left_part = int_plain_text & 0xFFFFFFFF
    for i in range(32):
        if i == 31:
            f_function_result = f_function(right_part, round_keys[round_keys_list[i]])
            xor_result = xor(left=left_part, right=f_function_result)
            res = xor_result << 32
            res = res | right_part
        else:
            f_function_result = f_function(right_part, round_keys[round_keys_list[i]])
            xor_result = xor(left=left_part, right=f_function_result)
            left_part, right_part = right_part, xor_result
    return res

with open('S_blocks_matrix.json') as f:
    data = json.load(f)
S_blocks = data['matrix']


def encode(plain_text, key):
    test1 = []
    itog = b''
    text_blocks = get_text_blocks(plain_text.encode())
    round_keys = get_round_keys(int.from_bytes(key.encode(), 'big'))
    round_keys_list = [0, 1, 2, 3, 4, 5, 6, 7] * 3 + [7, 6, 5, 4, 3, 2, 1, 0]
    # round_keys_list.reverse()
    for text in text_blocks:
        test1.append(int.from_bytes(text, 'big'))
        test = fiestel_scheme(int.from_bytes(text, 'big'), round_keys, round_keys_list)
        itog += test.to_bytes(8, 'big').strip(b'\x00')
    print(test1)
    return itog


def decode(ciphertext, key):
    test1 = []
    itog = b''
    text_blocks = get_text_blocks(ciphertext)
    round_keys = get_round_keys(int.from_bytes(key.encode(), 'big'))
    round_keys_list = [0, 1, 2, 3, 4, 5, 6, 7] * 3 + [7, 6, 5, 4, 3, 2, 1, 0]
    round_keys_list.reverse()
    for text in text_blocks:
        test = fiestel_scheme(int.from_bytes(text, 'big'), round_keys, round_keys_list)
        test1.append(test)
        itog += test.to_bytes(8, 'big').strip(b'\x00')
    print(test1)
    return itog

def tests(n: int, text_len: int) -> bool:
    success = False
    key_len = 16
    count = 0
    for i in range(n):
        plaintext = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(text_len))
        key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(key_len))
        first = encode(plaintext, key)
        try:
            decode_res = decode(first, key)
            decode_res = decode_res.decode()
        except:
            print(plaintext)
            print(key)
        if decode_res == plaintext:
            count += 1
    if count == n:
        success = True
    return success


plain_text = 'Z4HquBTEDXogGvVvUXDPShhie5y803wqTVmU2Gc6y3CnMR3DnPMtE9xnLs1AiLBxGdk7pJooyVwPiTOvjyJYvJZJw13HpQBEYy1QnqBvm8Lo2lrev53AbUtx0RzjtPAqs4X6bOma0H0TJo5wh9pqXokXYu0QhakRmVn3zA1R7d005KfI9jDP9udLS4CMW9AK1PT2w3HQbcHLnHwqNmWpf2348PFoLdfBZZe0kMHS1drGs26UGJlx0YK7UjIeyCsRqtYDdELmxorgSBZBUgoX6WX2SPOymXVtsL0u1vcJvDoURNBciURshQ2tXeb7wCx2SHI3CIwiyNmECPc6DTsNmHeht63oO43rr3rPeupPRkupmxNHj9PBdFS2OWJXhzO3cWJp7PR6Fx1ESa2RbAyTVKPBNYUkKBtZ72yKQGdRXoGpfAQmC2yRmDKJJND5F9EKakqhCPHzMui0jWy4RCfNT0fj5iF2LUAjdsagybWBeaWoK0Wy9bT5'
int_key = 'A3dk1C16EuhJjR1Z'

print('encode')
a = encode(plain_text, int_key)
print(a)
print('decode')
print(decode(a, int_key))
# start_time = time.time()
# if tests(10, 500):
#     print('ok')
#
# print(time.time() - start_time)