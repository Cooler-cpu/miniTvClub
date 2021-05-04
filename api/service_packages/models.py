from django.db import models

from users.models import Clients
from service_channels.models import Channels


class TypePackage(models.Model):
    name = models.CharField(verbose_name="Название типа платежа", max_length=250)

    class Meta:
        verbose_name = "Название типа пакета"
        verbose_name_plural = "Типы пакетов"

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(verbose_name="Название платежа", max_length=250)
    total_sum = models.FloatField(verbose_name="Стоимость пакета")
    type_payments = models.ForeignKey(TypePackage, verbose_name="Тип пакета", on_delete=models.CASCADE)
    owner = models.ForeignKey(Clients, verbose_name="Пакет от пользователя", on_delete=models.CASCADE, blank=True, null=True)
    channels = models.ManyToManyField(Channels, verbose_name="Список каналов")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пакет"
        verbose_name_plural = "Пакеты"