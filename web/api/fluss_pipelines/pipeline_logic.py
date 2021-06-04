from broadcasts.models import LiveBroadcast, ArchivePipelineBroadcast

from django_app.requests import ArchiveRequest

live_type_name = "Прямая трансляция"
archive_type_name =  "Архивная трансляция"


def create_obj(data):
    name = data.name #Имя пайплайна
    type_name = data.type_pipeline.name #Имя типа паплайна

    if type_name == live_type_name:
        LiveBroadcast.objects.create(name=name+"-live", pipeline_id=data.id)
    elif type_name == archive_type_name:
        arch_obj = ArchivePipelineBroadcast.objects.create(pipeline_id=data.id, name=f"{name}-archive", root=f"{name}-archive/disk1")
        arch_obj.save()
        arch = ArchiveRequest(arch_obj)
        arch.create_archive()
    else:
        pass