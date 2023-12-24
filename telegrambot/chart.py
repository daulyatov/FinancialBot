import os
import matplotlib.pyplot as plt
from django.conf import settings 
from telegrambot.models import TelegramUser, TelegramExpense, TelegramIncome


def userchart(user_id):
    tuser = TelegramUser.objects.get(user_id=user_id)
    expenses = TelegramExpense.objects.get(user=tuser)
    incomes = TelegramIncome.objects.get(user=tuser)

    fruits = ["Расходы", "Баланс", "Доходы"]
    counts = [expenses.amount, tuser.balance, incomes.amount]
    plt.bar(fruits, counts)
    plt.title("График финансов!")

    temp_file_path = f"{tuser.user_id}_temp.png"
    plt.savefig(temp_file_path)

    with open(temp_file_path, "rb") as temp_file:
        tuser.chart.save(f"{tuser.user_id}.png", temp_file)
    plt.close()
    os.remove(temp_file_path)
    
    
    all_summa = sum([expenses.amount, tuser.balance])
    return (
        f"<b>Расходы:</b> {expenses.amount} ₸ | {round(expenses.amount / all_summa * 100, 2) if all_summa else 0}%\n"
        f"<b>Баланс:</b> {tuser.balance} ₸ | {round(tuser.balance / all_summa * 100, 2) if all_summa else 0}%\n"
        f"<b>Доходы:</b> {incomes.amount} ₸\n"
    )


