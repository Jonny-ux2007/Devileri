from database import get_connection

def check_login(message,bot):
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

    from routes.users import next_log
    next_log(message, bot, result)

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
        return
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
    if username[0] == '/':
        bot.send_message(message.chat.id, 'Нельзя зарегистрирвоать как команда! пропишите /start')
        return
    if result is not None:
        bot.send_message(message.chat.id, 'Такой логин уже занят!!! Придумайте другой!')
        from routes.users import add_login
        add_login(message,bot)
    else:
        bot.send_message(message.from_user.id, f'Отлично, ваш логин: {username}.\nА теперь придумайте пароль:')
        from routes.users import add_password
        bot.register_next_step_handler(message, add_password, bot, username)

def check_tg_id(message):
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


def add_user(message, username, password, role):
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