from django.db import models


class TelegramUser(models.Model):
    user_id = models.BigIntegerField(
        unique=True,
        verbose_name="ID пользователя",
        help_text="Уникальный идентификатор пользователя в Telegram.",
    )
    username = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя пользователя",
        help_text="Имя пользователя в Telegram.",
    )
    first_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя",
        help_text="Имя пользователя в Telegram.",
    )
    last_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Фамилия пользователя в Telegram.",
    )
    language_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Код языка",
        help_text="Код языка, используемый пользователем в Telegram.",
    )
    is_bot = models.BooleanField(
        default=False,
        verbose_name="Бот",
        help_text="Указывает, является ли пользователь ботом.",
    )
    
    balance = models.BigIntegerField(
        default=0,
        verbose_name="Баланс",
        help_text="Баланс пользователя.",
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан пользователь.",
    )

    def get_name(self):
        if self.username:
            return self.username
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return "Пользователь"

    def __str__(self):
        return f"{self.user_id}: {self.get_name()}"

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ["-created_at"]


class TelegramChat(models.Model):
    pass


class TelegramIncome(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, которому принадлежит доход.",
    )
    amount = models.BigIntegerField(
        default=0,
        verbose_name="Сумма",
        help_text="Сумма дохода.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан доход.",
    )

    def __str__(self):
        return f"{self.user.get_name()}: {self.amount}"

    class Meta:
        verbose_name = "Доход Telegram"
        verbose_name_plural = "Доходы Telegram"
        ordering = ["-created_at"]
        

class TelegramExpense(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, которому принадлежит расход.",
    )
    amount = models.BigIntegerField(
        default=0,
        verbose_name="Сумма",
        help_text="Сумма расхода.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан расход.",
    )

    def __str__(self):
        return f"{self.user.get_name()}: {self.amount}"

    class Meta:
        verbose_name = "Расход Telegram"
        verbose_name_plural = "Расходы Telegram"
        ordering = ["-created_at"]
     
     
class TelegramSupport(models.Model):
    user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, которому принадлежит расход.",
    )
    message = models.TextField(
        verbose_name="Сообщение",
        help_text="Сообщение пользователя.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан расход.",
    )

    def __str__(self):
        return f"{self.user.get_name()}: {self.message}"

    class Meta:
        verbose_name = "Поддержка Telegram"
        verbose_name_plural = "Поддержка Telegram"
        ordering = ["-created_at"]
