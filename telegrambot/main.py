import logging
import telebot
from telebot import types
from datetime import datetime, timedelta


from django.conf import settings
from telegrambot.models import TelegramUser, TelegramSupport, TelegramExpense, TelegramIncome, TelegramAnswers, Category
from telegrambot.chart import userchart

from django.core.exceptions import ObjectDoesNotExist

from telegrambot.keyboards import get_menu_keyboard, get_profile_keyboard, get_bank_keyboard, get_cancel_keyboard,get_expenses_keyboard

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup



logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


bot = telebot.TeleBot(settings.TOKENBOT, parse_mode="HTML")


@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    
    model_user, created = TelegramUser.objects.get_or_create(user_id=user.id)
    userchart(model_user.user_id)
    
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


@bot.message_handler(func=lambda message: message.text.lower() == "мой банк")
def bank(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    user_bank = ("Выберите действие:")
    logging.info(f"Пользователь {model_user.get_name()} в банке.") 
    
    bot.send_message(message.chat.id, user_bank, reply_markup=get_bank_keyboard())



# Функция, которая возвращает описание бота
def get_about_text():
    return (
        "Этот бот создан для управления финансами. В нем вы можете записывать свои доходы и расходы,"
        "а так же смотреть статистику расходов и доходов в графике и отправлять графики своих финансов другим пользователям."
    )


@bot.message_handler(func=lambda message: message.text.lower() == "о боте")
def handle_about(message):
    about_text = get_about_text()
    bot.send_message(message.chat.id, about_text)


@bot.message_handler(func=lambda message: message.text.lower() == "пополнить")
def add_balance(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    
    logging.info(f"Пользователь {model_user.get_name()} пополняет баланс.") 
    
    # Используем клавиатуру отмены
    cancel_keyboard = get_cancel_keyboard()

    bot.send_message(message.chat.id, "Введите сумму:", reply_markup=cancel_keyboard)
    bot.register_next_step_handler(message, add_balance_message)


def add_balance_message(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    model_user_income = TelegramIncome.objects.get(user=model_user)

    # Используем клавиатуру отмены
    cancel_keyboard = get_cancel_keyboard()

    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, "Действие отменено.", reply_markup=get_bank_keyboard())
        return

    # Проверяем, что введенная сумма - число
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Неверный формат суммы. Повторите попытку.", reply_markup=cancel_keyboard)
        # Просим ввести сумму заново
        bot.register_next_step_handler(message, add_balance_message)
        return

    if int(message.text) <= 0:
        bot.send_message(message.chat.id, "Сумма должна быть больше нуля!", reply_markup=cancel_keyboard)
        bot.register_next_step_handler(message, add_balance_message)
        return
    
    if int(message.text) > 1000000:
        bot.send_message(message.chat.id, "Сумма должна быть меньше 1 000 000!", reply_markup=cancel_keyboard)
        bot.register_next_step_handler(message, add_balance_message)
        return
    
    # Пополняем баланс
    model_user.balance += int(message.text)
    model_user_income.amount += int(message.text)
    model_user.save()
    model_user_income.save()

    logging.info(f"Баланс пользователя {model_user.get_name()} увеличен на {message.text} ₸.")

    # Отправляем подтверждение и возвращаемся в меню
    bot.send_message(
        message.chat.id,
        f"Баланс успешно пополнен на {message.text} ₸. Новый баланс: {model_user.balance} ₸.",
        reply_markup=get_bank_keyboard()
    )



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

    cancel_keyboard = get_cancel_keyboard()

     # Если пользователь нажал "Отмена", возвращаемся в меню
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, "Действие отменнено", reply_markup=get_menu_keyboard())
        return
    
    bot.send_message(message.chat.id, "Введите ваш вопрос:", reply_markup=cancel_keyboard)
    bot.register_next_step_handler(message, support_message)


def answer_message(model_user, questions, answer):
    text = (
        f"Привет {model_user.get_name()}!\n"
        f"Администраторы ответили на ваш вопрос \n'{questions}'\n\n"
        f"Ответ: {answer}"
    )
    bot.send_message(model_user.user_id, text=text, reply_markup=get_menu_keyboard())
    return




@bot.message_handler(func=lambda message: message.text.lower() == "график")
def chart(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    logging.info(f"Пользователь {model_user.get_name()} запросил график.") 
    
    contecx = userchart(model_user.user_id)
    
    if model_user.chart and model_user.chart.path:
        # Отправляем график только если файл существует
        bot.send_photo(message.chat.id, open(model_user.chart.path, "rb"), caption=contecx, reply_markup=get_bank_keyboard())
    else:
        # Обработка случая, когда файл отсутствует
        bot.send_message(message.chat.id, "Извините, у вас нет сохраненного графика.")


@bot.message_handler(func=lambda message: message.text.lower() == "доходы")
def monthly_income(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    logging.info(f"Пользователь {model_user.get_name()} смотрит доходы.") 

    # Получаем текущую дату
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Корректируем месяц для обработки декабря
    next_month = current_month + 1
    next_year = current_year

    if next_month > 12:
        next_month = 1
        next_year += 1

    # Вычисляем последний день месяца
    last_day_of_month = datetime(next_year, next_month, 1) - timedelta(days=1)

    # Получаем записи доходов за текущий месяц
    incomes = TelegramIncome.objects.filter(
        user=model_user,
        created_at__gte=datetime(current_year, current_month, 1),
        created_at__lte=last_day_of_month
    )

    total_income = sum(income.amount for income in incomes)

    response = (
        f"<b>Доход за месяц {now.strftime('%B %Y')}:</b>\n"
        f"<b>Общий доход:</b> {total_income} ₸"
    )

    bot.send_message(message.chat.id, response, reply_markup=get_bank_keyboard())
    return True



@bot.message_handler(func=lambda message: message.text.lower() == "расходы")
def expenses(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)
    
    logging.info(f"Пользователь {model_user.get_name()} в расходах.") 

    bot.send_message(message.chat.id, "Выберите действие", reply_markup=get_expenses_keyboard())
    return True
 


MAX_CATEGORIES = 6  # Maximum number of categories a user can create

@bot.message_handler(func=lambda message: message.text.lower() == "добавить категорию")
def add_category(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)

    logging.info(f"Пользователь {model_user.get_name()} добавляет категорию.")

    cancel_keyboard = get_cancel_keyboard()

    # Check if the user has reached the maximum number of categories
    existing_categories_count = Category.objects.filter(user=model_user).count()
    if existing_categories_count >= MAX_CATEGORIES:
        bot.send_message(message.chat.id, f"Достигнуто максимальное количество категорий ({MAX_CATEGORIES}).", reply_markup=get_expenses_keyboard())
        return

    bot.send_message(message.chat.id, "Введите название новой категории:", reply_markup=cancel_keyboard)
    bot.register_next_step_handler(message, add_category_message)

def add_category_message(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)

    # Check if the message is "отмена" to cancel the operation
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, "Добавление категории отменено.", reply_markup=get_expenses_keyboard())
        return

    # Check if the user has reached the maximum number of categories
    existing_categories_count = Category.objects.filter(user=model_user).count()
    if existing_categories_count >= MAX_CATEGORIES:
        bot.send_message(message.chat.id, f"Достигнуто максимальное количество категорий ({MAX_CATEGORIES}).", reply_markup=get_expenses_keyboard())
        return

    # Check if the category already exists for the user
    if Category.objects.filter(user=model_user, name=message.text).exists():
        bot.send_message(message.chat.id, f"Категория '{message.text}' уже существует. Введите другое название.", reply_markup=get_cancel_keyboard())
        bot.register_next_step_handler(message, add_category_message)
        return

    # Create a new category with the provided name
    new_category = Category(user=model_user, name=message.text)
    new_category.save()

    logging.info(f"Добавлена новая категория: {new_category.name}.")

    # Send confirmation message and return to the main menu
    bot.send_message(
        message.chat.id,
        f"Категория '{new_category.name}' успешно добавлена.",
        reply_markup=get_expenses_keyboard()
    )
    return True




@bot.message_handler(func=lambda message: message.text.lower() == "удалить категорию")
def delete_category(message):
    user = message.from_user
    model_user = TelegramUser.objects.get(user_id=user.id)

    cancel_keyboard = get_cancel_keyboard()

    logging.info(f"Пользователь {model_user.get_name()} удаляет категорию.")

    bot.send_message(message.chat.id, "Введите название категории, которую вы хотите удалить:", reply_markup=cancel_keyboard)


     # Если пользователь нажал "Отмена", возвращаемся в меню
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, "Действие отменнено", reply_markup=cancel_keyboard)
        return

    bot.register_next_step_handler(message, delete_category_message)

def delete_category_message(message):
    user = message.from_user

    # Check if the message is "отмена" to cancel the operation
    if message.text.lower() == "отмена":
        bot.send_message(message.chat.id, "Удаление категории отменено.", reply_markup=get_expenses_keyboard())
        return

    # Check if the category exists
    try:
        category_to_delete = Category.objects.get(name=message.text)
    except Category.DoesNotExist:
        bot.send_message(message.chat.id, f"Категории '{message.text}' не существует. Пожалуйста, введите корректное название категории.", reply_markup=get_cancel_keyboard())
        bot.register_next_step_handler(message, delete_category_message)  # Register next step to try again
        return

    # Delete the category
    category_to_delete.delete()

    logging.info(f"Категория '{category_to_delete.name}' удалена.")

    # Send confirmation message and return to the main menu
    bot.send_message(
        message.chat.id,
        f"Категория '{category_to_delete.name}' успешно удалена.",
        reply_markup=get_bank_keyboard()
    )
    return True


@bot.message_handler(func=lambda message: message.text.lower() == "показать категории")
def show_categories(message):
    categories = Category.objects.all()

    if categories:
        categories_list = "\n".join(category.name for category in categories)
        bot.send_message(message.chat.id, f"Существующие категории:\n{categories_list}", reply_markup=get_expenses_keyboard())
    else:
        bot.send_message(message.chat.id, "Нет сохранённых категорий.")

    return True




@bot.message_handler(func=lambda message: message.text.lower() == "добавить расход")
def record_expense_step1(message):
    try:
        user = message.from_user
        model_user = TelegramUser.objects.get(user_id=user.id)

        # Используем клавиатуру отмены
        cancel_keyboard = get_cancel_keyboard()

        logging.info(f"Пользователь {model_user.get_name()} начал запись расходов.")

        # Проверяем, есть ли категории
        categories = Category.objects.all()

        if not categories:
            bot.send_message(message.chat.id, "Отсутствуют категории. Пожалуйста, добавьте категорию перед записью расхода.", reply_markup=get_expenses_keyboard())
            return

        # Получаем список названий категорий
        category_names = [category.name for category in categories]

        # Отправляем сообщение с предложением выбрать категорию
        markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        category_buttons = [types.KeyboardButton(name) for name in category_names]
        markup.add(*category_buttons)

        bot.send_message(message.chat.id, "Выберите категорию расхода:", reply_markup=markup)
        bot.register_next_step_handler(message, lambda m: record_expense_step2(m, model_user))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}. Повторите попытку.", reply_markup=cancel_keyboard)
        logging.error(f"Ошибка при начале записи расходов: {e}")
        # Заново регистрируем текущий обработчик
        bot.register_next_step_handler(message, record_expense_step1)

def record_expense_step2(message, user):
    try:
        # Check if the selected category is valid
        selected_category_name = message.text
        selected_category = Category.objects.get(name=selected_category_name)

        # Используем клавиатуру отмены
        cancel_keyboard = get_cancel_keyboard()

        # Проверяем баланс пользователя
        if user.balance <= 0:
            bot.send_message(message.chat.id, "На вашем балансе 0. Пополните баланс и повторите попытку.", reply_markup=get_bank_keyboard())
            return

        bot.send_message(message.chat.id, "Введите сумму расхода:", reply_markup=cancel_keyboard)
        bot.register_next_step_handler(message, lambda m: record_expense_step3(m, user, selected_category))

    except Category.DoesNotExist:
        bot.send_message(message.chat.id, "Выбранная категория не существует. Пожалуйста, выберите существующую категорию.", reply_markup=cancel_keyboard)
        bot.register_next_step_handler(message, lambda m: record_expense_step2(m, user))

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}. Повторите попытку.", reply_markup=cancel_keyboard)
        logging.error(f"Ошибка при выборе категории расхода: {e}")
        # Заново регистрируем текущий обработчик
        bot.register_next_step_handler(message, lambda m: record_expense_step2(m, user))

def record_expense_step3(message, user, selected_category):
    try:
        # Check if the entered amount is a valid positive integer
        while True:
            # Используем клавиатуру отмены
            cancel_keyboard = get_cancel_keyboard()

            # Если пользователь нажал "Отмена", возвращаемся в меню
            if message.text.lower() == "отмена":
                bot.send_message(message.chat.id, "Действие отменено.", reply_markup=get_bank_keyboard())
                return

            if not message.text.isdigit():
                bot.send_message(message.chat.id, "Неверный формат суммы расхода. Повторите попытку.", reply_markup=cancel_keyboard)
                # Просим ввести сумму заново
                bot.register_next_step_handler(message, lambda m: record_expense_step3(m, user, selected_category))
                return

            amount = int(message.text)

            # Check if the user has enough balance
            if amount <= 0:
                bot.send_message(message.chat.id, "Сумма должна быть больше нуля. Повторите попытку.", reply_markup=cancel_keyboard)
                # Просим ввести сумму заново
                bot.register_next_step_handler(message, lambda m: record_expense_step3(m, user, selected_category))
                return

            if amount > user.balance:
                bot.send_message(message.chat.id, "У вас недостаточно средств для совершения расхода, повторите попытку или пополните баланс.", reply_markup=get_expenses_keyboard())
                # Просим ввести сумму заново
                return

            # Save the expense with the selected category
            TelegramExpense.objects.create(user=user, amount=amount, category=selected_category)

            # Update the user's balance
            user.balance -= amount
            user.save()

            logging.info(f"Пользователь {user.get_name()} записал расход на {amount} ₸ в категории '{selected_category.name}'.")

            # Send confirmation and return to the main menu
            bot.send_message(
                message.chat.id,
                f"Расход в размере {amount} ₸ успешно записан в категории '{selected_category.name}'. Новый баланс: {user.balance} ₸.",
                reply_markup=get_expenses_keyboard()
            )
            return

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}. Повторите попытку.", reply_markup=cancel_keyboard)
        logging.error(f"Ошибка при записи расхода: {e}")
        # Заново регистрируем текущий обработчик
        bot.register_next_step_handler(message, lambda m: record_expense_step3(m, user, selected_category))



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