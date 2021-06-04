from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
# from django_app.requests import StreamRequest
StreamRequest = []
from fluss_pipelines.models import Pipelines


class Streams(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.SlugField(verbose_name="Название стрима")
    sourse = models.CharField(verbose_name="Поток на канал", max_length=120)
    fluss_pipelines = models.ForeignKey(Pipelines, verbose_name="Пакет серверов", on_delete=models.CASCADE)
    data_create = models.DateTimeField(verbose_name="Дата создание стрима", default=now)
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return self.name

    def clean(self):
        super(Streams, self).clean()
        sr = StreamRequest(self)
        try:
            obj = Streams.objects.get(id=self.id)
            obj_name = obj.name
            obj_sourse = obj.sourse
            obj_status = obj.status
        except Exception:
            obj_name = None
            obj_sourse = None
            obj_status = None
        
        if obj_name != self.name:
            if sr.is_exists():
                raise ValidationError("Сервер с таким названием уже существует")
            if obj_name != None:
                sr.delete_stream()
            answer = sr.create_stream()
            if not answer:
                raise ValidationError("Произошла ошибка при создании потока")

        if obj_sourse != self.sourse and obj_sourse != None:
            answer = sr.change_url()
            if not answer:
                raise ValidationError("Произошла ошибка при смене url")

        if obj_status != self.status and obj_status != None:
            answer = sr.change_status()
            if not answer:
                raise ValidationError("Произошла ошибка при смене статуса")


    def delete(self):
        super(Streams, self).delete()
        sr = StreamRequest(self)
        sr.delete_stream()
