from database import *
from telebot import types
from routes.orders import *

def menu(message, bot):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    menu_btn = types.KeyboardButton('Меню')
    basket = types.KeyboardButton('Корзина')
    courier = types.KeyboardButton('Устроиться курьером')
    markup.row(menu_btn, basket, courier)
    bot.send_message(message.chat.id, 'Что хотите выбрать?', reply_markup=markup)
    bot.register_next_step_handler(message, menu2, bot)


def menu2(message,bot):
    if message.text.strip() == 'Меню':
        menu_category(message,bot)
    elif message.text.strip() == 'Корзина':
        show_basket(message,bot)
    elif message.text.strip() == 'Устроиться курьером':
        pass

def menu_category(message, bot):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    back = types.KeyboardButton('<-- Назад')
    beverages = types.KeyboardButton('Напитки')
    Potato = types.KeyboardButton('Картошка')
    Doner = types.KeyboardButton('Донеры')
    Sauces = types.KeyboardButton('Соусы')

    markup.row(back)
    markup.row(beverages, Potato, Doner, Sauces)

    bot.send_message(message.chat.id, 'Категории', reply_markup=markup)
    bot.register_next_step_handler(message, choice, bot)

def choice(message, bot):
    text = message.text.strip()

    if text == '<-- Назад':
        menu(message, bot)
    elif text == 'Напитки':
        from routes.products import beverages_cat
        beverages_cat(message,bot,text)
    elif text == 'Картошка':
        from routes.products import potato_cat
        potato_cat(message,bot,text)
    elif text == 'Донеры':
        from routes.products import doners_cat
        doners_cat(message, bot, text)
    elif text == 'Соусы':
        from routes.products import souces_cat
        souces_cat(message,bot,text)

