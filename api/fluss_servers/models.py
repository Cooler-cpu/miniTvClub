from django.db import models


class Servers(models.Model):
    fluss_url = models.CharField(verbose_name="Адрес на сервер", max_length=120)

    class Meta:
        verbose_name = "Сервер"
        verbose_name_plural = "Сервера"

    def __str__(self):
        return self.fluss_url