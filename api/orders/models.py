from django.db import models
from django.utils import timezone

from users.models import Clients
from service_packages.models import Package


class TypePayment(models.Model):
    name = models.CharField(verbose_name="Название типа платежа", max_length=250)

    class Meta:
        verbose_name = "Название типа платежа"
        verbose_name_plural = "Типы платижей"

    def __str__(self):
        return self.name


class StatusPayments(models.Model):
    name = models.CharField(verbose_name="Название типа платежа", max_length=250)

    class Meta:
        verbose_name = "Название статуса платежа"
        verbose_name_plural = "Статусы платижей"

    def __str__(self):
        return self.name


class Payments(models.Model):
    user = models.ForeignKey(Clients, verbose_name="Клиент", on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(verbose_name="Ip платежа")
    total_sum = models.FloatField(verbose_name="Сумма платежа")
    type_payments = models.ForeignKey(TypePayment, verbose_name="Тип платежа", on_delete=models.CASCADE)
    status_payments = models.ForeignKey(StatusPayments, verbose_name="Статус платежа", on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Дата платежа", default=timezone.now())

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.id}"


class Orders(models.Model):
    payment = models.ForeignKey(Payments, verbose_name="Информация об платеже", on_delete=models.CASCADE )
    package = models.ManyToManyField(Package, verbose_name="Приобретенный пакет")
    starts_with = models.DateTimeField(verbose_name="Активен с", default=timezone.now())
    valid_until = models.DateTimeField(verbose_name="Действителен до", default=timezone.now())

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"