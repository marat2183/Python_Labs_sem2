import json
from math import fabs
import re


# def validate_ip_addr(ip_addr):
#     result = re.match(r'^(((\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5])\.){3}(\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5]))$',
#                       ip_addr)
#     if result is None:
#         return False
#     else:
#         return True
#
#
# def validate_cidr_ip(ip_addr):
#     result = re.match(r'^((((\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5])\.){3}(\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5]))\/(\d|[1-2][0-9]|3[0-2]))$',
#                       ip_addr)
#     if result is None:
#         return False
#     else:
#         return True


def decode_ip_to_binary(user_input):
    temp = user_input.split('.')
    res = ''.join([bin(int(i))[2:].zfill(8) for i in temp])
    return res


def decode_ip_to_list(user_input):
    return [int(i) for i in user_input.split('.')]


def get_mask_from_length(mask_number):
    with open('mask.json') as f:
        masks = json.load(f)
    return '.'.join([str(i) for i in masks[mask_number]])


def invert_mask(mask):
    return [int(fabs(i - 255)) for i in mask]


def decode_cidr_ip(user_input):
    ip, mask_number = user_input.split('/')
    ip_address = [int(i) for i in ip.split('.')]
    with open('mask.json') as f:
        masks = json.load(f)
    return ip_address, mask_number, masks[mask_number]


def user_input_handler(user_input, task_number):
    if task_number == 1 or task_number == 3:
        return decode_ip_to_binary(user_input)
    elif task_number == 2 or task_number == 4:
        return decode_cidr_ip(user_input)
    elif task_number == 5:
        first_ip, second_ip = user_input
        first_ip = decode_ip_to_list(first_ip)
        second_ip, _, mask = decode_cidr_ip(second_ip)
        return first_ip, second_ip, mask
    elif task_number == 6:
        first_ip = decode_ip_to_binary(user_input[0])
        second_ip = decode_ip_to_binary(user_input[1])
        return first_ip, second_ip


def get_ip_class(ip_addr):
    if ip_addr.startswith('0'):
        return 'A'
    elif ip_addr.startswith('10'):
        return 'B'
    elif ip_addr.startswith('110'):
        return 'C'
    elif ip_addr.startswith('1110'):
        return 'D'
    elif ip_addr.startswith('1111'):
        return 'E'
    else:
        return None


def get_mask_by_class(class_name):
    if class_name == 'A':
        return ['255', '0', '0', '0']
    elif class_name == 'B':
        return ['255', '255', '0', '0']
    elif class_name == 'C':
        return ['255', '255', '255', '0']
    elif class_name == 'D':
        return ['255', '255', '255', '255']
    elif class_name == 'E':
        return ['255', '255', '255', '255']


def get_network_address(ip_addr, mask):
    result = [str(i & j) for i, j in zip(ip_addr, mask)]
    return '.'.join(result)


def get_broadcast_address(ip_addr, mask):
    mask = invert_mask(mask)
    result = [str(i | j) for i, j in zip(ip_addr, mask)]
    return '.'.join(result)


def first_task(user_input, task_number):
    result = dict()
    result['IP Адрес'] = user_input
    user_input = user_input_handler(user_input, task_number)
    result['Класс'] = get_ip_class(user_input)
    if result['Класс'] is None:
        result['Класс'] = "Не удалось определить класс'"
        result['Маска'] = 'Не удалось определить маску, так как класс не был определен'
    else:
        mask = get_mask_by_class(result['Класс'])
        result['Маска'] = '.'.join(mask)
        result["Адрес сети"] = get_network_address([int(i) for i in result['IP Адрес'].split('.')], [int(i) for i in mask])
        result["Широковещательный адрес"] = get_broadcast_address([int(i) for i in result['IP Адрес'].split('.')], [int(i) for i in mask])
    return result


def second_task(user_input, task_number):
    result = dict()
    user_input = user_input_handler(user_input, task_number)
    result['IP Адрес'] = '.'.join([str(i) for i in user_input[0]])
    result['Номер маски'] = user_input[1]
    result['Маска'] = get_mask_from_length(user_input[1])
    result['Адрес сети'] = get_network_address(user_input[0], user_input[2])
    result['Широковещательный адрес'] = get_broadcast_address(user_input[0], user_input[2])
    return result


def third_task(user_input, task_number):
    result = dict()
    bin_mask = user_input_handler(user_input, task_number)
    if '01' in bin_mask:
        result['Итог'] = "Маска неправильная"
    else:
        result['Итог'] = "Маска верна"
    return result


def fourth_task(user_input, task_number):
    result = dict()
    ip_address, _, mask = user_input_handler(user_input, task_number)
    network_address = get_network_address(ip_address, mask)
    if network_address == '.'.join(str(i) for i in ip_address):
        result['Итог'] = f"Да, {'.'.join(list(map(str,ip_address)))} - адрес сети"
    else:
        result['Итог'] = f"Нет, {'.'.join(list(map(str,ip_address)))} - не адрес сети"
    return result


def fifth_task(user_input, task_number):
    result = dict()
    first_ip, second_ip, mask = user_input_handler(user_input, task_number)
    first_network_address = get_network_address(first_ip, mask)
    second_network_address = get_network_address(second_ip, mask)
    if first_network_address == second_network_address:
        result['Итог'] = 'В одной подсети'
    else:
        result['Итог'] = 'В разных подсетях'
    return result


def sixth_task(user_input, task_number):
    result = dict()
    first_ip, second_ip = user_input_handler(user_input, task_number)
    count = 0
    while first_ip[count] == second_ip[count]:
        count += 1
    result['Минимальная длина маски'] = count
    return result


def solve_task(user_input, task_number):
    if task_number == 1:
        return first_task(user_input, task_number)
    elif task_number == 2:
        return second_task(user_input, task_number)
    elif task_number == 3:
        return third_task(user_input, task_number)
    elif task_number == 4:
        return fourth_task(user_input, task_number)
    elif task_number == 5:
        return fifth_task(user_input, task_number)
    elif task_number == 6:
        return sixth_task(user_input, task_number)



