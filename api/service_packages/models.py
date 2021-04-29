from django.db import models

class Package(models.Model):
    name = models.CharField(verbose_name="Название платежа", max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пакет"
        verbose_name_plural = "Пакеты"