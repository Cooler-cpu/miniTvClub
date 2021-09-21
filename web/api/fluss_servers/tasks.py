from django_app.celery import app

from .models import Servers
from .views import syncServer

from fluss.service import BaseRequest

@app.task
def make_synchronization():
    for server in Servers.objects.all():
        syncServer(server.fluss_url, server.login, server.password)
    

@app.task 
def make_least_server_loaded():
    sr = BaseRequest()
    min = int("inf")
    for server in Servers.objects.all():
        config = sr.get_server_api_config(server)
        if config["total_bandwidth"] < min:
            min = config["total_bandwidth"]
            