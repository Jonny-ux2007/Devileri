from database import *

def order_item(message,bot):
    conn = get_connection()
    cursor = conn.cursor()

    text = message.text.strip()
    tg_id = message.chat.id
    product_name,price= '',''

    if '---' in text:
        product_name, price = text.split('---')
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
            SELECT order_id FROM orders WHERE user_id = ?
            '''
    cursor.execute(query, (user_id,))
    id = cursor.fetchone()
    if id is not None:
        or_id = id[0]
        query = '''
                INSERT INTO order_items (order_id, product_id, price_one_order) 
                VALUES (?,(SELECT product_id FROM product WHERE name = ?), ?)
                '''
        cursor.execute(query, (or_id,product_name, price))
        conn.commit()
        cursor.close()
        conn.close()

        bot.send_message(message.chat.id, "Товар добавлен в корзину!")
        from routes.categories import menu
        menu(message, bot)

    else:
        query = '''
                INSERT INTO orders (user_id) VALUES (?) 
                '''
        cursor.execute(query, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        from routes.categories import menu
        menu(message, bot)


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

    use_id = result[0]
    query = '''
            SELECT order_id FROM orders WHERE user_id = ?
            '''
    cursor.execute(query, (use_id,))
    id = cursor.fetchone()
    if id is not None:
        id_new = id[0]
        query = '''
                SELECT SUM(price_one_order) FROM order_items WHERE order_id = ?
                '''
        cursor.execute(query, (id_new,))
        summa = cursor.fetchone()[0]

        query = '''
                SELECT oi.price_one_order, p.name FROM order_items oi
                JOIN product p ON oi.product_id = p.product_id
                WHERE oi.order_id = ?
                '''
        cursor.execute(query, (id_new,))
        lst = cursor.fetchall()
        text = 'Корзина\n'

        for price, name in lst:
            text += f'{name} -> {price}\n'

        text += f'Общая стоимость {summa}'

        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Корзина пуста!')

    conn.commit()
    cursor.close()
    conn.close()
    from routes.categories import menu
    menu(message,bot)