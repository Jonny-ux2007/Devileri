from pyexpat.errors import messages
from routes.categories import menu

from database import get_connection

def check_login(message, bot):
    text = message.text.strip()
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
            SELECT user_id  FROM [user] WHERE username= ?
            '''
    cursor.execute(query, (text,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    next_log(message,bot,result)

def next_log(message,bot,result):
    if result is None:
        bot.send_message(message.chat.id, 'Такого акканута нет! Введите /start')
        return False
    else:
        bot.send_message(message.chat.id, 'Введите пароль...')
        bot.register_next_step_handler(message, check_password, bot, result[0])
        return True

def check_password(message, bot, user_id):
    tg_id = message.from_user.id
    text = message.text.strip()
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
            SELECT password FROM [user] WHERE user_id= ?
            '''
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    if result[0]!= text:
        bot.send_message(message.chat.id, 'Вы неверно ввели пароль! \nВведите /start')
    else:
        bot.send_message(message.chat.id, 'Вы успешно вошли!\nВведите /main')

        query = '''
                UPDATE [user] SET tg_id = ? WHERE tg_id = ? 
                '''
        cursor.execute(query, (0, tg_id))

        query = '''
                UPDATE [user] SET tg_id = ? WHERE user_id = ?
                '''
        cursor.execute(query, (tg_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()


def add_user(message,username, password, role):
    telegram_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    query = '''
            INSERT INTO [user] (username, password, role, tg_id)
            VALUES (?, ?, ?, ?)
            '''
    
    cursor.execute(query, (username, password, role, telegram_id))

    conn.commit()
    cursor.close()
    conn.close()

def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
                DELETE FROM [user]
                WHERE user_id = ?
        '''
    
    cursor.execute(query, (user_id,))

    cursor.commit()
    cursor.close()

def check_tg_id(message, bot):
    telegram_id = message.from_user.id
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
            SELECT  tg_id FROM [user] WHERE tg_id = ?
            '''
    cursor.execute(query, (telegram_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None:
        return True
    else:
        return False

def unique_login(message,bot):
    username = message.text.strip()

    conn = get_connection()
    cursor = conn.cursor()

    query = '''SELECT user_id
                FROM [user] 
                WHERE username = ?'''

    cursor.execute(query, (username,))

    result = cursor.fetchone()

    cursor.close()

    if result is not None:
        bot.send_message(message.chat.id, 'Такой логин уже занят!!! Придумайте другой!')
        add_login(message,bot)
    else:
        bot.send_message(message.from_user.id, f'Отлично, ваш логин: {username}.\nА теперь придумайте пароль:')
        bot.register_next_step_handler(message, add_password, bot, username)


#ПЕРЕДЕЛАТЬ НАДО
def on_click(message,bot):
    text = message.text.strip()

    # ЕСЛИ ПОЛЬЗОВАТЕЛЬ ВВЕЛ КОМАНДУ — ПРЕРЫВАЕМ ШАГ И ЗАПУСКАЕМ ЕЁ ВРУЧНУЮ
    if text.startswith('/'):
        if text == '/main':
            menu(message, bot)  # Сразу вызываем меню
            return  # Выходим из функции, чтобы код ниже не выполнялся
        elif text == '/start':
            start(message)  # Сразу перезапускаем старт
            return
    if message.text.lower() == 'войти':
        bot.send_message(message.from_user.id, 'Введите логин')
        bot.register_next_step_handler(message, check_login, bot)
    elif message.text.lower() == 'зарегистрироваться':
        add_login(message,bot)

def add_login(message,bot):
    if check_tg_id(message,bot):
        bot.send_message(message.from_user.id, 'Придумайте логин')
        bot.register_next_step_handler(message, unique_login,bot)
    else:
        bot.send_message(message.chat.id, 'Ваш телеграм аккаунт уже был зарегистрирован! Напишите /start')

def add_password(message, bot, username):
    user_password = message.text.strip()
    bot.send_message(message.from_user.id, f"Успех!\nЛогин: {username}\nПароль: {user_password}")
    add_user(message, username,user_password,'user')
    bot.send_message(message.chat.id, 'Напишите -> /main, чтобы продолжить')



