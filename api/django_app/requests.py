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


class StreamRequest(BaseRequest):
	def __init__(self, stream_obj):
		self.servers = stream_obj.fluss_pipelines.fluss_servers.all() #список серверов
		self.stream_status = stream_obj.status #статус стрима
		self.stream_sourse = stream_obj.sourse #ссыылка на стрим
		self.stream_name = stream_obj.name #имя стрима
		self.config = self.get_config(self.servers[0]) #конфиг одного из сервера
		self.list_names = [item for item in self.config['streams']] #список стримов на сервере

	def is_exists(self):
		return bool(self.stream_name in self.list_names)

	def create_stream(self):
		tmp = f"{self.stream_sourse}; auth auth://catena.backend soft_limitation=true;"
		server_conf = "{url "+ f"{tmp}" + ";}"
		try:
			for server in self.servers:
				self.server_url = server.fluss_url
				url = f'{self.server_url}/flussonic/api/config/stream_create'
				data = f"stream {self.stream_name} {server_conf}"
				header = self.get_headers(server.login, server.password)
				response = requests.post(url, headers=header, data=data)
				answer = response.json()
		except:
			return False
		return True

	def delete_stream(self):
		try:
			for server in self.servers:
				self.server_url = server.fluss_url
				url = f"{self.server_url}/flussonic/api/config/stream_delete"
				header = self.get_headers(server.login, server.password)
				response = requests.post(url, headers=header, data=self.stream_name)
				answer = response.json()
		except:
			return False
		return True

	def change_url(self):
		try:
			for server in self.servers:
				self.server_url = server.fluss_url
				url = f'{self.server_url}/flussonic/api/modify_config?async=true'
				self.config['streams'].get(self.stream_name)['urls'][0]['url'] = self.stream_sourse
				header = self.get_headers(server.login, server.password)
				response = requests.post(url, headers=header, data = json.dumps(self.config))
				answer = response.json()
		except:
			return False
		return True

	def change_status(self):
		try:
			for server in self.servers:
				self.server_url = server.fluss_url
				url = f'{self.server_url}/flussonic/api/modify_config?async=true'
				self.config['streams'].get(self.stream_name)['disabled'] = not bool(int(self.stream_status))
				header = self.get_headers(server.login, server.password)
				response = requests.post(url, headers=header, data = json.dumps(self.config))
				answer = response.json()
		except:
			return False
		return True


class ArchiveRequest(BaseRequest):
	def __init__(self, archive_obj):
		self.archive = archive_obj
		self.servers = archive_obj.pipeline.fluss_servers.all() #список серверов
		print(self.servers)

	def create_archive(self):
		urls = [server.fluss_url for server in self.servers]
		for url in urls:
			config = self.get_config(url)
			dvrs = config.get("dvrs", None)
			if dvrs:
				print("Тут")
				# tmp = f'"disk_limit": {self.archive.disk_limit}, "dvr_limit": {self.archive.dvr_limit}, "name": {self.archive.name}, "root": {self.archive.root},'
				# data = f'"{self.archive.name}": ' + "{" + tmp + "},"
			# вставляе

