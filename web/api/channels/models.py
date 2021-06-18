
from django.db import models

from PIL import Image

from fluss_streams.models import Streams
from users.models import Users

from .validators import validate_epgshift, validate_arhivedays

from categories.models import Categories, Languages
# from languages.models import Languages

from django_app.utils.models_utils import get_ordering_field


class Epg(models.Model):
    name = models.CharField(verbose_name="Название поставщика телепрограммы", max_length=120, null = True)
    sourse = models.CharField(verbose_name="Поток на канал", max_length=120, null = True)
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
    stream = models.ForeignKey(Streams, verbose_name="Поток стрима на канал", on_delete=models.CASCADE, null = True)
    logo = models.ImageField(verbose_name="Лого", upload_to='logo', null = True) 
    epg = models.ForeignKey(Epg, verbose_name="Название ТВ программы", on_delete=models.CASCADE , null = True)
    epgshift = models.SmallIntegerField(verbose_name="Смещение времени ТВ программы канала", validators=[validate_epgshift],  null = True)
    arhivedays = models.SmallIntegerField(verbose_name="Количество дней записи архива", validators=[validate_arhivedays],  null = True)
    catchup = models.BooleanField(verbose_name="on catchup", null = True)
    categories = models.ForeignKey(Categories, verbose_name="Категория", on_delete=models.CASCADE, null = True)
    # subtitles = models.ManyToManyField(Languages, verbose_name="Название языков субтитров", null = True)
    languages = models.ForeignKey(Languages, verbose_name="Язык трансялции", on_delete=models.CASCADE, null = True)
    price = models.FloatField(verbose_name="Цена канала", null = True)
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1", null = True)
    censored = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1", null = True)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    ordering = get_ordering_field()

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"
        ordering = ['ordering']
        
    def save(self, *args, **kwards):
        super().save(*args, **kwards)
        if self.logo:
            image = Image.open(self.logo.path)
            if image.height > 60 or image.width > 60:
                resize = (60, 60)
                image.thumbnail(resize)
                image.save(self.logo.path)
                return image

    def __str__(self):
        return self.name
    
