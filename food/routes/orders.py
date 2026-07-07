from db.orders_db import *

def delete_choice(message,bot):
    if message.text.strip() == 'Да':
        bot.send_message(message.chat.id, 'Напишите название продукта, который хотите удалить')
        bot.register_next_step_handler(message, delete_item,bot)
    else:
        from routes.categories import menu
        menu(message, bot)