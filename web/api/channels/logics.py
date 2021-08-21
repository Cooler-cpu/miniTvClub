from fluss_servers.models import ServerDvr

def arhivedays_recording(stream, arhivedays):
    """
    Добавление количества дней записи архива из канала в архив и на медиа сервер
    """
    sec = arhivedays * 86400
    archive = ServerDvr.objects.get(name = stream.archive.name)
    archive.dvr_limit = sec
    archive.save()
    