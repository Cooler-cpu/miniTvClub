from django_app.celery import app

from .models import Servers
from .views import syncServer


@app.task
def make_synchronization():
    for server in Servers.objects.all():
        syncServer(server.fluss_url, server.login, server.password)