import telebot
from telebot import types
import requests
import json

bot = telebot.TeleBot("6047133927:AAGghMLkgEJTkopYrSksrSmZzCRhsd_bKLE")
about_bot = 'Привет, я Karich-Helper-Bot, введите название города и я скажу какая там погода.'
weather_API_key = 'afca35e0a5606c9a045fa6592eb962cf'


@bot.message_handler(commands=['start', 'channels', 'help'])
def commands(message):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('погода')
        btn2 = types.KeyboardButton('курсы валют')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}',
                         reply_markup=markup)
    elif message.text == '/channels':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Карыч', url='https://www.youtube.com/@user-cx5xi3xn7l'))
        markup.add(types.InlineKeyboardButton('Карыч Страйк', url='https://www.youtube.com/@user-wp5kq6xt8n'))
        btn1 = types.InlineKeyboardButton('delete', callback_data='delete')
        btn2 = types.InlineKeyboardButton('addit', callback_data='edit')
        markup.row(btn1, btn2)
        bot.reply_to(message, 'Вот список каналов ', reply_markup=markup)
    elif message.text == '/help':
        bot.send_message(message.chat.id, about_bot)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.reply_to(message, 'красиво!')


@bot.message_handler(content_types=['video'])
def get_photo(message):
    bot.reply_to(message, 'как интересно!')


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)


@bot.message_handler(content_types=['text'])
def info(message):
    if message.text.lower() == 'погода':
        bot.send_message(message.chat.id, 'введите название города')
    elif message.text.lower() == 'курсы валют':
        bot.send_message(message.chat.id, 'рубль пока не стабилен')
    else:
        city = message.text.strip().lower()
        res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_API_key}&units=metric')
        if res.status_code == 200:
            weather = json.loads(res.text)
            bot.reply_to(message,
                         f'В городе {message.text} {weather["sys"]["country"]} {weather["weather"][0]["main"]}\n'
                         f'Температура {weather["main"]["temp"]} \n'
                         f'Ощущается как {weather["main"]["feels_like"]} \n'
                         f'Минимум {weather["main"]["temp_min"]} \n'
                         f'Максимум {weather["main"]["temp_max"]} \n'
                         f'Влажность {weather["main"]["humidity"]} \n'
                         f'Ветер {weather["wind"]["speed"]} \n')
        else:
            bot.reply_to(message, f'К сожалению я не знаю город {message.text}')



bot.polling(none_stop=True)
