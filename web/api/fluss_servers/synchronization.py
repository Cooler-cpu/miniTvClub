from fluss.service import BaseRequest
from .models import ServerDvr 

class FlussSynchronization(BaseRequest):
    def __init__(self, server, server_up = None):
        self.server = server
        self.server_up = server_up
        # поля которые синхронизируем
        self.dataSync = ("auth_backends", "dvrs", "streams")


    def delete_all_auth_backends(self):
        auth_backends = getattr(self.server, "auth_backends")
        auth_backends.clear()
    
    def delete_all_dvrs(self):
        for dvr in self.server.get_dvrs().all():
            ServerDvr.objects.get(name = dvr).delete()


    # Удалить все обьекты auth которых нет на медиа сервере, но есть у нас в обьекте сервера
    def delete_objects_auth(self, config_auth):
        auth_backends = getattr(self.server, "auth_backends")
        list_Auth_names = [authConfig for authConfig in config_auth]
        for auth in auth_backends.all():
            is_delete = False
            for name_config in list_Auth_names:
                if auth.name == name_config:
                    is_delete = True
            if is_delete != True:
                self.server.auth_backends.remove(auth)



    def synchronization_server(self):
        config = self.get_config(self.server)
        for syncField in self.dataSync:
            config[syncField] = config.get(syncField, {})
            if config[syncField]:
                if syncField == "auth_backends":
                    self.delete_objects_auth(config[syncField])
            else:
                if syncField == "auth_backends":
                    self.delete_all_auth_backends()
                if syncField == "dvrs":
                    self.delete_all_dvrs()



