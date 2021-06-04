from django.db import models


class Servers(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]
    name = models.CharField(verbose_name="Название сервера", max_length=120)
    fluss_url = models.CharField(verbose_name="Адрес на сервер", max_length=120)
    login = models.CharField(verbose_name="Логин подключения", max_length=120)
    password = models.CharField(verbose_name="Пароль подключения", max_length=120)
    interfaceinput = models.CharField(verbose_name="Входной адрес для интерфейса", max_length=120, blank=True)
    interfaceoutput = models.CharField(verbose_name="Выходной адрес для интерфейса", max_length=120, blank=True)
    network = models.FloatField(verbose_name="Пропускной трафиц в мегабайтах")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    timeout = models.FloatField(verbose_name="Время отлика в секундах")
    geoip = models.GenericIPAddressField(verbose_name="IP сервера")
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0")
    autobalancer = models.CharField(verbose_name="Учавствует в автобалансировки", max_length=1, choices=st, default="0")

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return self.fluss_url