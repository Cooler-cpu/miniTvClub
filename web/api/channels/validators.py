from django.core.exceptions import ValidationError



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