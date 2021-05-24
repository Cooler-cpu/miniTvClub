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


class AuthRequest(BaseRequest):
    def create_auth(self):
        print(self.server_auth) #массив auth
        print(self.server_auth[0].name)
        print(self.server_auth[0].position)
        print(self.server_auth[0].allow_default)
        print(self.server_auth[0].auth_urls.all()) #массив ссылок
        print(self.server_auth[0].auth_urls.all()[0].url) #первая ссылка массива ссылок нулевого объекта



class Server(AuthRequest):
    def __init__(self, obj):
        self.server = obj #объект текущего сервера
        self.server_dvr = obj.dvr #объект информации об архиве для текущего сервера
        self.server_auth = obj.auth.all() #объект авторизации для бэкенда для текущего сервера
        self.model = apps.get_model('fluss_servers','Servers') #модель сервера
        # auth_urls, dvrs_urls

    def is_exists(self):
        server_id = self.server.id
        if server_id:
            self.get_old_server_info(server_id)

    def get_server(self):
        server = self.model.objects.get(id=self.old_server_id)
        return server

    def get_old_server_info(self, old_id):
        self.old_server_id = old_id #id старого сервера
        self.old_server = self.get_server() #объект старого сервера
        self.old_server_auth = self.old_server.auth.all() #объект авторизации для бэкенда для старого сервера
        self.old_server_dvr = self.old_server.dvr #объект информации об архиве для старого сервера

    def start(self):
        self.create_auth()
        # self.delete_auth(self.server)
        # self.uppdate_auth(self.server)


        # auth_same = self.compare_objects(self.server_auth, self.old_server_auth)
        # print(auth_same)
        # if not self.old_server_id or not auth_same:
            # print('goo')

    # def compare_objects(self, obj1, obj2):
        # try:
        # for i in range(obj1.count()):
        #     values = [(k,v) for k,v in obj1[i].__dict__.items() if k != '_state']
        #     other_values = [(k,v) for k,v in obj2[i].__dict__.items() if k != '_state']
        #     if not values == other_values:
        #         return False
        # except:
            # return False
        # return True
        # return (obj1.__dist__ == obj2.__dist__)
        # values = [(k,v) for k,v in obj1.__dict__.items() if k != '_state']
        # other_values = [(k,v) for k,v in obj2.__dict__.items() if k != '_state']
        # return values == other_values
