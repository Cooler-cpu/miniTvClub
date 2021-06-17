  
from django.core.exceptions import ValidationError

from fluss_servers.models import Servers

def validate_archive_server(value):
    server = Servers.objects.get(id=value)
    if not server.dvr:
        raise ValidationError("Архив на данном сервере отсутствует")
    else:
        return value

      
def validate_piplenes(value):
  if len(value) < 1:
    raise ValidationError("Пайплайн не может быть пустым")
  else:
    return value
