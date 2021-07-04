from rest_framework import serializers

from .models import Streams
from fluss_pipelines.serializer import PipelineSerializer


class StreamsSerializer(serializers.ModelSerializer):
    fluss_pipelines = PipelineSerializer()

    class Meta:
        model = Streams
        exclude = ("id",)