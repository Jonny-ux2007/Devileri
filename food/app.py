import telebot
from database import *
from routes.products import *
from routes.users import *
from telebot import types
from routes.categories import *

bot = telebot.TeleBot('8910557183:AAFaqpFgnyCL9jSfDsLcezxJg8EUOLVmcHc')

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

bot.polling(none_stop= True)