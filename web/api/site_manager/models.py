from django.db import models
from fluss_streams.models import Streams
# from fluss_servers.models import 
from utils.models_utils import get_verbose_names_meta
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from fluss.service import StreamRequest


class StreamsProxy(Streams):
    class Meta:
        _model = Streams
        verbose_name, verbose_name_plural = get_verbose_names_meta(_model)
        proxy = True

@receiver(pre_delete, sender=StreamsProxy)
def streams_delete(sender, instance, **kwargs):
    sr = StreamRequest(instance)
    sr.delete_stream()