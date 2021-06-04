from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import post_save


from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


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
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField('Имя', max_length=30, blank=True, default="Анонимный")
    last_name = models.CharField('Фамилия', max_length=30, blank=True, default="пользователь")
    bithday = models.DateTimeField("Дата рождения", null=True, blank=True)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    def __str__(self):
        return f"{self.get_full_name()}"


class Clients(models.Model):
    user = models.OneToOneField(Users, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="client")

    def __str__(self):
        return f"{self.user}"

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Clients.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=Users)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"