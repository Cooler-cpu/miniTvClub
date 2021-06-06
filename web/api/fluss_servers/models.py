from django.db import models

from fluss.service import Server

from sortedm2m.fields import SortedManyToManyField
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.db.models import signals
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
    url = models.CharField(verbose_name="Ссылка на бэкенд", max_length=120)
    server_auth = models.ForeignKey(ServerAuth, verbose_name="Бэкенд авторизация", on_delete=models.CASCADE, related_name="auth_urls")

    def __str__(self):
        return self.server_auth.name

    class Meta:
        verbose_name = "Ссылка на бэкенд авторизацию"
        verbose_name_plural = "Ссылки на бэкенд авторизации"


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

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return self.fluss_url

@receiver(m2m_changed, sender = Servers.auth_backends.through)
def create_server(instance, **kwargs):
    action = kwargs.pop('action', None)
    if action == "post_add":
        print(instance.auth_backends.all())

@receiver(post_save, sender = Servers)
def create_server2(instance, sender, **kwargs):
    print(instance.dvr.all())


class ServerDvr(models.Model):
    disk_limit = models.IntegerField(verbose_name="Диск лимит", default=85)
    dvr_limit = models.IntegerField(verbose_name="Архив лимит", default=259200)
    server = models.OneToOneField(Servers, on_delete=models.CASCADE, related_name="dvr")

    def __str__(self):
        # return self.server.name
        return "g"

    class Meta:
        verbose_name = "Архив сервера"
        verbose_name_plural = "Архив сервера"

    # @receiver(post_save, sender = ServerDvr)
    def create_server2(instance, sender, **kwargs):
        print("hi")


# post_save.connect(ServerDvr.create_server2, sender = ServerDvr)


class DvrPath(models.Model):
    url = models.CharField(verbose_name="Путь к диску", max_length=120, default="url")
    server_auth = models.ForeignKey(ServerDvr, verbose_name="Архив сервера", on_delete=models.CASCADE, related_name="dvr_urls")

    def __str__(self):
        return self.server_auth.server.name

    class Meta:
        verbose_name = "Ссылка на диск"
        verbose_name_plural = "Ссылки на диски"

