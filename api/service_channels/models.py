from django.db import models

class Channels(models.Model):
    name = models.CharField(verbose_name="Название канала", max_length=250)

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.name