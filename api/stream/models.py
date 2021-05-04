from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .requests import StreamRequest

from fluss_servers.models import Servers


class Stream(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.SlugField(verbose_name="Название стрима")
    sourse = models.CharField(verbose_name="Поток на канал", blank=True, max_length=120)
    fluss_server = models.ForeignKey(Servers, verbose_name="Сервер", on_delete=models.CASCADE)
    data_create = models.DateTimeField(verbose_name="Дата создание стрима", default=now)
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0")

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return self.name

    def clean(self):
        super(Stream, self).clean()
        sr = StreamRequest(stream_name=self.name, server_url=self.fluss_server.fluss_url)
        try:
            obj = Stream.objects.get(id=self.id)
            obj_name = obj.name
        except Exception:
            obj_name = None
        
        if obj_name != self.name:
            if sr.is_exists():
                raise ValidationError("Сервер с таким названием уже существует")
            if obj_name != None:
                sr.delete_stream()
            answer = sr.create_stream()
            if not answer.get("success", None):
                raise ValidationError("Произошла ошибка при создании потока")
            self.sourse = sr.sourse_conf


    def delete(self):
        super(Stream, self).delete()
        sr = StreamRequest(stream_name=self.name, server_url=self.fluss_server.fluss_url)
        sr.delete_stream()
