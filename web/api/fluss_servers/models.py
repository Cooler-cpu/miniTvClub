from django.db import models

from fluss.service import ArchivesRequest, AuthRequest

from sortedm2m.fields import SortedManyToManyField
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class ServerAuth(models.Model):
    name = models.CharField(verbose_name="Название бэкенд авторизации", max_length=120, default="name")
    allow_default = models.BooleanField(verbose_name="Разрешить, если все бэкенды вышли из строя", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бэкенд авторизация"
        verbose_name_plural = "Бэкенд авторизации"


class AuthUrl(models.Model):
    url = models.CharField(verbose_name="Название папки", max_length=120)
    server_auth = models.ForeignKey(ServerAuth, verbose_name="Бэкенд авторизация", on_delete=models.CASCADE, related_name="auth_urls")

    def __str__(self):
        return self.server_auth.name

    class Meta:
        verbose_name = "Ссылка на бэкенд авторизацию"
        verbose_name_plural = "Ссылки на бэкенд авторизации"


class ServerDvr(models.Model):
    name = models.CharField(verbose_name="Название архива", max_length=125, unique=True)
    root = models.CharField(verbose_name="Путь к диску", max_length=125, unique=True, default="root")
    disk_limit = models.IntegerField(verbose_name="Диск лимит", default=85)
    dvr_limit = models.IntegerField(verbose_name="Архив лимит", default=259200)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Архив сервера"
        verbose_name_plural = "Архив сервера"


class Schedule(models.Model):
    start = models.IntegerField(verbose_name="Время начала", default=1)
    end = models.IntegerField(verbose_name="Время конца", default=2)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    server_dvr = models.ForeignKey(ServerDvr, verbose_name="Архив сервера", on_delete=models.CASCADE, related_name="dvr_schedule")

    def __str__(self):
        return f"{self.server_dvr.name} time {self.start}:{self.end}"

    class Meta:
        verbose_name = "Расписание архива"
        verbose_name_plural = "Расписания архивов"


class DvrPath(models.Model):
    url = models.CharField(verbose_name="Название диска", max_length=120, default="url")
    server_dvr = models.ForeignKey(ServerDvr, verbose_name="Архив сервера", on_delete=models.CASCADE, related_name="dvr_urls")

    def __str__(self):
        return f"{self.server_dvr.name} url:{self.url}"

    class Meta:
        verbose_name = "Название диска"
        verbose_name_plural = "Названия дисков"


class Servers(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]
    name = models.CharField(verbose_name="Название сервера", max_length=120, default="name")
    fluss_url = models.CharField(verbose_name="Адрес на сервер", max_length=120, default="http://a1.minitv.club:8080")
    login = models.CharField(verbose_name="Логин подключения", max_length=120, default="test")
    password = models.CharField(verbose_name="Пароль подключения", max_length=120, default="test123")
    interfaceinput = models.CharField(verbose_name="Входной адрес для интерфейса", max_length=120, blank=True)
    interfaceoutput = models.CharField(verbose_name="Выходной адрес для интерфейса", max_length=120, blank=True)
    network = models.FloatField(verbose_name="Пропускной трафиц в мегабайтах", default=100)
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    timeout = models.FloatField(verbose_name="Время отлика в секундах", default=8)
    geoip = models.GenericIPAddressField(verbose_name="IP сервера", default="192.168.1.1")
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0")
    autobalancer = models.CharField(verbose_name="Учавствует в автобалансировки", max_length=1, choices=st, default="0")
    auth_backends = SortedManyToManyField(ServerAuth, verbose_name="Бэкенд авторизации")
    dvr = models.ForeignKey(ServerDvr, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Архив")

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return f"{self.name} - {self.fluss_url}"


@receiver(m2m_changed, sender = Servers.auth_backends.through)
def create_server(instance, **kwargs):
    action = kwargs.pop('action', None)
    if action == "post_add":
        if instance.dvr:
            obj_dvr = instance.dvr
            ar = ArchivesRequest(instance, obj_dvr)
            ar.update_archive()
        obj_auths = instance.auth_backends.all()
        at = AuthRequest(instance, obj_auths)
        at.update_auths()
