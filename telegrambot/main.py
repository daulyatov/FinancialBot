import logging

import telebot
from telebot import types

from django.conf import settings
from telegrambot.models import TelegramUser, TelegramSupport, TelegramExpense, TelegramIncome

from telegrambot.keyboards import get_menu_keyboard, get_profile_keyboard, get_bank_keyboard

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


bot = telebot.TeleBot(settings.TOKENBOT, parse_mode="HTML")


@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    
    model_user, created = TelegramUser.objects.get_or_create(user_id=user.id)
    
    if created:
        model_user.user_id = user.id
        model_user.username = user.username
        model_user.first_name = user.first_name
        model_user.last_name = user.last_name
        model_user.language_code = user.language_code
        model_user.is_bot = user.is_bot
        model_user.save()

        logging.info(f'Был создан новый аккаунт {model_user.get_name()}')
    
    bot.send_message(message.chat.id, f"Привет, {model_user.get_name()}!", reply_markup=get_menu_keyboard())


@bot.message_handler(func=lambda message: message.text.lower() == "меню")
def menu(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    logging.info(f"Пользователь {model_user.get_name()} в меню.") 
    
    bot.send_message(message.chat.id, "Выберите нужную опцию:", reply_markup=get_menu_keyboard())
    return True


def get_photo_profile(message):
    user_id = message.from_user.id
    photos = bot.get_user_profile_photos(user_id, limit=1)

    if photos.photos:
        file_id = photos.photos[0][-1].file_id
        return file_id


@bot.message_handler(func=lambda message: message.text.lower() == "мой профиль")
def profile(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    user_profile = (
        f"<b>ID:</b> {model_user.user_id}\n"
        f"<b>Имя:</b> {model_user.first_name}\n"
        f"<b>Фамилия:</b> {model_user.last_name}\n"
        f"<b>Никнейм:</b> @{model_user.username}\n"
        f"<b>Код языка:</b> {model_user.language_code}\n"
        f"<b>Бот:</b> {'Да' if model_user.is_bot else 'Нет'}\n"
        f"\n"
        f"<b>Ваш баланс:</b> {model_user.balance} ₸"
    )
    logging.info(f"Пользователь {model_user.get_name()} в профиле.") 
    try:
        bot.send_photo(
            message.chat.id,
            photo=get_photo_profile(message),
            caption=user_profile,
            reply_markup=get_profile_keyboard()
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке фото: {e}!")
        bot.send_message(message.chat.id, user_profile, reply_markup=get_profile_keyboard())


def support_message(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    model_support = TelegramSupport.objects.create(user=model_user, message=message.text)
    logging.info(f"Пользователь {model_user.get_name()} отправил вопрос в поддержку.") 
    
    bot.send_message(message.chat.id, "Ваш вопрос отправлен в поддержку!", reply_markup=get_menu_keyboard())
    return True


@bot.message_handler(func=lambda message: message.text.lower() == "поддержка")
def support(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    logging.info(f"Пользователь {model_user.get_name()} в поддержке.") 
    
    bot.send_message(message.chat.id, "Введите ваш вопрос:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, support_message)


@bot.message_handler(func=lambda message: message.text.lower() == "мой банк")
def bank(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    user_bank = (
        f"<b>Ваш баланс:</b> {model_user.balance} ₸"
    )
    logging.info(f"Пользователь {model_user.get_name()} в банке.") 
    
    bot.send_message(message.chat.id, user_bank, reply_markup=get_bank_keyboard())


def add_balance_message(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    model_user_income = TelegramIncome.objects.get(user=model_user)
    
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Неверный формат суммы!", reply_markup=get_bank_keyboard())
        return False
    
    if int(message.text) <= 0:
        bot.send_message(message.chat.id, "Сумма должна быть больше нуля!", reply_markup=get_bank_keyboard())
        return False
    
    if int(message.text) > 1000000:
        bot.send_message(message.chat.id, "Сумма должна быть меньше 1 000 000!", reply_markup=get_bank_keyboard())
        return False
    
    model_user.balance += int(message.text)
    model_user_income.amount += int(message.text)
    model_user.save()
    model_user_income.save()
    
    logging.info(f"Пользователь {model_user.get_name()} пополнил баланс на {message.text} ₸.") 
    
    bot.send_message(message.chat.id, "Ваш баланс пополнен!", reply_markup=get_menu_keyboard())
    return True


@bot.message_handler(func=lambda message: message.text.lower() == "пополнить")
def add_balance(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    logging.info(f"Пользователь {model_user.get_name()} пополняет баланс.") 
    
    bot.send_message(message.chat.id, "Введите сумму:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, add_balance_message)



def RunBot():
    try:
        logger = logging.getLogger("RunBot")
        logger.info("Запуск бота!")
        bot.polling(none_stop=True, interval=0)
        
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}!")
        raise e
    
    except KeyboardInterrupt:
        logger.info("Бот остановлен принудительно!")
    
    finally:
        logger.info("Завершение работы бота!")