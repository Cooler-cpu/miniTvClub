  
from django.core.exceptions import ValidationError

from fluss_servers.models import Servers
from fluss_pipelines.models import Pipelines


def validate_archive_server(value):
    server = Servers.objects.get(id=value)
    if not server.get_dvrs():
        raise ValidationError("Архив на данном сервере отсутствует")
    else:
      return value

      
def validate_piplenes(value):
  pipeline = Pipelines.objects.get(id=value)
  if len(pipeline.fluss_servers.all()) < 1:
    raise ValidationError("Пайплайн не может быть пустым")
  else:
    return value
