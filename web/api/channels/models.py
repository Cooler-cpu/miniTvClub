from django.db import models

from fluss_streams.models import Streams

class Channels(models.Model):
    name = models.CharField(verbose_name="Название канала", max_length=120)
    stream = models.ForeignKey(Streams, verbose_name="Поток стрима на канал", on_delete=models.CASCADE, null = True)
    logo = models.FileField(upload_to='logo', null = True) 

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.name
    