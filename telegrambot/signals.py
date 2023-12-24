from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegrambot.models import TelegramUser, TelegramIncome, TelegramExpense, TelegramAnswers
from telegrambot.main import answer_message

@receiver(post_save, sender=TelegramUser)
def create_data(sender, instance, created, **kwargs):
    if created:
        TelegramIncome.objects.create(user=instance)
        TelegramExpense.objects.create(user=instance)
        

@receiver(post_save, sender=TelegramAnswers)
def create_answers(sender, instance, created, **kwargs):
    if created:
        answer_message(instance.questions.user, instance.questions.message, instance.answer)