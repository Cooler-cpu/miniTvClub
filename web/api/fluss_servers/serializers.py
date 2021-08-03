from rest_framework import serializers

from .models import ServerDvr


class DVRSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServerDvr
        fields = ("id", "name")