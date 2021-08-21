from django.db.models.signals import m2m_changed, post_save, pre_delete
from django.dispatch import receiver
from fluss.service import ArchivesRequest, AuthRequest

from .models import ServerAuth, ServerDvr, Schedule, Servers

@receiver(m2m_changed, sender = Servers.auth_backends.through)
def create_server(instance, **kwargs):
    action = kwargs.pop('action', None)
    list_servers = [instance]
    if action == "post_add":
        ar = ArchivesRequest(list_servers)
        ar.update_archive() 
        at = AuthRequest(list_servers)
        at.update_auths()


@receiver(pre_delete, sender=ServerAuth)
def auth_delete(sender, instance, **kwargs):
    print("AUTH DELETE SIGNAL")
    servers = instance.servers_set.all()
    at = AuthRequest(servers)
    at.delete_auth(instance)

@receiver(pre_delete, sender=ServerDvr)
def archive_delete(sender, instance, **kwargs):
    print("ARCHIVE DELETE SIGNAL")
    servers = Servers.objects.filter(name = instance.server.name)
    ar = ArchivesRequest(servers)
    ar.delete_archive(instance)

@receiver(post_save, sender=Schedule)
def schedule_save(sender, instance, **kwargs):
    print("ARCHIVE_SCHEDULE POST_SAVE SIGNAL")
    ar = ArchivesRequest()
    ar.update_schedule(instance.server_dvr.server, instance.server_dvr)

