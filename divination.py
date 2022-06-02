import random


import requests
from telebot import types
from bs4 import BeautifulSoup as bs
from http import HTTPStatus as H

import main
import settings

bot = main.bot


@bot.message_handler(commands=['button'])
def menu_horoscopes(message):
    mr = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    bt = []
    for i in settings.BT_HOROSCOPE:
        bt.append(types.KeyboardButton(i))
    mr.add(*bt)
    bot.send_message(message.chat.id, "Что будем делать?", reply_markup = mr)


def horoscopes(message, zodiac):
    r = requests.get(settings.URL_HOROSCOPE + zodiac)
    if r.status_code != H.OK:
        bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")
        main.menu(message)
    else:
        html = bs(r.text, "html.parser")
        result = str(html.find_all('p')[0]).strip()
        bot.send_message(message.chat.id, result[3:-4])
        main.menu_divination(message)


def horoscopes_data_new(message):
    data = message.text
    if "," not in data and "." not in data:
        data = data.split(" ")
    elif "," in data:
        data = data.split(",")
    elif "." in data:
        data = data.split(".")
    if len(data) == 3:
        D, M, G = data
        D, M, G = int(D), int(M), int(G)
        try:
            data = str(D) + '.' + str(M) + '.' + str(G)
            r = requests.post(settings.URL_HOROSCOPE_DATA_NEW + data)
            if r.status_code != H.OK:
                bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")
                main.menu(message)
            else:
                html = bs(r.text, "html.parser")
                item = html.find_all('h3')
                items = html.find_all('p')
                for i in range(len(items)):
                    bot.send_message(message.chat.id, (
                        item[i].text + ":  " + items[i].text))
        except:
            bot.send_message(message.chat.id, "Неправильно введена дата")
            main.menu_divination(message)


def horoscopes_data(message):
    data = message.text
    if "," not in data and "." not in data:
        data = data.split(" ")
    elif "," in data:
        data = data.split(",")
    elif "." in data:
        data = data.split(".")
    if len(data) == 3:
        D, M, G = data
        D, M, G = int(D), int(M), int(G)
        try:
            r = requests.get(settings.URL_HOROSCOPE_DATA + f'{D}-{settings.MONTH[M]}-{G}-god')
            if r.status_code != H.OK:
                bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")
                main.menu(message)
            else:
                html = bs(r.text, "html.parser")
                result = html.find_all('p')
                if len(result) >= 9:
                    count = 1
                    for itm in result:
                        itm = str(itm)[3:-4].strip()
                        if "<" not in itm and "&gt;" not in itm  and "id" not in itm:
                            bot.send_message(message.chat.id, (settings.CHRT[count] + " " + itm))
                            count += 1
                        if count == 9:
                            break
                    main.menu_divination(message)
                else:
                    bot.send_message(message.chat.id, "Неправильно введена дата")
                    main.menu_divination(message)
        except:
            bot.send_message(message.chat.id, "Неправильно введена дата")
            main.menu_divination(message)
    else:
        bot.send_message(message.chat.id, "Формат даты должен быть такой (1.1.2000)")
        main.menu_divination(message)


def book(message):
    url = "https://kartaslov.ru/предложения-со-словом/"
    if len(message.text.strip().split(' ')) > 1:
        t = message.text.strip().replace(" ", "+")
        r = requests.get(url + t)
    else:
        r = requests.get(url + message.text)
    if r.status_code != H.OK:
        bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")
        main.menu(message)
    else:
        html = bs(r.text, "html.parser")
        items = html.find_all('div', class_='v2-sentence-box')
        if len(items):
            result = random.choice(items).text.split('.')[0].strip()
            bot.send_message(message.chat.id, result)
            main.menu_divination(message)
        else:
            bot.send_message(message.chat.id, "Такого слова у нас нет")
            main.menu_divination(message)