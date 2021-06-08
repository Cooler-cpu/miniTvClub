from django.apps import apps
import requests
import json
from requests.auth import _basic_auth_str


class BaseRequest:
	def get_headers(self, login=None, password=None):
		headers = {'Content-type': 'application/json',
					'Authorization': _basic_auth_str(login, password), 
					'Accept': 'text/plain',
					'Content-Encoding': 'utf-8'}
		return headers

	def get_config(self, server):
		url = f"{server.fluss_url}/flussonic/api/read_config"
		header = self.get_headers(server.login, server.password)
		response = requests.get(url, headers = header)
		answer = response.json()
		return answer

	def send_config(self, server, config):
		url = f'{server.fluss_url}/flussonic/api/modify_config?async=true'
		header = self.get_headers(server.login, server.password)
		response = requests.post(url, headers=header, data = json.dumps(config))
		answer = response.json()
		print(answer)


class ArchivesRequest(BaseRequest):
	def __init__(self, server, obj):
		self.server = server
		self.obj = obj

	def update_archive(self):
		config = self.get_config(self.server)
		config_dvrs = config.get("dvrs", {})
		dvrs = {}
		for obj in self.obj:
			dvrs[obj.name] = {}
			dvrs[obj.name]['disk_limit'] = obj.disk_limit
			dvrs[obj.name]['dvr_limit'] = obj.dvr_limit
			dvrs[obj.name]['name'] = obj.name
			dvrs[obj.name]['root'] = obj.name + "/" + obj.root
			dvrs[obj.name]['disks'] = {}
			for item in obj.dvr_urls.all():
				dvrs[obj.name]['disks'][item.url] = {}
			dvrs[obj.name]['schedule'] = []
			for item in obj.dvr_schedule.all():
				dvrs[obj.name]['schedule'].append( [item.start, item.end] )
		self.delete_olds(config_dvrs, dvrs, self.server)
		config['dvrs'] = dvrs
		self.send_config(self.server, config)

	def delete_olds(self, old_config, new_config, server):
		#Получаешь старую и новую часть конфига с DVRS и сервер
		#Нужно отправить запросы на удаление DVR, если какой-то DVR есть в старом, но нет в новом
		pass 


class AuthRequest(BaseRequest):
	def __init__(self, server, obj):
		self.server = server
		self.obj = obj

	def update_auths(self):
		config = self.get_config(self.server)
		config_auth = config.get("auth_backends", {})
		auth_backends = {}
		for obj in self.obj:
			auth_backends[obj.name] = {}
			auth_backends[obj.name]['allow_default'] = obj.allow_default
			auth_backends[obj.name]['backends'] = []
			for item in obj.auth_urls.all():
				auth_backends[obj.name]['backends'].append( {'url':item.url} )
			auth_backends[obj.name]['name'] = obj.name
		self.delete_olds(config_auth, auth_backends, self.server)
		config['auth_backends'] = auth_backends
		self.send_config(self.server, config)

	def delete_olds(self, old_config, new_config, server):
		#Получаешь старую и новую часть конфига с AUTH и сервер
		#Нужно отправить запросы на удаление AUTH, если какой-то AUTH есть в старом, но нет в новом
		pass


class StreamRequest(BaseRequest):
	def __init__(self, stream_obj):
		self.pipeline = stream_obj.fluss_pipelines #пакет стримов
		self.servers = stream_obj.fluss_pipelines.fluss_servers.all() #список серверов
		self.stream_name = stream_obj.name #имя стрима
		self.stream_sourse = stream_obj.sourse #ссылка на стрим

	def update_stream(self):
		for server in self.servers:
			config = self.get_config(server)
			config['streams'] = config.get("steams", {})
			stream = {}
			stream['auth'] = {}
			stream['auth']['soft_limitation'] = True
			stream['auth']['url'] = server.auth_backends.all().first().auth_urls.all().first().url
			stream['name'] = self.stream_name
			config['streams'][self.stream_name] = stream
			if self.pipeline.is_archives:
				stream['dvr'] = {"root":server.dvr.all().first().root}
			config['streams'][self.stream_name]['urls'] = [{'url':self.stream_sourse}]
			self.send_config(server, config)

	# def delete_stream(self):
	# 	try:
	# 		for server in self.servers:
	# 			self.server_url = server.fluss_url
	# 			url = f"{self.server_url}/flussonic/api/config/stream_delete"
	# 			header = self.get_headers(server.login, server.password)
	# 			response = requests.post(url, headers=header, data=self.stream_name)
	# 			answer = response.json()
	# 	except:
	# 		return False
	# 	return True
