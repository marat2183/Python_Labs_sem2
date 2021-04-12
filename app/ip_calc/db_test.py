import sqlite3
from app.magma_cipher.Magma import decode, encode
import os


dir_path = os.path.dirname(os.path.realpath(__file__))

con = sqlite3.connect(dir_path + '\\ip_calc.db')
cur = con.cursor()


def success(status, message, user=''):
    return {'status': status, 'message': message, 'user': user}


def error(status, message):
    return {'status': status, 'message': message}


def check_username(username):
    try:
        cur.execute("SELECT name,password FROM users WHERE login = ?", (username,))
        user = cur.fetchone()
        if user is None:
            return True
        else:
            return False
    except:
        return False


def create_user(name, login, password):
    status = 1
    try:
        cur.execute("INSERT INTO users (name, login, password) VALUES (?,?,?)", (name, login, encode(password)))
        con.commit()
        return success(status, "Пользователь успешно создан", login)
    # except sqlite3.IntegrityError:
    #     status = 2
    #     return error(status, "Пользователь с таким именем уже существует")
    except:
        status = 0
        return error(status, "Произошла непредвиденная ошибка")


def get_user(login, password):
    try:
        cur.execute("SELECT name,login,password FROM users WHERE login = ? AND password = ?", (login, encode(password)))
        user = cur.fetchone()
        if user is None:
            return error(0, "Неверный логин или пароль")
        else:
            return success(1, f"Вы успешно авторизировались под именем {user[1]}", user[1])
    except:
        return error(2, "Произошла непредвиденная ошибка")


