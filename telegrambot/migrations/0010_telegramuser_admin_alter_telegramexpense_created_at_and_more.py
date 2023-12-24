# Generated by Django 4.2.7 on 2023-12-24 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('telegrambot', '0009_telegramuser_chart'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='admin',
            field=models.BooleanField(default=False, help_text='Указывает, является ли пользователь админом.', verbose_name='Админ'),
        ),
        migrations.AlterField(
            model_name='telegramexpense',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Временная метка, указывающая, когда был создан.', verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='telegramsupport',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='Временная метка, указывающая, когда был создан.', verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='telegramsupport',
            name='user',
            field=models.ForeignKey(help_text='Пользователь, которому принадлежит вопрос.', on_delete=django.db.models.deletion.CASCADE, to='telegrambot.telegramuser', verbose_name='Пользователь'),
        ),
        migrations.CreateModel(
            name='TelegramAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(help_text='Ответ на вопрос пользователя.', verbose_name='Ответ')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Временная метка, указывающая, когда был создан.', verbose_name='Создан')),
                ('admin_user', models.ForeignKey(help_text='Пользователь, которому выдана права администратора.', on_delete=django.db.models.deletion.CASCADE, to='telegrambot.telegramuser', verbose_name='Администратор')),
                ('questions', models.ForeignKey(help_text='Вопрос пользователя.', on_delete=django.db.models.deletion.CASCADE, to='telegrambot.telegramsupport', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Ответы на вопросы Telegram',
                'verbose_name_plural': 'Ответы на вопросы Telegram',
                'ordering': ['-created_at'],
            },
        ),
    ]