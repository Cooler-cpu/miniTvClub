from rest_framework import serializers

from .models import Playlists


# class PacketSerializers(serializers.Serializer):
#     packet = serializers.SlugRelatedField()



class PlaylistSerializers(serializers.Serializer):
    pass
    # name = serializers.CharField(max_length=50)
    # user = serializers.IntegerField()
    # type_autopay = serializers.CharField(max_length=1)
    # type_pay = serializers.CharField(max_length=1)
    # status = serializers.CharField(max_length=1)
    # # packets = PacketSerializers(many=True)
    # data_start = serializers.DateTimeField()
    # data_stop = serializers.DateTimeField()
    # token = serializers.IntegerField()
