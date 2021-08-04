from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from fluss.synchronization import FlussSynchronization
from .models import Servers

class SynchronizationView(APIView):
    # permission_classes = (IsAuthenticated,)


    def post(self, request):
        """
        Запуск синхронизации для определенного сервера
        """
        data = JSONParser().parse(request)

        ip = data["ip"]
        server = Servers.objects.get(geoip = ip)
        
        if server: 
            sync = FlussSynchronization(server)
            try:
                sync.synchronization_server()

                res = {'success' : 'Сервер синхронизирован'}
                return Response(res, status=status.HTTP_200_OK)

            except KeyError:
                res = {'error' : 'Ошибка синхронизации'}
        else:
            res = {'error' : 'Сервер не найден'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)







