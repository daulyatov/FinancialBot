import os
import matplotlib
import matplotlib.pyplot as plt
from django.conf import settings 
from telegrambot.models import TelegramUser, TelegramExpense, TelegramIncome
from datetime import datetime, timedelta

matplotlib.use("Agg")  

def userchart(user_id):
    tuser = TelegramUser.objects.get(user_id=user_id)

    # Найти первый и последний день текущего месяца
    today = datetime.now().date()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = (today.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)

    # Получить все расходы за текущий месяц
    expenses = TelegramExpense.objects.filter(user=tuser, date__range=[first_day_of_month, last_day_of_month])

    incomes = TelegramIncome.objects.filter(user=tuser).first()

    fruits = ["Расходы", "Баланс"]
    counts = [sum(expense.amount for expense in expenses), tuser.balance]

    plt.bar(fruits, counts)
    plt.title("График финансов!")

    temp_file_path = f"{tuser.user_id}_temp.png"
    plt.savefig(temp_file_path)

    with open(temp_file_path, "rb") as temp_file:
        tuser.chart.save(f"{tuser.user_id}.png", temp_file)
    plt.close()
    os.remove(temp_file_path)
    
    all_summa = counts[0] + counts[1]

    # Рассчитываем проценты относительно суммы расходов и баланса (исключая доходы)
    percent_expenses = (counts[0] / all_summa * 100) if all_summa else 0
    percent_balance = (counts[1] / all_summa * 100) if all_summa else 0

    return (
        f"<b>Расходы:</b> {counts[0]} ₸ | {round(percent_expenses, 2)}%\n"
        f"<b>Баланс:</b> {counts[1]} ₸ | {round(percent_balance, 2)}%\n"
    )
