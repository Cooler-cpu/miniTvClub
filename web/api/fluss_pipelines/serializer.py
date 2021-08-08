from rest_framework import serializers

from .models import Pipelines

class PipelineSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Pipelines
        exclude = ("id",)