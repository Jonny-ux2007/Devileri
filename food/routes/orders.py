from database import *
from telebot import types

def order_item(message,bot):
    conn = get_connection()
    cursor = conn.cursor()

    text = message.text.strip()

    if text == '<-- Назад':
        from routes.categories import menu_category
        menu_category(message, bot)
        return

    tg_id = message.chat.id
    product_name,price= '',''

    if '---' in text:
        product_name, price = text.split('---')
        product_name = product_name.strip()
        price = float(price)

    query = '''
            SELECT user_id FROM [user] WHERE tg_id = ?
            '''
    cursor.execute(query, (tg_id,))
    user_row = cursor.fetchone()

    if user_row is None:
        bot.send_message(message.chat.id, "Вы не авторизованы! Введите /start")
        cursor.close()
        conn.close()
        from routes.categories import menu
        menu(message, bot)
        return

    user_id = user_row[0]

    query = '''
            SELECT order_id FROM orders WHERE user_id = ? AND status = ?
            '''
    cursor.execute(query, (user_id,'inbasket'))
    order_id = cursor.fetchone()
    if order_id is not None:
        or_id = order_id[0]
        query = '''
                INSERT INTO order_items (order_id, product_id, price_one_order) 
                VALUES (?,(SELECT product_id FROM product WHERE name = ?), ?)
                '''
        cursor.execute(query, (or_id,product_name, price))
        conn.commit()
        cursor.close()
        conn.close()

        bot.send_message(message.chat.id, "Товар добавлен в корзину!")
        from routes.categories import menu_category
        menu_category(message, bot)

    else:
        query = '''
                INSERT INTO orders (user_id) 
                OUTPUT inserted.order_id 
                VALUES (?) 
                '''
        or_id = cursor.execute(query, (user_id,)).fetchval()

        query = '''
                INSERT INTO order_items (order_id, product_id, price_one_order) 
                VALUES (?,(SELECT product_id FROM product WHERE name = ?), ?)
                '''
        cursor.execute(query, (or_id,product_name, price))

        conn.commit()
        cursor.close()
        conn.close()
        bot.send_message(message.chat.id, "Товар успешно добавлен!")
        from routes.categories import menu_category
        menu_category(message, bot)


def show_basket(message,bot):
    tg_id = message.chat.id
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
            SELECT user_id FROM [user] WHERE tg_id = ?
            '''
    cursor.execute(query, (tg_id,))
    result = cursor.fetchone()

    if result is None:
        bot.send_message(message.chat.id, "Вы не авторизованы! Введите /start")
        cursor.close()
        conn.close()
        from routes.categories import menu
        menu(message, bot)
        return

    user_id = result[0]
    query = '''
            SELECT order_id,status FROM orders WHERE user_id = ?
            '''
    cursor.execute(query, (user_id,))
    lst = cursor.fetchall()
    if lst:
        variable = False
        for order_id, status in lst:
            if status == 'inbasket':
                variable = True
                query = '''
                        SELECT SUM(price_one_order) FROM order_items WHERE order_id = ?
                        '''
                cursor.execute(query, (order_id,))
                summa = cursor.fetchone()[0]

                query = '''
                        SELECT oi.price_one_order, p.name FROM order_items oi
                        JOIN product p ON oi.product_id = p.product_id
                        WHERE oi.order_id = ?
                        '''
                cursor.execute(query, (order_id,))
                lst = cursor.fetchall()
                text = 'Корзина\n'

                for price, name in lst:
                    text += f'{name} -> {price}\n'

                text += f'Общая стоимость {summa}'

                bot.send_message(message.chat.id, text)
                markup = types.ReplyKeyboardMarkup(one_time_keyboard= True, resize_keyboard= True)
                yes_btn = types.KeyboardButton('Да')
                no_btn = types.KeyboardButton('Нет')
                markup.row(yes_btn, no_btn)
                bot.send_message(message.chat.id, "удалить предмет из корзины?", reply_markup=markup)
                bot.register_next_step_handler(message,delete_choice, bot)
        if variable == False:
            bot.send_message(message.chat.id, 'Корзина пуста!')
            from routes.categories import menu
            menu(message, bot)

    else:
        bot.send_message(message.chat.id, 'Корзина пуста!')
        from routes.categories import menu
        menu(message, bot)

    conn.commit()
    cursor.close()
    conn.close()

def pay_for_basket(message,bot):
    variable = False
    tg_id = message.chat.id
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
                SELECT user_id FROM [user] WHERE tg_id = ?
                '''
    cursor.execute(query, (tg_id,))
    user_id = cursor.fetchone()

    if user_id is None:
        bot.send_message(message.chat.id, "Вы не авторизованы! Введите /start")
        cursor.close()
        conn.close()
        from routes.categories import menu
        menu(message, bot)
        return

    query ='''
            SELECT order_id FROM orders WHERE user_id = ?
            '''
    cursor.execute(query, (user_id[0],))
    order_id = cursor.fetchall()
    if order_id:
        for or_id in order_id:
            query = '''
                    SELECT status FROM orders WHERE order_id = ?
                    '''
            cursor.execute(query, (or_id[0],))
            status = cursor.fetchone()[0]
            if status == 'inbasket':
                query = '''
                        UPDATE orders SET status= ? WHERE order_id = ?
                        '''
                cursor.execute(query, ('paid',or_id[0]))
                bot.send_message(message.chat.id, "Вы успешно оплатили корзину!")
                variable = True
                from routes.categories import menu
                menu(message, bot)

        if variable == False:
            from routes.categories import menu
            bot.send_message(message.chat.id, "Ваша корзина пуста!")
            menu(message, bot)
    else:
        from routes.categories import menu
        bot.send_message(message.chat.id, "Ваша корзина пуста!")
        menu(message, bot)

    conn.commit()
    cursor.close()
    conn.close()


def delete_choice(message,bot):
    if message.text.strip() == 'Да':
        bot.send_message(message.chat.id, 'Напишите название продукта, который хотите удалить')
        bot.register_next_step_handler(message, delete_item,bot)
    else:
        from routes.categories import menu
        menu(message, bot)

def delete_item(message, bot):
    text = message.text.strip()
    tg_id = message.chat.id
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
            SELECT user_id FROM [user] WHERE tg_id = ?
            '''
    cursor.execute(query, (tg_id,))
    id = cursor.fetchone()[0]

    query = '''
            SELECT order_id FROM orders WHERE user_id = ? AND status = ?
            '''
    cursor.execute(query, (id,'inbasket'))
    or_id = cursor.fetchone()[0]

    query = '''
            DELETE TOP (1) FROM order_items WHERE  order_id =? AND product_id = (SELECT product_id FROM product WHERE name = ?)
            '''
    cursor.execute(query, (or_id,text))

    bot.send_message(message.chat.id, 'Продукт успешно удален!')

    query = '''
            SELECT order_id FROM order_items WHERE order_id = ?
            '''
    cursor.execute(query, (or_id,))
    result = cursor.fetchone()
    if result is None:
        query = '''
                DELETE FROM orders WHERE order_id = ?
                '''
        cursor.execute(query, (or_id,))

    from routes.categories import menu
    menu(message, bot)
    conn.commit()
    cursor.close()
    conn.close()