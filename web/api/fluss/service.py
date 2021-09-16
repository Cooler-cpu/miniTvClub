from django.apps import apps
import requests
import json
from requests.auth import _basic_auth_str
from django.core.exceptions import ValidationError
from django.http import Http404


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
		try:
			response = requests.get(url, headers = header)
			answer = response.json()
			return answer 
		except Exception:
			# raise ValidationError("Сервер не работает")
			return False


	def send_config(self, server, config):
		url = f'{server.fluss_url}/flussonic/api/modify_config?async=true'
		header = self.get_headers(server.login, server.password)
		response = requests.post(url, headers=header, data = json.dumps(config))
		answer = response.json()


class ArchivesRequest(BaseRequest):
	def __init__(self, servers = None):
		self.servers = servers

	def update_archive(self):
		for server in self.servers:
			config = self.get_config(server)
			if config:
				config_dvrs = config.get("dvrs", {})
				dvrs = {}
				for item in config_dvrs:
					dvrs[item] = None
				objs = server.server_dvr.all()
				for obj in objs:
					dvrs[obj.name] = {}
					dvrs[obj.name]['disk_limit'] = obj.disk_limit
					dvrs[obj.name]['dvr_limit'] = obj.dvr_limit
					dvrs[obj.name]['name'] = obj.name
					dvrs[obj.name]['root'] = obj.root
					dvrs[obj.name]['disks'] = {}
					for item in obj.dvr_urls.all():
						dvrs[obj.name]['disks'][item.url] = {}
				config['dvrs'] = dvrs
				self.send_config(server, config)

	def update_schedule(self, server, dvr):
		config = self.get_config(server)
		config['dvrs'][dvr.name]['schedule'] = []
		for item in dvr.dvr_schedule.all():
			time_start = item.start.strftime('%H:%M').split(':')
			time_end = item.end.strftime('%H:%M').split(':')
			time_start = time_start[0] + time_start[1]
			time_end = time_end[0] + time_end[1]
			config['dvrs'][dvr.name]['schedule'].append([time_start, time_end])
		self.send_config(server, config)

	def delete_archive(self, archive):
		for server in self.servers:
			archives = server.get_dvrs()
			if archives.get(name = archive.name):
				config = self.get_config(server)
				if config:
					config_archive = config.get("dvrs", {})
					archive_name = archive.name
					config_archive[archive_name] = None
					config['dvrs'] = config_archive
					self.send_config(server, config)


class AuthRequest(BaseRequest):
	def __init__(self, servers):
		self.servers = servers

	def update_auths(self):
		for server in self.servers:
			auths = server.auth_backends.all()
			config = self.get_config(server)
			if config:
				config_auth = config.get("auth_backends", {})
				auth_backends = {}
				for item in config_auth:
					auth_backends[item] = None
				for obj in auths:
					auth_backends[obj.name] = {}
					auth_backends[obj.name]['allow_default'] = obj.allow_default
					auth_backends[obj.name]['backends'] = []
					for item in obj.auth_urls.all():
						auth_backends[obj.name]['backends'].append( {'url':item.url} )
					auth_backends[obj.name]['name'] = obj.name
				config['auth_backends'] = auth_backends
				self.send_config(server, config)
				return {'status': True}
			return {'status': False}

	def delete_auth(self, auth):
		for server in self.servers:
			auth_backends = server.auth_backends.all()
			if auth_backends.get(name = auth):
				config = self.get_config(server)
				config_auth = config.get("auth_backends", {})
				auth_name = auth.name
				config_auth[auth_name] = None
				config['auth_backends'] = config_auth
				self.send_config(server, config)


class StreamRequest(BaseRequest):
	def __init__(self, stream_obj):
		self.pipeline = stream_obj.fluss_pipelines #пакет стримов
		self.servers = stream_obj.fluss_pipelines.fluss_servers.all() #список серверов
		self.stream_name = stream_obj.name #имя стрима
		self.stream_sourse = stream_obj.sourse #ссылка на стрим
		self.archive = stream_obj.archive #архив

	def update_stream(self):
		for server in self.servers:
			config = self.get_config(server)
			config['streams'] = config.get("streams", {})
			stream = {}
			stream['auth'] = {}
			stream['auth']['soft_limitation'] = True
			stream['auth']['url'] = f"auth://{server.auth_backends.all().first().name}"
			stream['name'] = self.stream_name
			config['streams'][self.stream_name] = stream
			if self.archive in server.get_dvrs():
				stream['dvr'] = {"reference":self.archive.name}
			else:
				stream['dvr'] = None
			config['streams'][self.stream_name]['urls'] = [{'url':self.stream_sourse}]
			self.send_config(server, config)

	def update_locale_dvr_limit(self, stream, sec_dvr_limit):
		for server in self.servers:
			config = self.get_config(server)
			if config:
				key_dvr = 'dvr'
				if key_dvr in config['streams'][self.stream_name]:
					config['streams'][self.stream_name]['dvr']['dvr_limit'] = sec_dvr_limit
					self.send_config(server, config)

	# def delete_locale_dvr_limit(self):
	# 	for server in self.servers:
	# 		config = self.get_config(server)
	# 		if config: 
	# 			key_dvr = 'dvr'
	# 			if key_dvr
	
			
	def delete_stream(self):
		for server in self.servers:
			config = self.get_config(server)
			config['streams'][self.stream_name] = None
			self.send_config(server, config)