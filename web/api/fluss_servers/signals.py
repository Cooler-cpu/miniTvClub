from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from fluss.service import ArchivesRequest, AuthRequest
from django.db.models.signals import pre_delete

from .models import ServerAuth
from .models import ServerDvr
from .models import Servers

@receiver(m2m_changed, sender = Servers.auth_backends.through)
def create_server(instance, **kwargs):
    action = kwargs.pop('action', None)
    list_servers= [instance]
    if action == "post_add":
        ar = ArchivesRequest(list_servers)
        ar.update_archive() 
        at = AuthRequest(list_servers)
        at.update_auths()


@receiver(pre_delete, sender=ServerAuth)
def auth_delete(sender, instance, **kwargs):
    servers = instance.servers_set.all()
    at = AuthRequest(servers)
    at.delete_auth(instance)


@receiver(pre_delete, sender=ServerDvr)
def auth_delete(sender, instance, **kwargs):
    servers = Servers.objects.filter(name = instance.server.name)
    ar = ArchivesRequest(servers)
    ar.delete_archive(instance)
