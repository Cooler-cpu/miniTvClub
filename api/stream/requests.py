import requests
import json


class StreamRequest:

	headers = {'Content-type': 'application/json',
				'Authorization': 'Basic dGVzdDp0ZXN0MTIz', 
				'Accept': 'text/plain',
				'Content-Encoding': 'utf-8'
				}

	def __init__(self, stream_name="", server_url="http://a1.minitv.club:8080"):
		self.stream_name = stream_name
		self.server_url = server_url
		self.sourse_conf = None
		self.list_names = self.get_streams()


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
		self.sourse_conf = f"ts{self.server_url}/play/{self.stream_name}?auth=login1:pass2"
		server_conf = "{url "+self.sourse_conf+"; auth auth://"+self.stream_name+".backend soft_limitation=true;}"
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