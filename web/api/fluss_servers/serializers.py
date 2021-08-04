from rest_framework import serializers

from .models import ServerDvr


class DVRSerializers(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = ServerDvr
        fields = ("id", "name")

    def get_name(self, name):
        return name.__str__()