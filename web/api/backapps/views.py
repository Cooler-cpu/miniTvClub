from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from django.http import Http404
from fluss_servers.models import Servers
from .models import ServerBackapps
from fluss.synchronization.synchronizationModel import ModelSynchronization
from fluss.synchronization.synchronizationMedia import MediaSynchronization
from rest_framework.response import Response
from rest_framework import status

from fluss.service import BaseRequest

class BackappsServerActivate(APIView):

    def post(self, request):
        """
        Активация синхронизации для сервера
        """
        data = JSONParser().parse(request)
        url = data["url"]
        id_backapps = data["id_backapps"]
        try:
            server = Servers.objects.get(fluss_url = url)
            br = BaseRequest()
        except Servers.DoesNotExist:
            raise Http404
        try:
            backapps = ServerBackapps.objects.all()
            server_backapps = ServerBackapps.objects.get(id = id_backapps)
            json_load = server_backapps.json
        except ServerBackapps.DoesNotExist:
            raise Http404

        sync = ModelSynchronization(server = server, server_json = json_load)
        try:
            sync.synchronization_model()
            res = {'success' : 'Сервер синхронизирован'}
            return Response(res, status=status.HTTP_200_OK)
        except KeyError:
            res = {'error' : 'Ошибка синхронизации'}
            return Response(res)

 

