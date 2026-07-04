from pyexpat.errors import messages

from database import get_connection

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
        bot.send_message(message.from_user.id, f'Отлично, ваш логин: {username}. А теперь придумайте пароль:')
        bot.register_next_step_handler(message, add_password, bot, username)


def on_click(message,bot):
    if message.text.lower() == 'войти':
        bot.send_message(message.from_user.id, 'Введите логин')
    elif message.text.lower() == 'зарегистрироваться':
        add_login(message,bot)

def add_login(message,bot):
    bot.send_message(message.from_user.id, 'Придумайте логин')
    bot.register_next_step_handler(message, unique_login,bot)

def add_password(message, bot, username):
    user_password = message.text.strip()
    bot.send_message(message.from_user.id, f"Успех!\nЛогин: {username}\nПароль: {user_password}")
    add_user(message, username,user_password,'user')
    bot.send_message(message.chat.id, 'Напишите -> /main, чтобы продолжить')



