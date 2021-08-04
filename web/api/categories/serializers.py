from rest_framework import serializers

from .models import Categories, Languages


class LanguageSerializer(serializers.ModelSerializer):


    class Meta:
        model = Languages
        exclude = ("id",)

class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Categories
        exclude = ("id",)
