from django.db import models

class Languages(models.Model):
    name = models.CharField(verbose_name="Название языка трансляции", max_length=120, null = True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык трансялции"
        verbose_name_plural = "Языки трансляции"

        

class Categories(models.Model):
    name = models.CharField(verbose_name="Название категории", max_length=120, null = True)    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
