import os

import cv2
import requests
from PIL import Image
from telebot import types
from bs4 import BeautifulSoup as bs
from http import HTTPStatus as H

import divination

bot = divination.bot

URL_SEARCH_PHOTO = os.getenv("URL_SEARCH_PHOTO")
URL_SEARCH_PHOTO_2 = os.getenv("URL_SEARCH_PHOTO_2")
URL_ANSWER = "Пришлите изображение."


@bot.message_handler(commands=['button'])
def choice_pixelate(message):
    mr = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bt1 = types.KeyboardButton("С сеткой")
    bt2 = types.KeyboardButton("Без сетки")
    mr.add(bt1, bt2)
    bot.send_message(message.chat.id, "С сеткой или без сетки?", reply_markup = mr)


def pixelate(image, draw_margin, pixel_size=9):
    margin_color = (0, 0, 0)
    image = image.resize((image.size[0] // pixel_size, image.size[1] // pixel_size), Image.NEAREST)
    image = image.resize((image.size[0] * pixel_size, image.size[1] * pixel_size), Image.NEAREST)
    pixel = image.load()

    if draw_margin:
        for i in range(0, image.size[0], pixel_size):
            for j in range(0, image.size[1], pixel_size):
                for r in range(pixel_size):
                    pixel[i+r, j] = margin_color
                    pixel[i, j+r] = margin_color
    return image


def menu_photo(message, name, item):
    if os.path.isfile(f"{name}.jpg"):
        #try:
        #    os.remove(f"{name}.jpg")
        #except PermissionError:
        #    os.close(f"{name}.jpg")
        os.remove(f"{name}.jpg")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    item10 = types.KeyboardButton("Изменить картинку")
    item11 = types.KeyboardButton("В меню")
    markup.add(item, item10, item11)
    bot.send_message(message.chat.id, "Продолжим?", reply_markup = markup)


def get_photo(message):
    name = message.from_user.username
    if message.content_type == "photo":
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"{name}.jpg", "wb") as new_file:
            new_file.write(downloaded_file)
        return f"{name}.jpg", name
    else:
        bot.send_message(message.chat.id, URL_ANSWER)
        return False


def get_search_photo(message):
    im = get_photo(message)
    item = types.KeyboardButton("Поиск по фото")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.username, item)
    else:
        f = open(im[0],'rb')
        try:
            files = {'upfile': ('blob', im[0], 'image/jpeg')}
            params = {'rpt': 'imageview', 'format': 'json', 'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
            r = requests.post(URL_SEARCH_PHOTO, params=params, files=files)
            query_string = r.json()['blocks'][0]['params']['url']
            img_search_url = URL_SEARCH_PHOTO + '?' + query_string
        except:
            files = {'encoded_image': (im[0], im[0]), 'image_content': ''}
            r = requests.post(URL_SEARCH_PHOTO_2, files=files, allow_redirects=False)
            html = bs(r.text, "html.parser")
            img_search_url = str(html.find_all("a")[0]).split('"')[1]
        bot.send_message(message.chat.id, img_search_url)
        f.close()
        menu_photo(message, im[1], item)


def get_photo_pixelate_True(message):
    get_photo_pixelate(message, True)


def get_photo_pixelate_False(message):
    get_photo_pixelate(message, False)


def get_photo_pixelate(message, draw_margin):
    im = get_photo(message)
    item = types.KeyboardButton("Пиксель арт")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.first_name, item)
    else:
        image_pixelate = pixelate(Image.open(im[0]), draw_margin)
        bot.send_photo(message.chat.id, image_pixelate)
        menu_photo(message, im[1], item)


def get_photo_grey(message):
    im = get_photo(message)
    item = types.KeyboardButton("50 оттенков серого")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.first_name, item)
    else:
        img_grey = cv2.imread(im[0], cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(im[0], img_grey)
        bot.send_photo(message.chat.id, Image.open(im[0]))
        menu_photo(message, im[1], item)


def get_photo_bw(message):
    im = get_photo(message)
    item = types.KeyboardButton("Сделать черно-белым")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.first_name, item)
    else:
        img_grey = cv2.imread(im[0], cv2.IMREAD_GRAYSCALE)
        img_binary = cv2.threshold(img_grey, 128, 255, 0)[1]
        cv2.imwrite(im[0], img_binary)
        bot.send_photo(message.chat.id, Image.open(im[0]))
        menu_photo(message, im[1], item)


def get_to_turn_90(message):
    im = get_photo(message)
    item = types.KeyboardButton("Повернуть на право")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.first_name, item)
    else:
        bot.send_photo(message.chat.id, Image.open(im[0]).transpose(Image.ROTATE_90))
        menu_photo(message, im[1], item)


def get_to_turn_180(message):
    im = get_photo(message)
    item = types.KeyboardButton("Перевернуть на 180")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.first_name, item)
    else:
        bot.send_photo(message.chat.id, Image.open(im[0]).transpose(Image.ROTATE_180))
        menu_photo(message, im[1], item)


def get_to_turn_270(message):
    im = get_photo(message)
    item = types.KeyboardButton("Повернуть на лево")
    if not im:
        bot.send_message(message.chat.id, URL_ANSWER)
        menu_photo(message, message.from_user.first_name, item)
    else:
        bot.send_photo(message.chat.id, Image.open(im[0]).transpose(Image.ROTATE_270))
        menu_photo(message, im[1], item)