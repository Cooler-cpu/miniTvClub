from django.views.generic.base import View
from rest_framework import views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

from fluss.synchronization.synchronizationModel import ModelSynchronization
from fluss.synchronization.synchronizationMedia import MediaSynchronization
from .models import ServerAuth, Servers

from fluss.service import BaseRequest


def syncServer(url, login, password, pk = None):

    sr = BaseRequest()
    server, created = Servers.objects.get_or_create(
        fluss_url = url, 
        login = login, 
        password = password
    )
    answer = sr.get_config(server)
    if not answer: 
        server.delete()

    sync = ModelSynchronization(server = server)
    try:
        sync.synchronization_model()
        res = {'success' : 'Сервер синхронизирован'}
        return res

    except KeyError:
        res = {'error' : 'Ошибка синхронизации'}
        return res


class ModelSynchronizationView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Запуск синхронизации для определенного сервера
        """
        data = JSONParser().parse(request)
        url = data["url"]
        login = data["login"]
        password = data["password"]

        res = syncServer(url, login, password)
        return Response(res)



class MediaSynchronizationView(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Запуск синхронизации для медиа сервера и обьекту сервера привязанному к медиа, 
        по обьекту сервера копирования
        """
        data = JSONParser().parse(request)
        url_copy = data["url_copy"]
        url_sync = data["url_sync"]

        try:
            server_copy = Servers.objects.get(fluss_url = url_copy)
            server_sync = Servers.objects.get(fluss_url = url_sync)
        except Servers.DoesNotExist:
            raise Http404

        sync_media = MediaSynchronization(server_copy = server_copy, server_sync = server_sync)
        sync_model = ModelSynchronization(server_sync = server_sync)

        try:
            sync_media.synchronization_media()
            sync_model.synchronization_model()

            res = {'success' : 'Сервер синхронизирован'}
            return Response(res, status=status.HTTP_200_OK)

        except KeyError:
            res = {'error' : 'Ошибка синхронизации'}
            return Response(res)


from django.views.generic import DetailView

class ServerAction(DetailView):
    model = Servers
    template_name = 'fluss_servers/action_server'










