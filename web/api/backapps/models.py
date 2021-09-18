from django.db import models
from django.db.models.fields import json
from django.utils.timezone import now

from fluss_servers.models import Servers
from fluss.service import BaseRequest

from django.urls import reverse

class Server(models.Model):
    server = models.ForeignKey(Servers, verbose_name="Сервер", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return f"{self.server}"

    def save(self, **kwargs):
        super(Server, self).save()
        br = BaseRequest()
        config = br.get_config(self.server)
        ServerBackapps.objects.create(server = self, json = config)

    def get_absolute_url(self):
        return reverse('server_action', kwargs={'pk': self.pk})
        

class ServerBackapps(models.Model):
    data = models.DateTimeField(verbose_name="Дата бэкапа", default=now, null = True)
    json = models.JSONField(verbose_name="Данные в json")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    server = models.ForeignKey(Server, verbose_name="Бэкапы сервера", on_delete=models.CASCADE, related_name="server_back")

    class Meta:
        verbose_name = "Бэкап сервера"
        verbose_name_plural = "Бэкапы серверов"