import txt as txt
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import txt

button_yes = types.KeyboardButton('Да')
button_no = types.KeyboardButton('Нет')
button_hot = types.KeyboardButton('Горячий')
button_cold = types.KeyboardButton('Холодный')
buttons_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_1.add(button_yes, button_no)
buttons_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons_2.add(button_hot, button_cold)


def recipes(file: txt):
    dic={}
    with open(file, 'r', encoding="utf-8") as r_book:
        rec=r_book.read().split('\n\n\n')
        for i in range(len(rec)):
            name, recipe = rec[i].split("!\n\n")
            dic.update({name: recipe})
    return dic

def genmarkup(data: dict):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for cocktail in data:
        markup.add(InlineKeyboardButton(text=cocktail, callback_data=f'{cocktail}'))
    return markup


