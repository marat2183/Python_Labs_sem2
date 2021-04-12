from app.ip_calc.solver import *
from time import sleep
from app.ip_calc.db_test import *
from termcolor import colored
from datetime import date
import time
import socket

repeater_for_task_selection = """
Режим работы:
1) Первое задание
2) Второе задание
3) Третье задание
4) Четвертое задание
5) Пятое задание
6) Шестое задание
7) Выход
Ответ: """

repeater_for_tasks = """
1) Попробовать снова
2) Выбрать другое задание
3) Выйти
Ответ: """

repeater_for_auth = """
1) Попробовать снова
2) Зарегистрироваться
Ответ: """

USERNAME_REGEX = r'^([a-zA-Z0-9]{8,25})$'
PASSWORD_REGEX = r'^([a-zA-Z0-9]{8,25})$'
NAME_REGEX = r'^([A-Z][a-z]+|[a-z][a-z]+)|([А-Я][а-я]+|[а-я][а-я]+)$'
IP_REGEX = r'^(((\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5])\.){3}(\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5]))$'
CIDR_IP_REGEX = r'^((((\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5])\.){3}(\d|[1-9]\d|1\d\d|2[0-4][0-9]|25[0-5]))\/(\d|[1-2][0-9]|3[0-2]))$'
PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 25
USERNAME_MIN_LEN = 8
USERNAME_MAX_LEN = 25
table = f"""
====================Валидация данных====================
Имя : может начинаться с большой или маленькой буквы на русском или английском языке
Логин: прописные и строчные буквы английского языка.
Минимальная длина логина = {USERNAME_MIN_LEN}
Максимальная длина логина = {USERNAME_MAX_LEN}
Пароль: прописные и строчные буквы английского языка.
Минимальная длина логина = {PASSWORD_MIN_LEN}
Максимальная длина логина = {PASSWORD_MAX_LEN}
"""


user_log_path = os.path.abspath('..') + '\\users.log'


def add_record_to_log(data):
    today = date.today()
    date_format = today.strftime("%b-%d-%Y")
    t = time.localtime()
    time_format = time.strftime("%H:%M:%S", t)
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    result = f"{ip_address} | {data} | {date_format} | {time_format}\n"
    with open(user_log_path, 'a') as f:
        f.write(result)


def get_results(result):
    print("=========Результаты=========")
    for k, v in result.items():
        print(f"{k}: {v}")


def error_message(message):
    print(colored(message, 'red'))


def success_message(message):
    print(colored(message, 'green'))


def validation(user_input, input_type, regex, message):
    result = re.match(regex, user_input)
    if result is None:
        error_message(message)
        end = False
        while not end:
            user_input = input(f"Введите {input_type}: ")
            result = re.match(regex, user_input)
            if result is None:
                error_message(message)
            else:
                end = True
        return user_input
    else:
        return user_input


def get_ip(text, e_message):
    ip = input(f"Введите {text}: ")
    temp_ip = validation(ip, text, IP_REGEX, e_message)
    ip = temp_ip
    return ip


def get_ip_with_mask(text, e_message):
    ip = input(f"Введите {text}: ")
    temp_ip = validation(ip, text, CIDR_IP_REGEX, e_message)
    ip = temp_ip
    return ip


def first_task_input():
    ip_addr = get_ip("ip адрес", "Некорректный ip адрес")
    get_results(solve_task(ip_addr, 1))


def second_task_input():
    ip_addr = get_ip_with_mask("ip адрес", "Некорректный ip адрес")
    get_results(solve_task(ip_addr, 2))


def third_task_input():
    mask = get_ip("маску", "Некорректная маска")
    get_results(solve_task(mask, 3))


def fourth_task_input():
    ip_addr = get_ip_with_mask("ip адрес", "Некорректный ip адрес")
    get_results(solve_task(ip_addr, 4))


def fifth_task_input():
    first_ip = get_ip("первый ip адрес", "Некорректный ip адрес")
    second_ip = get_ip_with_mask("второй ip адрес", "Некорректный ip адрес")
    user_input = [first_ip, second_ip]
    get_results(solve_task(user_input, 5))


def sixth_task_input():
    first_ip = get_ip("первый ip адрес", "Некорректный ip адрес")
    second_ip = get_ip("второй ip адрес", "Некорректный ip адрес")
    user_input = [first_ip, second_ip]
    get_results(solve_task(user_input, 6))


def get_username(action):
    username = input("Введите логин: ")
    if action == "Регистрация":
        temp_username = validation(username, 'логин', USERNAME_REGEX, "Некорректный логин")
        username = temp_username
    return username


def get_password(action):
    password = input("Введите пароль: ")
    if action == "Регистрация":
        temp_password = validation(password, 'пароль', PASSWORD_REGEX, "Некорректный пароль")
        password = temp_password
    return password


def get_name():
    name = input("Введите имя: ")
    temp_name = validation(name, 'имя', NAME_REGEX, "Некорректное имя")
    if temp_name:
        return name
    else:
        return name


def task_selection():
    end = False
    while not end:
        mode = input(repeater_for_task_selection)
        if mode == '1':
            first_task_input()
            sleep(1)
        elif mode == '2':
            second_task_input()
            sleep(1)
        elif mode == '3':
            third_task_input()
            sleep(1)
        elif mode == '4':
            fourth_task_input()
            sleep(1)
        elif mode == '5':
            fifth_task_input()
            sleep(1)
        elif mode == '6':
            sixth_task_input()
            sleep(1)
        elif mode == '7':
            end = True
        else:
            error_message("Некорректный выбор")


def registration():
    cycle_flag = True
    print("========Регистрация========")
    name = get_name()
    while cycle_flag:
        username = get_username("Регистрация")
        temp = check_username(username)
        if temp:
            cycle_flag = False
        else:
            error_message("Пользователь с таким логином уже существует")
    password = get_password("Регистрация")
    db_response = create_user(name=name, login=username, password=password)
    return db_response


def authorization():
    print("=====Авторизация=====")
    username = get_username("Авторизация")
    password = get_password("Авторизация")
    db_response = get_user(username, password)
    return db_response


def auth_menu_handler():
    cycle_flag = True
    while cycle_flag:
        auth_menu_action = input(repeater_for_auth)
        if auth_menu_action == "1" or auth_menu_action == "2":
            cycle_flag = False
        else:
            error_message("Некорректный выбор")
    return auth_menu_action


def start_menu():
    print(table)
    cycle_flag = True
    while cycle_flag:
        user_action = input("""
===========Главное меню===========
1) Зарегистрироваться
2) Войти
Ответ: """)
        if user_action == "1" or user_action == "2":
            cycle_flag = False
        else:
            error_message("Некорректный выбор")

    return user_action


def start_f():
    start_menu_res = start_menu()
    reg_cycle_flag = True
    auth_cycle_flag = True
    continue_reg = False
    if start_menu_res == "1":
        while reg_cycle_flag:
            registration_res = registration()
            if registration_res['status'] == 1:
                while auth_cycle_flag:
                    auth_res = authorization()
                    if auth_res['status'] == 1:
                        success_message(auth_res['message'])
                        add_record_to_log(auth_res['user'])
                        task_selection()
                        auth_cycle_flag = False
                    elif auth_res['status'] == 0:
                        error_message(auth_res['message'])
                        action = auth_menu_handler()
                        if action == "1":
                            pass
                        else:
                            continue_reg = True
                            auth_cycle_flag = False
                    else:
                        error_message(auth_res['message'])
                        auth_cycle_flag = False
                if continue_reg:
                    pass
                else:
                    reg_cycle_flag = False
            else:
                error_message(registration_res['message'])
                reg_cycle_flag = False
    else:
        while auth_cycle_flag:
            auth_res = authorization()
            if auth_res['status'] == 1:
                success_message(auth_res['message'])
                add_record_to_log(auth_res['user'])
                task_selection()
                auth_cycle_flag = False
            elif auth_res['status'] == 0:
                error_message(auth_res['message'])
                action = auth_menu_handler()
                if action == "1":
                    pass
                else:
                    registration_res = registration()
                    if registration_res['status'] == 1:
                        success_message(registration_res['message'])
                    else:
                        error_message(registration_res['message'])
                        auth_cycle_flag = False
            else:
                error_message(auth_res['message'])
                auth_cycle_flag = False

