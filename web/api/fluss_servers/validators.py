from django.core.exceptions import ValidationError

def validate_archive_server(value):
    if not value.dvr:
        raise ValidationError("Архив на данном сервере отсутствует")
    else:
        return value
