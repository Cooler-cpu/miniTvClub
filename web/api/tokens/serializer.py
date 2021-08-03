from rest_framework import serializers

from .models import Token, TokenType


class TokenTypeSerializer(serializers.ModelSerializer):

    class Meta:
            model = TokenType
            exclude = ("id",)


class TokenSerializer(serializers.ModelSerializer):

    type_token = TokenTypeSerializer()

    class Meta:
        model = Token
        exclude = ("id",)
