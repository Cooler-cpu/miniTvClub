from rest_framework import serializers

from .models import Playlists, Ips

from users.serializers import UserSerializers
from channels.serializers import PacketSerializer
from tokens.serializer import TokenSerializer

class IpsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ips
        exclude = ("id",)


class PlaylistSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    packets = PacketSerializer(many=True)
    token = TokenSerializer()
    allowaddip = IpsSerializers(many=True)


    class Meta:
        model = Playlists
        exclude = ("id",)

