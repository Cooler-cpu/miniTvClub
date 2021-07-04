from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView

from rest_framework.generics import ListAPIView

from rest_framework.response import Response

from .models import Packets, Channels

#test
# from users.models import Users
# from users.serializers import UserSerializers

from .serializers import(
    PacketSerializer, ChannelSerializer
)

# class Packet(APIView):
#     def get(self, request):
#         try:
#             packets = Packets.objects.all()
#         except Packets.DoesNotExist:
#             return Response(status=204)

#         print(packets)

#         serializer = PacketSerializer(packets)

#         # if serializer.is_valid(raise_exception=True):
#         print(serializer.data)

#         return Response(serializer.data)
#         # else:
#             # return Response(status = 204)


# test view  http://127.0.0.1:8000/api/getPackets

class Packet(ListAPIView):
    queryset = Packets.objects.all()
    
    serializer_class = PacketSerializer
    

# рабочий сериализатор для пользователя
# class Packet(ListAPIView):
#     queryset = Users.objects.all()

#     serializer_class = UserSerializers

# class Packet(ListAPIView):
#     queryset = Channels.objects.all()

#     serializer_class = ChannelSerializer