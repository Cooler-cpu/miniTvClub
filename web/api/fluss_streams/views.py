from django.db.models.query import QuerySet
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from fluss_streams.models import Streams
from fluss_pipelines.models import Pipelines
from fluss_servers.serializers import DVRSerializers
from fluss_servers.models import ServerDvr

#Channels import 
from .models import Packets
from .serializers import(
     PacketSerializer, ChannelSerializer
)

class GetPipelinesListView(APIView):
    def post(self, request, *args, **kwargs):
        pipeline_name = self.request.POST.get("pipeline_name")
        pipeline = Pipelines.objects.get(name=pipeline_name)
        servers = pipeline.fluss_servers.all()
        archives = []
        for server in servers:
            ars = server.get_dvrs()
            for archive in ars:
                archives.append(archive)
        serializer = DVRSerializers(archives, many=True)
        data = serializer.data
        return Response(data)


class Packet(ListAPIView):
    queryset = Packets.objects.all()
    
    serializer_class = PacketSerializer

