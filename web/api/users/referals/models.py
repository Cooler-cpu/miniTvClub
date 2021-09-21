from django.db import models

from users.models import Users
from tokens.models import Token

from django.utils.timezone import now

from Settings.models import Settings
from datetime import datetime, timedelta

class Referrals(models.Model):
    st_referral = [("0",'Неактивный'),("1",'Активный'), ("2", 'Использованный')]

    user = models.ForeignKey(Users, verbose_name="Пользователь создавший referal", on_delete=models.CASCADE)
    code = models.ForeignKey(Token, verbose_name="Токен рефериала", on_delete=models.CASCADE)
    status = models.CharField(verbose_name="Статус токена", max_length=1, choices=st_referral, default="1")
    balance = models.FloatField(verbose_name="Начисление за ввод реферального кода", default="0")
    date_start = models.DateTimeField('Дата создания', default=now)
    date_stop = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Реферал"
        verbose_name_plural = "Рефералы"

    def __str__(self):
        return f"{self.user.email} referal:{self.code}"

    def save(self, **kwargs):
        if not self.date_stop:
            if Settings.objects.all().first() and Settings.objects.all().first().days_referral:
                obj_settings = Settings.objects.first()
                self.date_stop = self.date_start + timedelta(days=obj_settings.days_referral)

        super(Referrals, self).save()



