import telebot
from telebot import types
import requests
import json
from currency_converter import CurrencyConverter
import openai


about_bot = (
            'Привет, я Karich-Helper-Bot. Я могу сказать погоду на сутки, конвертировать валюты и учусь общаться. '
            'Чтобы узнать погоду в любом городе достаточно просто ввести его название. Чтобы произвести конвертацию '
            'валют просто спросите "какой курс" и я постараюсь вам помочь.')
weather_API_key = 'afca35e0a5606c9a045fa6592eb962cf'
converter_API_key = 'db5ffabf3cb94524b8157e43af4d8bb6'
open_AI_key = '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'
telebot_key = '6047133927:AAGghMLkgEJTkopYrSksrSmZzCRhsd_bKLE'


def recurs_reload():
    try:
        bot = telebot.TeleBot(telebot_key)
        converter = CurrencyConverter()
        openai.api_key = open_AI_key

        print('Bot Started...')

        @bot.message_handler(commands=['start', 'channels', 'sites', 'help'])
        def commands(message):
            if message.text == '/start':
                markup = types.ReplyKeyboardMarkup()
                btn1 = types.KeyboardButton('погода')
                btn2 = types.KeyboardButton('курсы валют')
                markup.row(btn1, btn2)
                bot.send_message(message.chat.id,
                                 f'Привет, {message.from_user.first_name} {message.from_user.last_name}',
                                 reply_markup=markup)
            elif message.text == '/channels' or message.text == '/sites':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Карыч', url='https://www.youtube.com/@user-cx5xi3xn7l'))
                markup.add(types.InlineKeyboardButton('Карыч Страйк', url='https://www.youtube.com/@user-wp5kq6xt8n'))
                bot.reply_to(message, 'Вот список каналов ', reply_markup=markup)
            elif message.text == '/help':
                bot.send_message(message.chat.id, about_bot)

        @bot.message_handler(content_types=['photo'])
        def get_photo(message):
            bot.reply_to(message, 'Красиво!')

        @bot.message_handler(content_types=['video'])
        def get_photo(message):
            bot.reply_to(message, 'Как интересно!')

        @bot.message_handler(content_types=['text'])
        def info(message):
            text = message.text.lower()
            if ' погод' in text or ' температур' in text:
                bot.send_message(message.chat.id, 'введите название города погода в котором вам интересна')
            elif 'как ' in text and ' дела' in text:
                bot.send_message(message.chat.id, 'Всегда всё хорошо. Спасибо что спросили.')
            elif ('расскажи' in text and 'себе' in text) or 'помощь' in text or 'подска' in text:
                bot.send_message(message.chat.id, about_bot)
            elif 'спасиб' in text or 'благодарю' in text:
                bot.send_message(message.chat.id, 'Обращайтесь, всегда рад быть полезен.')
            elif 'привет' in text or 'здравствуй' in text:
                bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}'
                                                  f' {message.from_user.last_name}.')
            elif 'пока' in text or 'всё ' in text:
                bot.send_message(message.chat.id, 'Всего хорошего.')
            elif (('курс' in text and 'валют' in text) or ('как' in text and 'курс' in text)
                  or ('конверт' in text and 'валют' in text)) or 'переведи' in text:
                bot.send_message(message.chat.id, 'Введите сумму которую хотите конвертировать')
                bot.register_next_step_handler(message, summa)
            elif ' сайт' in text or ' ютуб' in text or 'сайты' in text:
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Карыч', url='https://www.youtube.com/@user-cx5xi3xn7l'))
                markup.add(types.InlineKeyboardButton('Карыч Страйк', url='https://www.youtube.com/@user-wp5kq6xt8n'))
                bot.reply_to(message, 'Вот список каналов ', reply_markup=markup)
            else:
                city = message.text.strip().lower()
                res = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_API_key}&units=metric')
                if res.status_code == 200:
                    weather = json.loads(res.text)
                    bot.reply_to(message,
                                 f'В городе {message.text} {weather["sys"]["country"]} '
                                 f'{weather["weather"][0]["main"]}\n'
                                 f'Температура {weather["main"]["temp"]} \n'
                                 f'Ощущается как {weather["main"]["feels_like"]} \n'
                                 f'Минимум {weather["main"]["temp_min"]} \n'
                                 f'Максимум {weather["main"]["temp_max"]} \n'
                                 f'Влажность {weather["main"]["humidity"]} \n'
                                 f'Ветер {weather["wind"]["speed"]} \n')
                else:
                    if len(text.split(' ')) > 3:
                        try:
                            bot.reply_to(message, f'{generate_response(text)}')
                        except Exception as ex:
                            print(f'OpenAI API error - {ex} ON {text}')
                            bot.reply_to(message, f'Увы я пока не умею отвечать на это.')
                    else:
                        bot.reply_to(message, f'К сожалению я не знаю город {message.text}')

        @bot.callback_query_handler(func=lambda call: True)
        def callback(call):
            if 'else' in call.data:
                bot.send_message(call.message.chat.id, 'Снова введите сумму и укажите валюты для конвертации')
                bot.register_next_step_handler(call.message, my_currency)
            else:
                values = call.data.split('/')
                v1 = get_value_in_dollar(values[1])
                v2 = get_value_in_dollar(values[2])
                if len(values) == 3 and v1 > 0 and v2 > 0:
                    bot.send_message(call.message.chat.id, f'Получается {round(float(values[0]) / v1 * v2)}')
                else:
                    bot.send_message(call.message.chat.id, 'Не понимаю формат, повторите. Пример: 999.99 usd rub')
                    bot.register_next_step_handler(call.message, my_currency)

        def summa(message):
            try:
                amount = float(message.text.replace(',', '.').strip())
            except ValueError:
                bot.send_message(message.chat.id,
                                 'Не могу распознать число, введите сумму конвертируемой валюты повторно')
                bot.register_next_step_handler(message, summa)
                return
            if amount > 0:
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton('USD/RUB', callback_data=f'{amount}/USD/RUB')
                btn2 = types.InlineKeyboardButton('RUB/USD', callback_data=f'{amount}/RUB/USD')
                btn3 = types.InlineKeyboardButton('USD/UZS', callback_data=f'{amount}/USD/UZS')
                btn4 = types.InlineKeyboardButton('UZS/USD', callback_data=f'{amount}/UZS/USD')
                btn5 = types.InlineKeyboardButton('RUB/UZS', callback_data=f'{amount}/RUB/UZS')
                btn6 = types.InlineKeyboardButton('UZS/RUB', callback_data=f'{amount}/UZS/RUB')
                btn7 = types.InlineKeyboardButton('Другое', callback_data=f'{amount}/else')
                markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
                bot.send_message(message.chat.id, 'Выберите пару валют либо выберите ДРУГОЕ и введите свою',
                                 reply_markup=markup)
            else:
                bot.send_message(message.chat.id, f'Вы ввели {amount}, введите число > 0')
                bot.register_next_step_handler(message, summa)

        def generate_response(text):
            response = openai.Completion.create(
                prompt=text,
                engine='text-davinci-003',
                max_tokens=100,
                temperature=0.1,
                n=1,
                stop=['ответ от чата GPT-3.5'],
                timeout=7
            )
            return response

        def get_value_in_dollar(value):
            if value == 'USD':
                return 1
            else:
                try:
                    return converter.convert(1, 'USD', value)
                except Exception as convert_ex:
                    print(f'Converter API do not know {value}. Error {convert_ex}')
                    try:
                        data = requests.get(
                            f'https://openexchangerates.org/api/latest.json?app_id={converter_API_key}&base=USD'
                            f'&symbols={value}').json()
                        return data['rates'][value]
                    except Exception as request_ex:
                        print(f'Openexchangerates API do not know {value}. Error {request_ex}')
                        try:
                            data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
                            dollar = data['Valute']['USD']['Value']
                            if value == 'RUB':
                                print(f'1$ costs {dollar} in {value}')
                                return dollar
                            else:
                                return dollar / data['Valute'][value]['Value']
                        except Exception as request_ex:
                            print(f'Fatal converting error on {value}. Error - {request_ex}')
                            return -1

        def my_currency(message):
            values = message.text.upper().strip().split(' ')
            if len(values) == 3:
                v1 = get_value_in_dollar(values[1])
                v2 = get_value_in_dollar(values[2])
                if v1 > 0 and v2 > 0:
                    bot.send_message(message.chat.id, f'Получается {round(float(values[0]) / v1 * v2)}')
                else:
                    bot.send_message(message.chat.id, 'Не понимаю формат, повторите. Пример: 999.99 usd rub')
                    print(f'Incorrect format of {values}')
                    bot.register_next_step_handler(message, my_currency)
            else:
                bot.send_message(message.chat.id, 'Не понимаю формат, повторите. Пример: 999.99 usd rub')
                print(f'Incorrect format of {values}')
                bot.register_next_step_handler(message, my_currency)

        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        recurs_reload()


recurs_reload()
