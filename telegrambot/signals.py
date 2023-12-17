from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegrambot.models import TelegramUser, TelegramIncome, TelegramExpense


@receiver(post_save, sender=TelegramUser)
def create_data(sender, instance, created, **kwargs):
    if created:
        TelegramIncome.objects.create(user=instance)
        TelegramExpense.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_data(sender, instance, **kwargs):
    instance.telegramuser.save()
    instance.telegramincome.save()
    instance.telegramexpense.save()
    instance.save()