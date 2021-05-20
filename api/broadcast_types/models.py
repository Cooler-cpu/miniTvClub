# from django.db import models

# from fluss_pipelines.models import Pipelines
# from fluss_servers.models import Servers

# from django.utils.timezone import now


# # class LiveBroadcast(models.Model):
# #     st = [("0",'Выключен'),("1",'Включен')]

# #     name = models.CharField(verbose_name="Название стрима", max_length=125)
# #     pipeline = models.ForeignKey(Pipelines, verbose_name="Пакет стримов", on_delete=models.CASCADE)
# #     comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
# #     status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

# #     def __str__(self):
# #         return self.name

# #     class Meta:
# #         verbose_name = "Прямая трансляций"
# #         verbose_name_plural = "Прямые трансляции"


# class ArchiveBroadcast(models.Model):
#     st = [("0",'Выключен'),("1",'Включен')]

#     name = models.CharField(verbose_name="Название канала с архивом", max_length=125)
#     sourse = models.CharField(verbose_name="Поток на архив канала", max_length=120)
#     fluss_server = models.ForeignKey(Servers, verbose_name="Сервер, где хранится архив", on_delete=models.CASCADE)
#     data_create = models.DateTimeField(verbose_name="Дата создание стрима", default=now)
#     status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Архив стрима"
#         verbose_name_plural = "Архивы стримов"


# class ArchivePipelineBroadcast(models.Model):
#     st = [("0",'Выключен'),("1",'Включен')]
    
#     pipeline = models.ForeignKey(Pipelines, verbose_name="Пакет стримов", on_delete=models.CASCADE)
#     dvrs = models.ManyToManyField(ArchiveBroadcast, verbose_name="Архивы")
#     name = models.CharField(verbose_name="Название архива", max_length=125)
#     comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
#     status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="1")

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Архив пакета стримов"
#         verbose_name_plural = "Архивы пакетов стримов"