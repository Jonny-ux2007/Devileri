from db.user_db import *

def next_log(message,bot,result):
    if result is None:
        bot.send_message(message.chat.id, 'Такого акканута нет! Введите /start')
        return False
    else:
        bot.send_message(message.chat.id, 'Введите пароль...')
        bot.register_next_step_handler(message, check_password, bot, result[0])
        return True

def on_click(message,bot):
    text = message.text.strip().lower()
    if message.text.lower() == 'войти':
        bot.send_message(message.from_user.id, 'Введите логин')
        bot.register_next_step_handler(message, check_login,bot)
    elif message.text.lower() == 'зарегистрироваться':
        add_login(message,bot)

def add_login(message,bot):
    if check_tg_id(message):
        bot.send_message(message.from_user.id, 'Придумайте логин')
        bot.register_next_step_handler(message, unique_login,bot)
    else:
        bot.send_message(message.chat.id, 'Ваш телеграм аккаунт уже был зарегистрирован! Напишите /start')

def add_password(message, bot, username):
    user_password = message.text.strip()
    if user_password[0] == '/':
        bot.send_message(message.chat.id, 'Нельзя запаролиться как команда! пропишите /start')
        return
    bot.send_message(message.from_user.id, f"Успех!\nЛогин: {username}\nПароль: {user_password}")
    add_user(message, username,user_password,'user')
    bot.send_message(message.chat.id, 'Напишите -> /main, чтобы продолжить')