from django.db import models

from fluss.service import Server


class Servers(models.Model):
    st = [("0",'Выключен'),("1",'Включен')]
    name = models.CharField(verbose_name="Название сервера", max_length=120)
    fluss_url = models.CharField(verbose_name="Адрес на сервер", max_length=120)
    login = models.CharField(verbose_name="Логин подключения", max_length=120)
    password = models.CharField(verbose_name="Пароль подключения", max_length=120)
    interfaceinput = models.CharField(verbose_name="Входной адрес для интерфейса", max_length=120, blank=True)
    interfaceoutput = models.CharField(verbose_name="Выходной адрес для интерфейса", max_length=120, blank=True)
    network = models.FloatField(verbose_name="Пропускной трафиц в мегабайтах")
    comment = models.TextField(verbose_name="Комментарий", blank=True)
    timeout = models.FloatField(verbose_name="Время отлика в секундах")
    geoip = models.GenericIPAddressField(verbose_name="IP сервера")
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0")
    autobalancer = models.CharField(verbose_name="Учавствует в автобалансировки", max_length=1, choices=st, default="0")

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return self.fluss_url

    def save(self, *args, **kwargs):
        serv = Server(self)
        serv.is_exists()
        serv.start()
        super().save(*args, **kwargs)


class ServerDvr(models.Model):
    disk_limit = models.IntegerField(verbose_name="Диск лимит", default=85)
    dvr_limit = models.IntegerField(verbose_name="Архив лимит", default=259200)
    server = models.OneToOneField(Servers, on_delete=models.CASCADE, related_name="dvr")

    def __str__(self):
        return self.server.name

    class Meta:
        verbose_name = "Архив сервера"
        verbose_name_plural = "Архив сервера"


class DvrPath(models.Model):
    url = models.CharField(verbose_name="Путь к диску", max_length=120)
    server_auth = models.ForeignKey(ServerDvr, verbose_name="Архив сервера", on_delete=models.CASCADE, related_name="dvr_urls")

    def __str__(self):
        return self.server_auth.server.name

    class Meta:
        verbose_name = "Ссылка на бэкенд авторизацию"
        verbose_name_plural = "Ссылки на бэкенд авторизации"


class ServerAuth(models.Model):
    name = models.CharField(verbose_name="Название бэкенд авторизации", max_length=120)
    position = models.SmallIntegerField(verbose_name="Приоритет", default=0)
    allow_default = models.BooleanField(verbose_name="Разрешить, если все бэкенды вышли из строя", default=False)
    server = models.ForeignKey(Servers, on_delete=models.CASCADE, related_name="auth")

    def __str__(self):
        return self.server.name

    class Meta:
        verbose_name = "Бэкенд авторизация"
        verbose_name_plural = "Бэкенд авторизации"


class AuthUrl(models.Model):
    url = models.CharField(verbose_name="Ссылка на бэкенд", max_length=120)
    server_auth = models.ForeignKey(ServerAuth, verbose_name="Бэкенд авторизация", on_delete=models.CASCADE, related_name="auth_urls")

    def __str__(self):
        return self.server_auth.server.name

    class Meta:
        verbose_name = "Ссылка на бэкенд авторизацию"
        verbose_name_plural = "Ссылки на бэкенд авторизации"