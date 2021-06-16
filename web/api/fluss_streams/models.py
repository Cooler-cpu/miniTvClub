from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from fluss.service import StreamRequest
from fluss_pipelines.models import Pipelines
from fluss_servers.models import Servers
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .validators import validate_archive_server


class Streams(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.SlugField(verbose_name="Название стрима")
    sourse = models.CharField(verbose_name="Поток на канал", max_length=120)
    fluss_pipelines = models.ForeignKey(Pipelines, verbose_name="Пакет серверов", on_delete=models.CASCADE)
    data_create = models.DateTimeField(verbose_name="Дата создание стрима", default=now)
    servers_archive = models.ForeignKey(Servers, verbose_name="Список серверов", blank=True, null=True, on_delete=models.CASCADE, validators= [validate_archive_server])
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return self.name

    def save(self):
        super(Streams, self).save()
        sr = StreamRequest(self)
        sr.update_stream()

    # def delete(self):
    #     super(Streams, self).delete()
    #     sr = StreamRequest(self)
    #     sr.delete_stream()


