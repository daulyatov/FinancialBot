# Generated by Django 4.2.7 on 2023-12-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Дата и время создания записи в балансе.', verbose_name='Дата создания'),
        ),
    ]