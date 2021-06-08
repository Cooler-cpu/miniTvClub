from django.db import models

from fluss_servers.models import Servers


class Pipelines(models.Model):
    name = models.CharField(verbose_name="Название пакета", max_length=250)
    fluss_servers = models.ManyToManyField(Servers, verbose_name="Список серверов")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "Пакет серверов"
        verbose_name_plural = "Пакеты серверов"

    def __str__(self):
        return self.name