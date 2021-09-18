  
from django.core.exceptions import ValidationError

from fluss_servers.models import Servers
from fluss_pipelines.models import Pipelines

"""
Streams validation
"""
def validate_archive_server(value):
    # server = Servers.objects.get(id=value)
    # if not server.get_dvrs():
    #     raise ValidationError("Архив на данном сервере отсутствует")
    # else:
    return value

def validate_piplenes(value):
  pipeline = Pipelines.objects.get(id=value)
  if len(pipeline.fluss_servers.all()) < 1:
    raise ValidationError("Пайплайн не может быть пустым")
  else:
    return value

"""
Channels validation
"""

def validate_epgshift(value):
    if value < -11 or value > 11:
        raise ValidationError("Смещение времени тв программы должно быть от -11 до 11")
    else: 
        return value

def validate_arhivedays(value):
    if value < 0 or value > 7:
        raise ValidationError("Количество дней записи архива должно от 0 до 7")
    else:
        return value