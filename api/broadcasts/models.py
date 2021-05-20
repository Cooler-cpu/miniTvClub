from django.db import models

from django.utils.timezone import now


class TypeBroadcast(models.Model):
    name = models.CharField(verbose_name="Название типа трансляции", max_length=125)

    class Meta:
        verbose_name = "Типа трансляции"
        verbose_name_plural = "Типы трансляций"

    def __str__(self):
        return self.name


class LiveBroadcast(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]

    name = models.CharField(verbose_name="Название стрима", max_length=125)
    pipeline = models.ForeignKey("fluss_pipelines.Pipelines", verbose_name="Список серверов", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Прямая трансляций"
        verbose_name_plural = "Прямые трансляции"


class Schedule(models.Model):
    start = models.IntegerField(verbose_name="Время начала")
    end = models.IntegerField(verbose_name="Время конца")
    comment = models.TextField(verbose_name="Так надо", blank=True, null=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Расписание архива"
        verbose_name_plural = "Расписания архивов"


class ArchivePipelineBroadcast(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]
    
    pipeline = models.ForeignKey("fluss_pipelines.Pipelines", verbose_name="Пакет стримов", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название архива", max_length=125, unique=True)
    disk_limit = models.IntegerField(verbose_name="Диск лимит", default=85)
    dvr_limit = models.IntegerField(verbose_name="Архив лимит", default=259200)
    schedule = models.ManyToManyField(Schedule, verbose_name="Расписания", blank=True)
    root = models.CharField(verbose_name="Путь к архиву", max_length=120)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Архив пакета стримов"
        verbose_name_plural = "Архивы пакетов стримов"
