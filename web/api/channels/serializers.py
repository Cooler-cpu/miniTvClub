from rest_framework import serializers

from .models import Packets, Channels, Epg

from users.serializers import UserSerializers
from categories.serializers import (
    CategorySerializer,
    LanguageSerializer
    )

class EpgSerializer(serializers.ModelSerializer):
    epg_user = UserSerializers()

    class Meta:
        model = Epg
        exclude = ("id",)


class ChannelSerializer(serializers.ModelSerializer):
     
    epg = EpgSerializer()
    categories = CategorySerializer()
    languages = LanguageSerializer()

    class Meta:
        model = Channels
        exclude = ("id",)



class PacketSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    channels = ChannelSerializer(many=True)
    
    class Meta:
        model = Packets
        exclude = ("id",)
