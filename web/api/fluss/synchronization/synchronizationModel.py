from fluss_servers.models import ServerDvr, Schedule, ServerAuth, AuthUrl
from fluss_pipelines.models import Pipelines
from fluss_streams.models import Streams
from fluss.service import StreamRequest

from datetime import time

class ModelSynchronization(StreamRequest):
    def __init__(self, server, server_json = None, server_up = None):
        self.server = server
        self.server_up = server_up
        self.server_json = server_json
        """
        поля которые синхронизируем
        """
        self.data_sync = ("auth_backends", "dvrs", "streams")

    def delete_all_auth_backends(self):
        auth_backends = getattr(self.server, "auth_backends")
        auth_backends.clear()

    def delete_all_auth_urls(self):
        Auth_url = AuthUrl.objects.all()
        Auth_url.delete()
    
    def delete_all_dvrs(self):
        for dvr in self.server.get_dvrs().all():
            ServerDvr.objects.get(name = dvr.name).delete()

    def delete_objects_dvrs(self, config_dvr):
        """
        Удалить все обьекты dvr которых нет на медиа сервере, но есть у нас в обьекте сервера
        """
        list_Dvrs_names = [dvr for dvr in config_dvr]
        for dvr in self.server.get_dvrs():
            is_delete = True
            for name_config in list_Dvrs_names:
                if dvr.name == name_config:
                    """
                    Не удаляем
                    """
                    is_delete = False 
            if is_delete != False:
                dvr = ServerDvr.objects.get(name = dvr.name)
                dvr.delete()

    def delete_objects_auths(self, config_auth):
        """
        Удалить все обьекты auth которых нет на медиа сервере, но есть у нас в обьекте сервера
        """
        auth_backends = getattr(self.server, "auth_backends")
        list_Auth_names = [authConfig for authConfig in config_auth]
        for auth in auth_backends.all():
            is_delete = True
            for name_config in list_Auth_names:
                if auth.name == name_config:
                    """
                    Не удаляем
                    """
                    is_delete = False 
            if is_delete != False:
                self.server.auth_backends.remove(auth)

    def synchronization_fields_auths(self, config_auth):
        """
        Синхронизируем поля и обьекты auth
        """
        self.delete_all_auth_urls()
        list_Auth_names = [authConfig for authConfig in config_auth] 

        for auth_name in list_Auth_names:
            obj, is_add = ServerAuth.objects.update_or_create(
                name = auth_name,
                defaults={
                    'allow_default' : config_auth[auth_name]['allow_default'],
                }
            )
            self.server.auth_backends.add(obj)
            server_auth = ServerAuth.objects.get(name = auth_name)
            if config_auth[server_auth.name].get('backends'):
                for url in config_auth[server_auth.name].get('backends'):
                    auth_url = AuthUrl(url = url['url'], server_auth = server_auth)
                    auth_url.save()

    def synchronization_fields_dvrs(self, config_dvr):
        """
        Синхронизируем поля и обьекты dvrs
        """
        list_Dvrs_names = [dvr for dvr in config_dvr]

        for dvr_name in list_Dvrs_names:

            key_disk_limit = 'disk_limit'
            key_dvr_limit = 'dvr_limit'
            if key_disk_limit in config_dvr[dvr_name]:
                disk_limit = config_dvr[dvr_name]['disk_limit']
            if key_dvr_limit in config_dvr[dvr_name]:
                dvr_limit = config_dvr[dvr_name]['dvr_limit']


            if disk_limit and dvr_limit:
                dvr_obj, is_create = ServerDvr.objects.update_or_create(
                name = str(dvr_name),
                defaults={
                    'root' : config_dvr[dvr_name]['root'],
                    'disk_limit' : config_dvr[dvr_name]['disk_limit'], 
                    'dvr_limit' : config_dvr[dvr_name]['dvr_limit'],
                    'server' : self.server
                }
            )

            key_schedule = 'schedule'
            schedule = Schedule.objects.filter(server_dvr = dvr_obj).delete()
            if key_schedule in config_dvr[dvr_name]:
                for dvr_schedule in config_dvr[dvr_name]['schedule']:
                    time_arr = []
                    for time_int in dvr_schedule:
                        time_str = str(time_int)
                        size = len(time_str) + 1
                        if size != 2:
                            timepart_1 = time_str[0:size//2]
                            timepart_2 = time_str[size//2:]
                            timepart_1 = int(timepart_1)
                            timepart_2 = int(timepart_2)
                            time_obj = time(timepart_1, timepart_2)
                            time_arr.append(time_obj)
                        else:
                            time_int = int(time_str)
                            time_obj = time(time_int)
                            time_arr.append(time_obj)
                    Schedule.objects.create(start = time_arr[0], end = time_arr[1], server_dvr = dvr_obj)

    def stream_fields_update(self, config_stream):
        """
        Синхронизация source и status если архив с именем как в медиа на сервере есть у нас в системе
        # to do:
            1)Для дальнейшией синхронизации решить проблему с пайплайнами
            2)Синхронизировать auth и dvr на стриме,
        """
        list_stream_name = [stream for stream in config_stream]
        for stream_name in list_stream_name:
            try:
                stream = Streams.objects.get(name=stream_name)
            except Streams.DoesNotExist:
                stream = None
            if stream:
                stream.sourse = config_stream[stream_name]['urls'][0]['url']
                if config_stream[stream_name]['static'] == False:
                    stream.status = '0'
                else:
                    stream.status = '1'                
                stream.save()

    def synchronization_objects_streams(self, config_stream):
        """
        Синхронизация обьектов и полей стримов 
        """
        pipelines = Pipelines.objects.filter(fluss_servers = self.server)

        list_stream_name = [stream for stream in config_stream]
        
        if pipelines:
            for stream in list_stream_name:
                for pipeline in pipelines:
                    if config_stream[stream]['static'] == False:
                        status = '0'
                    else:
                        status = '1'

                    key_dvr = 'dvr'
                    if key_dvr in config_stream[stream]:
                        dvr_name = config_stream[stream]['dvr']['reference']
                        dvr = ServerDvr.objects.get(name = dvr_name)
                    else: 
                        dvr = None

                    key_url = 'urls'
                    if key_url in config_stream[stream]:
                        url = config_stream[stream]['urls'][0]['url']
                    else:
                        url = 'tshttp://127.0.0.1:8000/play/defaultUri'

                    obj, is_create = Streams.objects.update_or_create(
                        name = stream,
                        defaults={
                            'sourse': url,
                            'fluss_pipelines': pipeline,
                            'archive': dvr,
                            'status': status,
                        }
                    )

    # def synchronization_objects_streams(self, config_stream):
    #     """
    #     Добавляет стрим на все медиа сервера в пайплайне если он есть у нас, но нету на медиа сервере
    #     """

    #     """
    #     названия стримов в конфиге медиа сервера
    #     """
    #     list_stream_name = [stream for stream in config_stream]
    #     pipelines = Pipelines.objects.filter(fluss_servers = self.server)
    #     for pipeline in pipelines:
    #         """
    #         названия стримов в системе
    #         """

    #         list_stream_system = [stream.name for stream in Streams.objects.filter(fluss_pipelines = pipeline)]

    #         """
    #         разность списков в системе и на медиа сервере
    #         """
    #         list_diff = list(set(list_stream_system)-set(list_stream_name))  

    #         for stream_name in list_diff:
    #             add_stream = Streams.objects.get(name = stream_name)
    #             sr = StreamRequest(add_stream)
    #             sr.update_stream()
            
    # def synchronization_fields_streams(self, config_stream):
    #     """
    #     Синхронизирует поля стрима на медиа сервере
    #     """
    #     pipelines = Pipelines.objects.filter(fluss_servers = self.server)

    #     for pipeline in pipelines:
    #         list_stream_system = [stream.name for stream in Streams.objects.filter(fluss_pipelines = pipeline)]
        
    #         for stream_name in list_stream_system:
                
    #             stream = Streams.objects.get(name = stream_name)
    #             sr = StreamRequest(stream)
    #             sr.update_stream()

    def synchronization_model(self):
        """
        синхронизирует обьекты если их нет на медиа сервере но есть у нас удаляем.
        Для auth_backends и dvrs
        """
        if self.server_json:
            config = self.server_json
        else:
            config = self.get_config(self.server)
        for syncField in self.data_sync:
            config[syncField] = config.get(syncField, {})

            if config[syncField]:
                if syncField == "auth_backends":
                    self.delete_objects_auths(config[syncField])
                    self.synchronization_fields_auths(config[syncField])
                if syncField == "dvrs":
                    self.delete_objects_dvrs(config[syncField])
                    self.synchronization_fields_dvrs(config[syncField])
                if syncField == "streams":
                    self.synchronization_objects_streams(config[syncField])
                #     self.stream_fields_update(config[syncField])
                #     self.synchronization_objects_streams(config[syncField])
                #     self.synchronization_fields_streams(config[syncField])
            else:
                if syncField == "auth_backends":
                    self.delete_all_auth_backends()
                if syncField == "dvrs":
                    self.delete_all_dvrs()


    




    
        


