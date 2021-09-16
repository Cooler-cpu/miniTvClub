from django.db import models
from django.utils.timezone import now
from fluss.service import StreamRequest
from fluss_pipelines.models import Pipelines
from fluss_servers.models import ServerDvr
from .validators import validate_piplenes,  validate_archive_server, validate_epgshift, validate_arhivedays
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

#import for channels
from PIL import Image
from utils.models_utils import get_ordering_field
from users.models import Users
from sorl.thumbnail import ImageField
from categories.models import Categories, Languages

from .logics import arhivedays_cleaning_from_channel, arhivedays_recording

class Epg(models.Model):
    name = models.CharField(verbose_name="Название поставщика телепрограммы", max_length=120, null = True)
    epg_user = models.ForeignKey(Users, verbose_name="Создатель epg", on_delete=models.CASCADE, null = True)
    url = models.CharField(verbose_name="Адрес на телепрограмму", max_length=120, null = True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    ordering = get_ordering_field()


    class Meta:
        verbose_name = "Название тв программы"
        verbose_name_plural = "Название тв программ"
        ordering = ['ordering']

    def __str__(self):
        return self.name

class Channels(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.CharField(verbose_name="Название канала", max_length=120, null = True)
    stream = models.OneToOneField('fluss_streams.Streams', verbose_name="Поток стрима на канал", on_delete=models.CASCADE, null = True)
    logo = ImageField(verbose_name="Лого", upload_to='logo', null = True) 
    epg = models.ForeignKey(Epg, verbose_name="Поставщик ТВ программы", on_delete=models.CASCADE , null = True)
    epgshift = models.SmallIntegerField(verbose_name="Смещение времени ТВ программы канала(часы)", validators=[validate_epgshift],  null = True)
    arhivedays = models.SmallIntegerField(verbose_name="Количество дней записи архива", validators=[validate_arhivedays])
    catchup = models.BooleanField(verbose_name="catchup", default=True)
    categories = models.ForeignKey(Categories, verbose_name="Категория", on_delete=models.CASCADE, null = True)
    languages = models.ForeignKey(Languages, verbose_name="Язык трансялции", on_delete=models.CASCADE, null = True)
    price = models.FloatField(verbose_name="Цена канала", null = True)
    status = models.CharField(verbose_name="Статус прописывания в плейлист ", max_length=1, choices=st, default="1", null = True)
    censored = models.CharField(verbose_name="Censored", max_length=1, choices=st, default="1", null = True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    ordering = get_ordering_field()

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"
        ordering = ['ordering']
        
    def save(self, *args, **kwards):
        super().save(*args, **kwards)
        arhivedays_recording(self.stream, self.arhivedays)
        if self.logo:
            image = Image.open(self.logo.path)
            if image.height > 60 or image.width > 60:
                resize = (60, 60)
                image.thumbnail(resize)
                image.save(self.logo.path)
                return image

    def __str__(self):
        return self.name

class Packets(models.Model):
    st = [("0",'Для админа'),("1",'Для пользователя'), ("3", 'Тестовый для новых пользователей')]

    user = models.ForeignKey(Users, verbose_name="Создатель пакета", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Имя пакета", max_length=50, null = True)
    channels = models.ManyToManyField(Channels, verbose_name="Каналы")
    price = models.FloatField(verbose_name="Цена", null = True)
    date = models.DateTimeField(verbose_name="Дата создания", default=now, null = True)
    last_time_use = models.DateTimeField(verbose_name="Дата последнего использования(просмотра)", null = True)
    type_packet = models.CharField(verbose_name="Тип", max_length=1, choices=st, default="0", null = True)
    period_day = models.IntegerField(verbose_name="Период действительности(дни)", default=30, null = True)
    ordering = get_ordering_field()

    class Meta:
        verbose_name = "Пакет"
        verbose_name_plural = "Пакеты"
        ordering = ['ordering']
        
    def __str__(self):
        return self.name


class Streams(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.SlugField(verbose_name="Название стрима", unique=True)
    sourse = models.CharField(verbose_name="Поток на канал", max_length=120)
    fluss_pipelines = models.ForeignKey(Pipelines, verbose_name="Пакет серверов", on_delete=models.CASCADE, validators= [validate_piplenes])
    data_create = models.DateTimeField(verbose_name="Дата создание стрима", default=now)
    archive = models.ForeignKey(ServerDvr, verbose_name="Архив на сервере", blank=True, null=True, on_delete=models.SET_NULL, validators=[validate_archive_server])
    #archive = models.ForeignKey(ServerDvr, verbose_name="Архив на сервере", blank=True, null=True, on_delete=models.SET_NULL, validators= [validate_archive_server])
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

    class Meta:
        verbose_name = "Стрим"
        verbose_name_plural = "Стримы"

    def __str__(self):
        return f"{self.name} - {self.sourse}"

    def save(self, *args, **kwargs):
        if self.id:
            stream_old = Streams.objects.get(id = self.id)
        else:
            stream_old = None
        super(Streams, self).save(*args, **kwargs)
        if stream_old != None:
            if stream_old.archive != None and self.archive == None:
                channel = Channels.objects.get(stream = stream_old)
                arhivedays_cleaning_from_channel(channel)

        sr = StreamRequest(self)
        sr.update_stream()

@receiver(pre_delete, sender=Streams)
def streams_delete(sender, instance, **kwargs):
    sr = StreamRequest(instance)
    sr.delete_stream()


