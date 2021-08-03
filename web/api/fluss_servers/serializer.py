from rest_framework import serializers

from .models import Servers, DvrPath, Schedule, ServerDvr, AuthUrl, ServerAuth

class ServerAuthSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServerAuth
        exclude = ("id",)


class AuthUrlSerializer(serializers.ModelSerializer):

    server_auth = ServerAuthSerializer()

    class Meta:
        model = AuthUrl
        exclude = ("id",)


class ServerDvrSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServerDvr
        exclude = ("id",)


class ScheduleSerializer(serializers.ModelSerializer):

    server_dvr = ServerDvrSerializer()

    class Meta:
        model = Schedule
        exclude = ("id",)


class DvrPathSerializer(serializers.ModelSerializer):

    server_dvr = ServerDvrSerializer()

    class Meta:
        model = DvrPath
        exclude = ("id",)

class ServerSerializer(serializers.ModelSerializer):

    auth_backends = ServerAuthSerializer(many=True)
    dvr = ServerDvrSerializer()

    class Meta:
        model = Servers
        exclude = ("id",)