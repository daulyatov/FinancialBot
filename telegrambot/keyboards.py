from telebot import types


def get_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = types.KeyboardButton("Мой профиль")
    btn2 = types.KeyboardButton("Поддержка")
    btn3 = types.KeyboardButton("О боте")
    
    keyboard.row(btn1, btn2)
    keyboard.row(btn3)
    
    return keyboard


def get_profile_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = types.KeyboardButton("Мой банк")
    btn2 = types.KeyboardButton("Меню")
    
    keyboard.row(btn1)
    keyboard.row(btn2)
    
    return keyboard


def get_bank_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn1 = types.KeyboardButton("Пополнить")
    btn2 = types.KeyboardButton("Перевод")
    btn3 = types.KeyboardButton("Доходы")
    btn4 = types.KeyboardButton("Расходы")
    btn5 = types.KeyboardButton("График")
    btn6 = types.KeyboardButton("Меню")
    
    keyboard.row(btn1, btn2)
    keyboard.row(btn3, btn4)
    keyboard.row(btn5)
    keyboard.row(btn6)
    
    return keyboard