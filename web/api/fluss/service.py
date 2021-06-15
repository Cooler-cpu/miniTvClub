from django.apps import apps
import requests
import json
from requests.auth import _basic_auth_str
from django.core.exceptions import ValidationError

class HeaderRequest:
	def get_headers(self, login=None, password=None):
		headers = {'Content-type': 'application/json',
					'Authorization': _basic_auth_str(login, password), 
					'Accept': 'text/plain',
					'Content-Encoding': 'utf-8'}
		return headers


class BaseRequest(HeaderRequest):
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
		dvrs[self.obj.name] = {}
		dvrs[self.obj.name]['disk_limit'] = self.obj.disk_limit
		dvrs[self.obj.name]['dvr_limit'] = self.obj.dvr_limit
		dvrs[self.obj.name]['name'] = self.obj.name
		dvrs[self.obj.name]['root'] = self.obj.name + "/" + self.obj.root
		dvrs[self.obj.name]['disks'] = {}
		for item in self.obj.dvr_urls.all():
			dvrs[self.obj.name]['disks'][item.url] = {}
		dvrs[self.obj.name]['schedule'] = []
		for item in self.obj.dvr_schedule.all():
			dvrs[self.obj.name]['schedule'].append( [item.start, item.end] )
		config['dvrs'] = dvrs
		self.send_config(self.server, config)


class AuthRequest(BaseRequest):
	def __init__(self, server, obj):
		self.server = server
		self.obj = obj

	def update_auths(self):
		config = self.get_config(self.server)
		config_auth = config.get("auth_backends", {})
		auth_backends = {}
		for item in config_auth:
			auth_backends[item] = None
		for obj in self.obj:
			auth_backends[obj.name] = {}
			auth_backends[obj.name]['allow_default'] = obj.allow_default
			auth_backends[obj.name]['backends'] = []
			for item in obj.auth_urls.all():
				auth_backends[obj.name]['backends'].append( {'url':obj.name + "/" + item.url} )
			auth_backends[obj.name]['name'] = obj.name
		config['auth_backends'] = auth_backends
		self.send_config(self.server, config)


class StreamRequest(BaseRequest):
	def __init__(self, stream_obj):
		self.pipeline = stream_obj.fluss_pipelines #пакет стримов
		self.servers = stream_obj.fluss_pipelines.fluss_servers.all() #список серверов
		self.stream_name = stream_obj.name #имя стрима
		self.stream_sourse = stream_obj.sourse #ссылка на стрим
		self.archive_servers = stream_obj.servers_archive #сервер с архивом

	def update_stream(self):
		for server in self.servers:
			config = self.get_config(server)
			config['streams'] = config.get("steams", {})
			stream = {}
			stream['auth'] = {}
			stream['auth']['soft_limitation'] = True
			stream['auth']['url'] = f"auth://{server.auth_backends.all().first().name}"
			stream['name'] = self.stream_name
			config['streams'][self.stream_name] = stream
			if server == self.archive_servers:
				if server.dvr:
					stream['dvr'] = {"reference":server.dvr.name}
			else:
				stream['dvr'] = None
			config['streams'][self.stream_name]['urls'] = [{'url':self.stream_sourse}]
			print(config['streams'])
			self.send_config(server, config)
