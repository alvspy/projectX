from telebot import *
import sqlite3
from config import bot_token
import hashlib
import secrets

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import students
import mails
import random

conn = sqlite3.connect("info.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users
                (stud_id INTEGER,
                tg_id INTEGER,
                email TEXT PRIMARY KEY,
                name TEXT,
                surname TEXT,
                midname TEXT,
                public_tg TEXT,
                phone TEXT,
                class TEXT)
                """)

cursor.execute("""
                CREATE TABLE IF NOT EXISTS Codes
                (hash INTEGER,
                salt TEXT,
                tg_id INTEGER PRIMARY KEY,
                email TEXT)
                """)



bot = TeleBot(bot_token)

send = bot.send_message

@bot.message_handler(commands=["start"])
def start_message(message):
    send(message.chat.id, "Это бот проета X, для авторизации используйте команду /reg\n"
                          "В любой момент вы можете отправить сообщение \"Отмена\" чтобы прервать текущее действие\n"
                          "Командой /help можео посмотреть список доступных команд")

@bot.message_handler(commands=["reg"])
def reg(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Напишите свою школьную почту")
        bot.register_next_step_handler(message, check_email)
        return
    send(tg_id, "Вы уже авторизованы")

@bot.message_handler(commands=["exit"])
def exit_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    cursor.execute("UPDATE Users SET tg_id = -1 WHERE tg_id = ?", (tg_id,))
    send(tg_id, "Вы вышли")


def check_email(message):
    if message.text == "Отмена":
        return
    tg_id = message.chat.id
    if not is_valid_email(message.text):
        send(tg_id, "Некорректная почта")
        return
    code = mails.send_verification_email(message.text)
    # print(code)
    salt = secrets.token_hex(16)
    cursor.execute("INSERT OR REPLACE INTO Codes VALUES (?,?,?,?)", (get_hash(str(code) + salt), salt, tg_id, message.text))
    conn.commit()
    send(tg_id, "На вашу почту был отправлен верификационный код\n"
                "(Он мог попасть в спам)\n"
                "У вас есть 3 попытки чтобы его ввести")
    bot.register_next_step_handler(message, verify_email)

def verify_email(message, tries=0):
    tg_id = message.chat.id
    if message.text == "Отмена":
        cursor.execute("DELETE FROM Codes WHERE tg_id = ?", (tg_id,))
        conn.commit()
        return
    cursor.execute("SELECT hash, salt FROM Codes WHERE tg_id = ?", (tg_id,))
    hsh, salt = cursor.fetchone()
    cursor.execute("SELECT email FROM Codes WHERE tg_id = ?", (tg_id,))
    email = cursor.fetchone()[0]
    # print(message.text, hsh)
    if not message.text.isdigit() or get_hash(message.text + salt) != hsh:
        if tries == 0:
            send(tg_id, f"Неверный код, осталось 2 попытки")
        elif tries == 1:
            send(tg_id, f"Неверный код, осталась 1 попытка")
        else:
            send(tg_id, f"Неверный код\n"
                        f"У вас не осталось попыток - начните авторизацию заново")
            cursor.execute("DELETE FROM Codes WHERE tg_id = ?", (tg_id,))
            conn.commit()
            return
        bot.register_next_step_handler(message, verify_email, tries + 1)
        return
    cursor.execute("DELETE FROM Codes WHERE tg_id = ?", (tg_id,))
    conn.commit()
    cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result is None:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("Принять ✔", callback_data=email),
            InlineKeyboardButton("Отказаться ✖", callback_data="123")
        )
        bot.send_message(
            tg_id,
            'Для создания аккаунта вам необходимо принять <a href="https://docs.yandex.ru/docs/view?url=ya-disk%3A%2F%2F%2Fdisk%2FDocument%204%20(3).pdf&name=Document%204%20(3).pdf&uid=1590519316">пользовательское соглашение</a>',
            parse_mode='HTML',
            reply_markup=markup
        )
        # cursor.execute("INSERT OR REPLACE INTO Users VALUES (-1, ?, ?, 'None', 'None', 'None')", (tg_id, email))
        # conn.commit()
        return
    cursor.execute("UPDATE Users SET tg_id = ? WHERE email = ?", (tg_id, email))
    conn.commit()
    send(tg_id, "Вы успешно авторизованы")

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    tg_id = call.message.chat.id
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=call.message.text,
        reply_markup=None
    )
    if call.data == "123":
        bot.send_message(call.message.chat.id, "Аккаунт не был создан, так как пользовательское соглашение не было принято")
    else:
        cursor.execute("INSERT OR REPLACE INTO Users VALUES (-1, ?, ?, 'Не предоставлено', 'Не предоставлена', 'Не предоставлено', 'Не предоставлен', 'Не предоставлен', 'Не предоставлен')", (tg_id, call.data))
        conn.commit()
        send(tg_id, "Вы успешно авторизованы")


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None



@bot.message_handler(commands=["add_name"])
def add_name_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    send(tg_id, "Напишите ваше имя")
    bot.register_next_step_handler(message, add_name)

def add_name(message):
    if message.text == "Отмена":
        return
    cursor.execute("UPDATE Users SET name = ? WHERE tg_id = ?", (message.text, message.chat.id))
    send(message.chat.id, "Имя успешно добавлено")


@bot.message_handler(commands=["add_surname"])
def add_surname_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    send(tg_id, "Напишите вашу фамилию")
    bot.register_next_step_handler(message, add_surname)


def add_surname(message):
    if message.text == "Отмена":
        return
    cursor.execute("UPDATE Users SET surname = ? WHERE tg_id = ?", (message.text, message.chat.id))
    send(message.chat.id, "Фамилия успешно добавлена")

@bot.message_handler(commands=["add_phone"])
def add_phone_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    send(tg_id, "Напишите ваш номер телефона")
    bot.register_next_step_handler(message, add_phone)


def add_phone(message):
    if message.text == "Отмена":
        return
    cursor.execute("UPDATE Users SET phone = ? WHERE tg_id = ?", (message.text, message.chat.id))
    send(message.chat.id, "Номер телефона успешно добавлен")

@bot.message_handler(commands=["add_tg"])
def add_tg_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    send(tg_id, "Напишите ваш телеграмм для связи (формат @user)")
    bot.register_next_step_handler(message, add_tg)


def add_tg(message):
    if message.text == "Отмена":
        return
    cursor.execute("UPDATE Users SET public_tg = ? WHERE tg_id = ?", (message.text, message.chat.id))
    send(message.chat.id, "телеграмм для связи успешно добавлен")

@bot.message_handler(commands=["add_class"])
def add_class_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    send(tg_id, "Напишите ваш класс обучения (формат 10 В)")
    bot.register_next_step_handler(message, add_class)


def add_class(message):
    if message.text == "Отмена":
        return
    cursor.execute("UPDATE Users SET class = ? WHERE tg_id = ?", (message.text, message.chat.id))
    send(message.chat.id, "Класс обучения успешно добавлен")


@bot.message_handler(commands=["add_midname"])
def add_midname_cmd(message):
    tg_id = message.chat.id
    if not check_auth(tg_id):
        send(tg_id, "Вы не авторизованы")
        return
    send(tg_id, "Напишите ваше отчество")
    bot.register_next_step_handler(message, add_midname)


def add_midname(message):
    if message.text == "Отмена":
        return
    cursor.execute("UPDATE Users SET midname = ? WHERE tg_id = ?", (message.text, message.chat.id))
    send(message.chat.id, "Отчество успешно добавлено")

@bot.message_handler(commands=["get_info"])
def get_info_cmd(message):
    tg_id = message.chat.id
    send(tg_id, "Введите почту человека, профиль которого вы хотите посмотреть")
    bot.register_next_step_handler(message, get_info)

def get_info(message):
    tg_id = message.chat.id
    if message.text == "Отмена":
        return

    cursor.execute("SELECT * FROM Users WHERE email = ?", (message.text,))
    result = cursor.fetchone()
    if result is None:
        send(tg_id, "Данный пользователь не создал аккаунт")
        return

    send(tg_id, f"Имя: {result[3]}\n"
                f"Фамилия: {result[4]}\n"
                f"Отчество: {result[5]}\n"
                f"Телеграмм для связи: {result[6]}\n"
                f"Номер телефона: {result[7]}\n"
                f"Класс обучения: {result[8]}")





# @bot.message_handler(commands=["get_name"])
# def get_name(message):
#     tg_id = message.chat.id
#     if not check_auth(tg_id):
#         send(tg_id, "Вы не авторизованы")
#         return
#     cursor.execute("SELECT name FROM Users WHERE tg_id = ?", (tg_id,))
#     result = cursor.fetchone()
#     send(tg_id, result[0])
#
# @bot.message_handler(commands=["get_surname"])
# def get_surname(message):
#     tg_id = message.chat.id
#     if not check_auth(tg_id):
#         send(tg_id, "Вы не авторизованы")
#         return
#     cursor.execute("SELECT surname FROM Users WHERE tg_id = ?", (tg_id,))
#     result = cursor.fetchone()
#     send(tg_id, result[0])


@bot.message_handler(commands=["help"])
def get_help(message):
    tg_id = message.chat.id
    send(tg_id, "/reg - Войти по почте\n"
                "/add_name - Добавить имя\n"
                "/add_surname - Добавить фамилию\n"
                "/add_midname - Добавить отчество\n"
                "/add_phone - Добавить номер телефона\n"
                "/add_tg - Добавить телеграмм для связи\n"
                "/add_class - Добавить класс обучения\n"
                "/get_info - Посмотреть профиль человека\n"
                "/exit - Выйти из аккаунта")


def check_auth(tg_id):
    cursor.execute("SELECT * FROM Users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()
    if result is None:
        return False
    return True

def get_email_by_tg(tg_id):
    cursor.execute("SELECT email FROM Users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()
    return result[0]



def get_hash(s):
    hsh = hashlib.sha256(s.encode()).hexdigest()
    return hsh

# @bot.message_handler(content_types=["text"])
# def talk(message):
#     return


bot.polling(none_stop=True, interval=0)
