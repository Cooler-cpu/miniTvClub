
from fluss.service import StreamRequest

class MediaSynchronization(StreamRequest):
    def __init__(self, server_copy,  server_sync):
        self.server_copy = server_copy
        self.server_sync = server_sync
        self.data_sync = ("auth_backends", "dvrs", "streams")


    def copy_config(self, server_copy, server_sync):
        config_copy = self.get_config(server_copy)

        config_sync = self.get_config(server_sync)
        config_auth = config_copy.get("auth_backends", {})
        config_dvrs = config_copy.get("dvrs", {})
        config_sync["auth_backends"] = config_auth
        config_sync["dvrs"] = config_dvrs

        # print(config_sync)

        return config_sync
        
    
    def load_config(self, server_sync, new_config):
        self.send_config(server_sync, new_config)


    def synchronization_media(self):
        new_config = self.copy_config(self.server_copy, self.server_sync)
        self.load_config(self.server_sync, new_config)
