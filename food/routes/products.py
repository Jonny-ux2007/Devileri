from database import *
from db.products_db import *
from telebot import types
from routes.categories import *
from routes.orders import order_item

def code(message, bot, name_category):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    lst = product_cat(name_category)
    back = types.KeyboardButton('<-- Назад')
    markup.row(back)
    for name, price in lst:
        markup.add(types.KeyboardButton(f'{name}---{price}'))
    return markup

def beverages_cat(message, bot, name_category):
    markup = code(message, bot, name_category)
    bot.send_message(message.chat.id, 'Доcтупные напитки...',reply_markup=markup)
    bot.register_next_step_handler(message, order_item, bot)

def potato_cat(message, bot, name_category):
    markup = code(message, bot, name_category)
    bot.send_message(message.chat.id, 'Доcтупные размеры картошки...', reply_markup=markup)
    bot.register_next_step_handler(message, order_item, bot)

def doners_cat(message, bot, name_category):
    markup = code(message, bot, name_category)
    bot.send_message(message.chat.id, 'Доcтупные донеры...', reply_markup=markup)
    bot.register_next_step_handler(message, order_item, bot)

def souces_cat(message, bot, name_category):
    markup = code(message, bot, name_category)
    bot.send_message(message.chat.id, 'Доcтупные соусы...', reply_markup=markup)
    bot.register_next_step_handler(message, order_item, bot)
