from fluss.service import StreamRequest
# from .models import Channels

def arhivedays_recording(stream, arhivedays):
    """
    Добавление количества дней записи архива из канала в архив и на медиа сервер
    """
    if stream.archive != None:
        sec_dvr_limit = arhivedays * 86400
        ar = StreamRequest(stream)
        ar.update_locale_dvr_limit(stream, sec_dvr_limit)

 

def arhivedays_cleaning_from_channel(channel):
    """
    Удаление dvr_limit из channel по stream, если удаляем dvr из stream
    """
    channel.arhivedays = 0
    channel.save()

