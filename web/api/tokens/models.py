from django.db import models

from .generator import token_generator


class TokenType(models.Model):
    name = models.CharField(verbose_name="Имя токена", max_length=125)
    count_symbols = models.PositiveSmallIntegerField(verbose_name="Количество символов")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип токена"
        verbose_name_plural = "Типы токенов"


class Token(models.Model):
    type_token = models.ForeignKey(TokenType, verbose_name="Тип токена", on_delete=models.CASCADE)
    token = models.CharField(verbose_name="Токен", max_length=150, blank=True, null=True)
    date_create = models.DateTimeField(verbose_name="Дата генерации токена", auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.token}"

    def save(self):
        if not self.token:
            self.token = token_generator(size=self.type_token.count_symbols)
        super(Token, self).save()

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"