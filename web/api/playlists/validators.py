from django.core.exceptions import ValidationError



def validate_ipFreeConntections(value):
    if value < 0:
        raise ValidationError("Количество ip должно быть больше нуля")
    else: 
        return value

def validate_maxConnections(value):
    if value < 0:
        raise ValidationError("Максимальное количество подключений должно быть больше нуля")
    else: 
        return value

