from datetime import timedelta
from django.db import models
from users.models import Users
from channels.models import Packets

from datetime import datetime
from dateutil.relativedelta import relativedelta

# test
from fluss.synchronization import FlussSynchronization
from fluss_servers.models import Servers

class PacketOrder(models.Model):
    st = [("0",'Системный'),("1",'Приватный')]  
    st_pay = [("0",'Оплачен'),("1",'Неоплачен')]  

    order_type = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0")
    user = models.ForeignKey(Users, verbose_name="Кому создан пакет",  blank=True, null=True, on_delete=models.SET_NULL, related_name="packet_user")
    creator = models.ForeignKey(Users, verbose_name="Кто создал пакет",  blank=True, null=True, on_delete=models.SET_NULL, related_name="packet_creator")
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st_pay, default="1")
    packet = models.ForeignKey(Packets, verbose_name="Пакет", blank=True, null=True, on_delete=models.SET_NULL, related_name="packet_order")
    price = models.FloatField(verbose_name="Цена канала")
    date = models.DateTimeField(verbose_name="Дата создания", default=datetime.now())
    dateStop = models.DateTimeField(verbose_name="Дата оканчания действителности приобритения заказа", blank=True, null=True) 
    period = models.IntegerField(verbose_name="Срок на покупку пакета(месяц)", default=1) # todo/ запрет на редактирование
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    def __str__(self):
        return self.user.email

    def save(self):
        self.dateStop = datetime.now() + relativedelta(months=+1)
        
        """
        test function synchronization
        if data exist on media server and not exist in server object
        """
        server = Servers.objects.get(fluss_url = 'http://a1.minitv.club:8080')
        sync = FlussSynchronization(server)
        sync.synchronization_server()

        super(PacketOrder, self).save()

    class Meta:
        verbose_name = "Заказ пакета"
        verbose_name_plural = "Заказ пакетов"