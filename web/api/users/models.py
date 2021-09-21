from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import post_save

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager

from Settings.models import Language, Settings

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None):
            """
            Creates and saves a User with the given email and password.
            """
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                email=self.normalize_email(email),
            )

            user.set_password(password)
            user.save(using=self._db)
            return user

    def create_superuser(self, email, password):
            """
            Creates and saves a superuser with the given email and password.
            """
            user = self.create_user(
                email,
                password=password,
            )
            user.is_staff = True
            user.is_superuser = True
            user.save(using=self._db)
            return user


class Users(AbstractBaseUser, PermissionsMixin):
    st = [("0",'Выключен'),("1",'Включен')]
    user_level = [("0", "Уровень 0"), ("1", "Уровень 1")]
    user_real = [("0", "Уровень 0"), ("1", "Уровень 1"), ("2", "Уровень 2")]
    st_block = [("0",'Разблокирован'),("1",'Заблокирован')]
    

    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=30, blank=True, default="Анонимный")
    last_name = models.CharField('Фамилия', max_length=30, blank=True, default="пользователь")
    bithday = models.DateTimeField("Дата рождения", null=True, blank=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    mail_tempkey = models.CharField("Временный ключ", max_length=30, blank=True)
    token = models.CharField(null=True, blank=True, max_length=10)
    status = models.CharField(verbose_name="Статус", max_length=1, choices=st, default="0")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    status_block = models.CharField(verbose_name="Статус блокирования", max_length=1, choices=st_block, default="0")
    level = models.CharField(verbose_name="Уровень пользователя", max_length=1, choices=user_level, default="0")
    language = models.ForeignKey(Language, verbose_name="Выбранный язык сайта пользователем", on_delete=models.CASCADE, related_name="user_language", null=True, blank=True)
    balance = models.FloatField(verbose_name="Баланс пользователя", default="0")

    playlist_count = models.IntegerField(verbose_name="Количество плейлистов которых может создать", default="1")
    package_count = models.IntegerField(verbose_name="Количество пакетов которых может создать", default="1")
    referral_count = models.IntegerField(verbose_name="Баланс рефериалов которых может создать", default="1")

    bossid = models.IntegerField(verbose_name="Через кого зарегестрировался пользователь", null=True, blank=True)
    profit = models.FloatField(verbose_name="Процент с покупок рефералов", blank=True)

    last_login_data = models.DateTimeField('Дата последнего подключения ', null=True, blank=True)
    reg_ip = models.GenericIPAddressField(verbose_name="IP регистрации ", null=True, blank=True)
    last_login_ip =  models.GenericIPAddressField(verbose_name="IP последнего подключения ", null=True, blank=True)
    phone_number = models.CharField(verbose_name="Номер телефона", max_length=12, blank=True)

    real = models.CharField(verbose_name="Уровень доверия", max_length=1, choices=user_real, default="0")
    newscfg = models.CharField(verbose_name="Новостная рассылка", max_length=1, choices=st, default="0")
    newspayment = models.CharField(verbose_name="Уведомления на почту о том, что заканчиваются кредиты", max_length=1, choices=st, default="0")

    comment = models.TextField(verbose_name="Комментарий", blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, **kwargs):
        if not self.profit:
            if Settings.objects.all().first():
                obj_settings = Settings.objects.all().first()
                self.profit = obj_settings.min_profit
        
        super(Users, self).save()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def __str__(self):
        return f"{self.get_full_name()}"
