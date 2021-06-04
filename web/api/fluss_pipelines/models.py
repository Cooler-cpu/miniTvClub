from django.db import models

from fluss_servers.models import Servers
from broadcasts.models import TypeBroadcast

from .pipeline_logic import create_obj


class Pipelines(models.Model):
    name = models.CharField(verbose_name="Название пакета", max_length=250)
    type_pipeline = models.ForeignKey(TypeBroadcast, verbose_name="Тип пакета", on_delete=models.CASCADE)
    fluss_servers = models.ManyToManyField(Servers, verbose_name="Список серверов")

    class Meta:
        verbose_name = "Пакет серверов"
        verbose_name_plural = "Пакеты серверов"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        create_obj(self)
