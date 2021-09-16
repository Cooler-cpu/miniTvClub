from django.db import models
from django.core.exceptions import ValidationError

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from sortedm2m.fields import SortedManyToManyField

from fluss.service import ArchivesRequest

from django.urls import reverse

class ServerAuth(models.Model):
    name = models.CharField(verbose_name="Название бэкенд авторизации", max_length=120, default="name", unique=True)
    allow_default = models.BooleanField(verbose_name="Разрешить, если все бэкенды вышли из строя", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бэкенд авторизация"
        verbose_name_plural = "Бэкенд авторизации"


class AuthUrl(models.Model):
    url = models.CharField(verbose_name="Ссылка на бэкенд", max_length=120)
    server_auth = models.ForeignKey(ServerAuth, verbose_name="Бэкенд авторизация", on_delete=models.CASCADE, related_name="auth_urls")

    def __str__(self):
        return f"{self.server_auth} - {self.url}"

    class Meta:
        verbose_name = "Ссылка на бэкенд авторизацию"
        verbose_name_plural = "Ссылки на бэкенд авторизации"


class ServerDvr(models.Model):
    name = models.CharField(verbose_name="Название архива", max_length=125, unique=True)
    root = models.CharField(verbose_name="Путь к архиву", max_length=125, unique=True, default="root")
    disk_limit = models.IntegerField(verbose_name="Диск лимит", default=85)
    dvr_limit = models.IntegerField(verbose_name="Архив лимит", default=259200)
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    server = models.ForeignKey("Servers", on_delete=models.CASCADE, verbose_name="Сервер", related_name="server_dvr", null=True, blank= True)

    def __str__(self):
        return f"{self.server} - {self.name}"

    class Meta:
        verbose_name = "Архив сервера"
        verbose_name_plural = "Архив сервера"

    def clean(self):
        old_obj = ServerDvr.objects.filter(id=self.id)
        if old_obj.exists():
            if old_obj[0].name != self.name:
                raise ValidationError('Название архива запрещено менять')
        return super(ServerDvr, self).clean()

    def save(self, **kwargs):
        super(ServerDvr, self).save()
        servers = Servers.objects.filter(name = self.server.name)
        ar = ArchivesRequest(servers)
        ar.update_archive()


class Schedule(models.Model):
    # start = models.IntegerField(verbose_name="Время начала", default=1)
    # end = models.IntegerField(verbose_name="Время конца", default=2)
    start = models.TimeField(verbose_name="Время начала")
    end = models.TimeField(verbose_name="Время конца")
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
    name = models.CharField(verbose_name="Название сервера", max_length=120, default="name", unique=True)
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

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return f"{self.name} - {self.fluss_url}"

    def get_dvrs(self):
        return self.server_dvr.all()

    def get_absolute_url(self):
        return reverse('server_action', kwargs={'pk': self.pk})
        



