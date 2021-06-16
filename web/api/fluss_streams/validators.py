  
from django.core.exceptions import ValidationError

from fluss_servers.models import Servers

def validate_archive_server(value):
    server = Servers.objects.get(id=value)
    if not server.dvr:
        raise ValidationError("Архив на данном сервере отсутствует")
    else:
        return value
