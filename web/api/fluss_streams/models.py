from django.db import models
from django.utils.timezone import now
from fluss.service import StreamRequest
from fluss_pipelines.models import Pipelines
from fluss_servers.models import Servers
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver
from .validators import validate_archive_server, validate_piplenes


class Streams(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.SlugField(verbose_name="Название стрима", unique=True)
    sourse = models.CharField(verbose_name="Поток на канал", max_length=120)
    fluss_pipelines = models.ForeignKey(Pipelines, verbose_name="Пакет серверов", on_delete=models.CASCADE, validators= [validate_piplenes])
    data_create = models.DateTimeField(verbose_name="Дата создание стрима", default=now)
    servers_archive = models.ForeignKey(Servers, verbose_name="Архив на сервере", blank=True, null=True, on_delete=models.SET_NULL, validators= [validate_archive_server])
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return f"{self.name} - {self.sourse}"

    def save(self):
        super(Streams, self).save()
        sr = StreamRequest(self)
        sr.update_stream()


# @receiver(pre_delete, sender=Streams)
# def streams_delete(sender, instance, **kwargs):
#     sr = StreamRequest(instance)
#     sr.delete_stream()