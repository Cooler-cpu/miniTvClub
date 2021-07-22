from django.apps import AppConfig


class FlussServersConfig(AppConfig):
    verbose_name = "Сервера"
    name = 'fluss_servers'

    def ready(self):
        import fluss_servers.signals

    