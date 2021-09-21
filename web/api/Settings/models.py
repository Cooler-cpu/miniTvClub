from django.db import models

class Language(models.Model):

    language = models.CharField(verbose_name="Архив сервера", unique=True, max_length=10)

    def __str__(self):
        return f"Язык: {self.language}"

    class Meta:
        verbose_name = "Язык сайта"
        verbose_name_plural = "Языки сайта"


class Settings(models.Model):

    min_profit = models.FloatField(verbose_name="Процент с покупок рефералов", null=True, blank=True)
    days_referral = models.IntegerField(verbose_name="Количество дней сколько доступна рефералка", null=True, blank=True)

    def __str__(self):
        return f"Настройки сайта: Минимальный процент с покупок рефералов - {self.min_profit}, Минимальное количество доступных дней для реферального кода {self.days_referral}"

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

