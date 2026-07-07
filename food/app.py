import logging

import telebot

from routes.categories import *
from routes.users import *

telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot('8862700075:AAFT77qaO6YkNFjDDR0rK986EhhaeD8Vb6g')

# обрабатывает комманду 
@bot.message_handler(commands = ['start'])
def start(message):
     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
     log_in = types.KeyboardButton('Войти')
     register = types.KeyboardButton('Зарегистрироваться')
     markup.row(log_in, register)
     bot.send_message(message.chat.id, 'Добро пожаловать. Войдите или зарегистрируйтесь в аккаунт!',
                      reply_markup=markup)
     bot.register_next_step_handler(message, on_click,bot)

@bot.message_handler(commands = ['main'])
def main(message):
    menu(message, bot)


bot.infinity_polling()