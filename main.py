import logging
import os
import random

import thecolorapi
from bs4 import BeautifulSoup as bs
from http import HTTPStatus as H

import requests
import telebot
from dotenv import load_dotenv
from PIL import Image
from telebot import types

import generate_img
import divination
import settings

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
URL_COLOR = os.getenv("URL_COLOR")

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать, {0.first_name}!\nЯ — <b>{1.first_name}</b>, "
        "бот созданный в развлекательных целях, который не несет "
        "смысловой нагрузки.".format(message.from_user, bot.get_me()),
        parse_mode = "html")
    menu(message)


@bot.message_handler(commands=['button'])
def menu(message):
    mr = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item2 = types.KeyboardButton("Бросить монетку")
    item3 = types.KeyboardButton("Получить цвет RGB")
    item4 = types.KeyboardButton("Поиск по фото")
    item5 = types.KeyboardButton("Изменить картинку")
    item6 = types.KeyboardButton("Гадание")
    item7 = types.KeyboardButton("Рандомное аниме")
    item8 = types.KeyboardButton("Рандомная дорама")
    mr.add(types.KeyboardButton("Получить рандомный пароль"))
    mr.add(item2, item4)
    mr.add(item3, item5)
    mr.add(item6, item7)
    mr.add(item8)
    mr.add(types.KeyboardButton("Найти рандомное кино по жанру"))
    bot.send_message(message.chat.id, "Что будем делать?", reply_markup = mr)


@bot.message_handler(commands=['button'])
def menu_divination(message):
    mr = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Загадать слово")
    btn2 = types.KeyboardButton("Гороскоп")
    btn3 = types.KeyboardButton("По дате рождения")
    #btn5 = types.KeyboardButton("50 оттенков серого")
    #btn6 = types.KeyboardButton("Сделать черно-белым")
    btn7 = types.KeyboardButton("В меню")
    mr.add(btn1, btn2)
    mr.add(btn3)
    mr.add(types.KeyboardButton("По дате рождения (новый вариант)"))
    #mr.add(btn5, btn6)
    mr.add(btn7)
    bot.send_message(message.chat.id, "Что будем делать?", reply_markup = mr)


@bot.message_handler(commands=['button'])
def menu_genre_movies(message):
    mr = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    bt = []
    for i in settings.BT_MOVIES:
        bt.append(types.KeyboardButton(i))
    mr.add(*bt)
    bot.send_message(message.chat.id, "Что будем искать?", reply_markup = mr)


@bot.message_handler(commands=['button'])
def menu_edit_photo(message):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("Повернуть на лево")
    btn2 = types.KeyboardButton("Перевернуть на 180")
    btn3 = types.KeyboardButton("Повернуть на право")
    btn4 = types.KeyboardButton("Пиксель арт")
    btn5 = types.KeyboardButton("50 оттенков серого")
    btn6 = types.KeyboardButton("Сделать черно-белым")
    btn7 = types.KeyboardButton("В меню")
    markup1.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(
        message.chat.id, "Что будем делать?", reply_markup = markup1
    )


@bot.message_handler(commands=['button'])
def menu_choice(message, item):
    markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item11 = types.KeyboardButton("В меню")
    markup3.add(item, item11)
    bot.send_message(message.chat.id, "Продолжим?", reply_markup = markup3)


@bot.message_handler(content_types=['text'])
def answer_markup(message):
    url_send = "Отправьте картинку"
    if message.text in ("Меню", "меню", "Menu", "menu", "В меню"):
        menu(message)
    elif message.text == "Получить рандомный пароль":
        mr = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mr.add(types.KeyboardButton("19"))
        text = "Введите длинну пароля (не больше 100)."
        sent = bot.reply_to(message, text, reply_markup = mr)
        bot.register_next_step_handler(sent, generate_password)
    elif message.text == "Получить цвет RGB":
        sent = bot.reply_to(
            message,
            "Введите цвет в формате RGB, три цифры через запятую от 0 до 255, например так "
            "'255, 255, 255' или HEX номер, пример: '#158f2b', решетка в начале не обязательна."
        )
        bot.register_next_step_handler(sent, create_photo)
    elif message.text == "Изменить картинку":
        menu_edit_photo(message)
    elif message.text == "Гадание":
        menu_divination(message)
    elif message.text == "Гороскоп":
        divination.menu_horoscopes(message)
    elif message.text in settings.ZODIAC:
        divination.horoscopes(message, settings.ZODIAC[message.text])
    elif message.text == "По дате рождения":
        sent = bot.reply_to(message, "Введи дату рождения целиком, (например: 1.1.1991)")
        bot.register_next_step_handler(sent, divination.horoscopes_data)
    elif message.text == "По дате рождения (новый вариант)":
        sent = bot.reply_to(message, "Введи дату рождения целиком, (например: 1.1.1991)")
        bot.register_next_step_handler(sent, divination.horoscopes_data_new)
    elif message.text == "Бросить монетку":
        mr = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mr.add(types.KeyboardButton("1"))
        text = "Сколько раз бросить монетку? (не больше 1000)."
        sent = bot.reply_to(message, text, reply_markup = mr)
        bot.register_next_step_handler(sent, toss_a_coin)
    elif message.text == "Найти рандомное кино по жанру":
        menu_genre_movies(message)
    elif message.text == "Поиск по фото":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_search_photo)
    elif message.text == "Повернуть на лево":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_to_turn_90)
    elif message.text == "Перевернуть на 180":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_to_turn_180)
    elif message.text == "Повернуть на право":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_to_turn_270)
    elif message.text == "Пиксель арт":
        generate_img.choice_pixelate(message)
    elif message.text == "С сеткой":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_photo_pixelate_True)
    elif message.text == "Без сетки":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_photo_pixelate_False)
    elif message.text == "50 оттенков серого":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_photo_grey)
    elif message.text == "Сделать черно-белым":
        bot.register_next_step_handler(bot.reply_to(
            message, url_send), generate_img.get_photo_bw)
    elif message.text == "Загадать слово":
        sent = bot.reply_to(
            message,
            "Гадание по слову, введите слово и "
            "если оно есть, придет предсказание."
        )
        bot.register_next_step_handler(sent, divination.book)
    elif message.text == "Рандомная дорама":
        get_doramy(message)
    elif message.text == "Рандомное аниме":
        get_anime(message)
    elif message.text in settings.MOVIES_GENRE:
        movies(message, settings.MOVIES_GENRE[message.text])
    elif message.text == "Мне повезет":
        movies(message, random.choice(list(settings.MOVIES_GENRE.values())))


def get_doramy(message):
    r = requests.get('https://doramy.club')
    if r.status_code == H.OK:
        page_num = int(bs(r.text, "html.parser").find_all('a', class_='page-numbers')[-2].text)
        r = requests.get(settings.URL_DORAMY.format(random.randrange(1, page_num + 1)))
        if r.status_code == H.OK:
            html = bs(r.text, "html.parser")
            item = random.choice(html.find_all('div', class_='post-home'))
            name = item.text.strip().split("\n")[0]
            name_em = item.text.strip().split("\n")[1]
            link = str(item.find_all('a')[0]).split('"')[1]
            bot.send_message(
                message.chat.id, "{0}\n{1}\n{2}".format(name, name_em, link), parse_mode = "html"
            )
            menu(message)
        else:
            bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")
    else:
        bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")


def get_anime(message):
    r = requests.get("https://animego.org/anime/random")
    a = requests.get("https://yummyanime.tv/random")
    if r.status_code == H.OK:
        html = bs(r.text, "html.parser")
        items = html.find_all('div', class_='anime-title')
        name1 = items[0].find_all('h1')[0].text
        name2 = items[0].find_all('li')[0].text
        link = str(html.find_all('meta')[7]).split('"')[1]
        bot.send_message(
            message.chat.id, "{0}\n{1}\n{2}".format(name1, name2, link), parse_mode = "html"
        )
        menu(message)
    elif a.status_code == H.OK:
        html = bs(a.text, "html.parser")
        name1 = html.find_all('div', class_='inner-page__title')[0].text
        name2 = html.find_all('div', class_='inner-page__subtitle')[0].text
        link = str(html.find_all('link')[1]).split('"')[1]
        bot.send_message(
            message.chat.id, "{0}\n{1}\n{2}".format(name1, name2, link), parse_mode = "html"
        )
        menu(message)
    else:
        bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")


def movies(message, genre):
    url = settings.URL.format(genre)
    r = requests.get(url + str(random.randrange(1, 300)))
    if r.status_code != H.OK:
        bot.send_message(message.chat.id, "Сервис временно недоступен, попробуйте позже.")
        movies(message, genre)
    else:
        html = bs(r.text, "html.parser")
        items = html.find_all('a', class_='nbl-slimPosterBlock')
    
        if (len(items)):
            url =  items[random.randrange(len(items))]
            it = str(url).split('class="nbl-slimPosterBlock__title">')[-1]
            name = it.split('</div>')[0]
            if '[4k]' in name:
                name = name[4:].strip()
            bot.send_message(message.chat.id, name)
            bot.send_message(message.chat.id, settings.URL_R.format(url['href']))
        else:
            logging.error("Фильм не найден.")
            movies(message, genre)


def generate_password(message):
    message_to_save = message.text
    if message_to_save.isdigit():
        message_to_save = int(message_to_save)
        if message_to_save > 99:
            sent = bot.reply_to(message, "Введите длинну пароля (не больше 100).")
            bot.register_next_step_handler(sent, generate_password)
        else:
            result = []
            for _ in range(3):
                item = ""
                count = 0
                for i in range(message_to_save):
                    if count == 4 and i != message_to_save - 1:
                        item += "-"
                        count = 0
                    else:
                        value = random.choice(settings.VARIABLES)
                        item += random.choice(value)
                        count += 1
                result.append(item)
                count = 0
            for i in range(len(result)):
                bot.send_message(message.chat.id, result[i])
            item = types.KeyboardButton("Получить рандомный пароль")
            menu_choice(message, item)
    else:
        sent = bot.reply_to(message, "Укажите длиннулину пароля в цифрах.")
        bot.register_next_step_handler(sent, generate_password)


def toss_a_coin(message):
    message_to_save = message.text
    if message_to_save == '':
        message_to_save == 1
    if message_to_save.isdigit():
        message_to_save = int(message_to_save)
        if message_to_save > 1000:
            sent = bot.reply_to(message, "Укажите количество бросков не больше 1000.")
            bot.register_next_step_handler(sent, toss_a_coin)
        else:
            YES = 0
            NO = 0
            for _ in range(message_to_save):
                n = random.choice([0, 1])
                if n == 0:
                    NO += 1
                else:
                    YES += 1
            if message_to_save > 1:
                bot.send_message(message.chat.id, "Орел: {0} Решка: {1}".format(YES, NO))
            elif YES == 0:
                bot.send_message(message.chat.id, "Решка")
            elif NO == 0:
                bot.send_message(message.chat.id, "Орел")
            item = types.KeyboardButton("Бросить монетку")
            menu_choice(message, item)
    else:
        sent = bot.reply_to(message, "Укажите количество бросков в цифрах.")
        bot.register_next_step_handler(sent, toss_a_coin)


def create_photo(message):
    num = message.text
    text_rgb = "Введите три цифры через запятую или HEX номер (решетка в начале не обязательна)."
    if "," in num or "." in num or " " in num.strip():
        if "," not in num and "." not in num:
            num = num.split(" ")
        elif "," in num:
            num = num.split(",")
        elif "." in num:
            num = num.split(".")
        if len(num) == 3:
            R, G, B = num
            R, G, B = R.strip(), G.strip(), B.strip()
            if R.isdigit() and G.isdigit() and B.isdigit():
                R, G, B = int(R), int(G), int(B)
                if R > 255 or G > 255 or B > 255:
                    bot.send_message(message.chat.id, "В RGB не может быть значений больше 255.")
                    menu_choice(message, types.KeyboardButton("Получить цвет RGB"))
                else:
                    try:
                        new_img = Image.new('RGB', (500, 500), (R, G, B))
                        color = thecolorapi.color(rgb=(R, G, B))
                        bot.send_message(message.chat.id, color.name)
                        bot.send_message(message.chat.id, color.hex_clean)
                        bot.send_photo(message.chat.id, new_img)
                        menu_choice(message, types.KeyboardButton("Получить цвет RGB"))
                    except ValueError:
                        bot.send_message(message.chat.id, text_rgb)
                        menu_choice(message, types.KeyboardButton("Получить цвет RGB"))
            else:
                bot.send_message(message.chat.id, text_rgb)
                menu_choice(message, types.KeyboardButton("Получить цвет RGB"))
        else:
            bot.send_message(message.chat.id, text_rgb)
            menu_choice(message, types.KeyboardButton("Получить цвет RGB"))
    else:
        try:
            num = num.strip()
            if num[0] != '#':
                num = '#' + num
            color = thecolorapi.color(hex=num)
            new_img = Image.new('RGB', (500, 500), color.rgb)
            bot.send_message(message.chat.id, color.name)
            bot.send_message(message.chat.id, color.rgb)
            bot.send_photo(message.chat.id, new_img)
            menu_choice(message, types.KeyboardButton("Получить цвет RGB"))
        except:
            bot.send_message(message.chat.id, text_rgb)
            menu_choice(message, types.KeyboardButton("Получить цвет RGB"))


if __name__ == '__main__':
     bot.infinity_polling()
