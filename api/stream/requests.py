import requests
import json


class StreamRequest:

	headers = {'Content-type': 'application/json',
				'Authorization': 'Basic dGVzdDp0ZXN0MTIz', 
				'Accept': 'text/plain',
				'Content-Encoding': 'utf-8'
				}

	def __init__(self, stream_status, stream_name="", stream_sourse="", server_url="http://a1.minitv.club:8080"):
		self.stream_status = stream_status
		self.stream_sourse = stream_sourse
		self.stream_name = stream_name
		self.server_url = server_url
		self.sourse_conf = None
		self.list_names = self.get_streams()
		self.config = self.get_config()


	def get_streams(self):
		list_names = []
		url = f"{self.server_url}/flussonic/api/media"
		response = requests.get(url, headers=self.headers)
		answer = response.json()
		for stream in answer:
			list_names.append(stream["value"]["name"])
		return list_names


	def is_exists(self):
		return bool(self.stream_name in self.list_names)


	def create_stream(self):
		tmp = f"{self.stream_sourse}; auth auth://catena.backend soft_limitation=true;"
		server_conf = "{url "+ f"{tmp}" + ";}"
		url = f'{self.server_url}/flussonic/api/config/stream_create'
		data = f"stream {self.stream_name} {server_conf}"
		response = requests.post(url, headers=self.headers, data=data)
		answer = response.json()
		print(answer)
		return answer


	def delete_stream(self):
		url = f"{self.server_url}/flussonic/api/config/stream_delete"
		response = requests.post(url, headers=self.headers, data=self.stream_name)
		answer = response.json()
		print(answer)


	def get_config(self):
		url = f"{self.server_url}/flussonic/api/read_config"
		response = requests.get(url, headers = self.headers)
		answer = response.json()
		return answer


	def change_url(self):
		url = f'{self.server_url}/flussonic/api/modify_config?async=true'
		self.config['streams'].get(self.stream_name)['urls'][0]['url'] = self.stream_sourse
		response = requests.post(url, headers=self.headers, data = json.dumps(self.config))
		answer = response.json()
		print(answer)


	def change_status(self):
		url = f'{self.server_url}/flussonic/api/modify_config?async=true'
		self.config['streams'].get(self.stream_name)['disabled'] = not bool(int(self.stream_status))
		response = requests.post(url, headers=self.headers, data = json.dumps(self.config))
		answer = response.json()
		print(answer)