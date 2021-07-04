from django.db import models

from users.models import Users
from channels.models import Packets

from django.utils.timezone import now
from django.core.exceptions import ValidationError

from .validators import validate_ipFreeConntections, validate_maxConnections


class Ips(models.Model):
    ip = models.CharField(max_length=15, verbose_name="ip", null = True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = "Ip"
        verbose_name_plural = "Ips"    


class Playlists(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]
    st_plural = [("0",'Выключена'),("1",'Включена')]
    st_type_pay = [("0", 'по месячная оплата (безлимит)')] # на поддержку

    name = models.CharField(verbose_name="Имя", max_length=50, null = True)
    user = models.ForeignKey(Users, verbose_name="Создатель плейлиста", on_delete=models.SET_NULL, null = True)
    type_autopay = models.CharField(verbose_name="Авто оплата", max_length=1, choices=st_plural, default="0", null = True)
    type_pay = models.CharField(verbose_name="Тип оплаты", max_length=1, choices=st_type_pay, default="0", null = True) # на поддержку
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0", null = True)
    packets = models.ManyToManyField(Packets, verbose_name="Пакеты")
    data_start = models.DateTimeField(verbose_name="Дата с которой будет действителен", default=now, null = True)
    data_stop = models.DateTimeField(verbose_name="Дата окончания", default=now, null = True)
    token = models.CharField(max_length=50, unique=True, default="dswirymas12346nsasqw")
    max_connections = models.IntegerField(verbose_name="Максимальное кол-во подключений", default=1, null = True, validators=[validate_maxConnections])
    oneip = models.CharField(verbose_name="Доступ только для одного ip", max_length=1, choices=st, default="1", null = True)
    oneipfreeconnections = models.IntegerField(verbose_name="Максимальное количество подключений с oneIp", default=1, null = True, blank = True, validators=[validate_ipFreeConntections])
    allowaddip = models.ManyToManyField(Ips, verbose_name="Массив ip адресов", blank = True)

    class Meta:
        verbose_name = "Плейлист"
        verbose_name_plural = "Плейлисты"
    
    def clean(self):
        if(self.status == 0):
            self.token = None

        if(int(self.oneip) == 0):
            self.oneipfreeconnections = None
        super(Playlists, self).clean()


    def __str__(self):
        return self.name