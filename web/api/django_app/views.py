from django.views.generic import View
from django.http import HttpResponse
import requests
import json
from datetime import datetime

from fluss_servers.models import Servers
from fluss_streams.models import Streams


class Load(View):
    def get(self, request):
        self.headers = {'Content-type': 'application/json',
                'Authorization': 'Basic dGVzdDp0ZXN0MTIz', 
                'Accept': 'text/plain',
                'Content-Encoding': 'utf-8'
                }
        self.server_url="http://a1.minitv.club:8080"
        self.config = self.get_config()
        self.create_records()
        return HttpResponse("<h1>Стримы были обновлены</h1>")

    def get_config(self):
        url = f"{self.server_url}/flussonic/api/read_config"
        response = requests.get(url, headers = self.headers)
        answer = response.json()
        return answer

    def create_records(self):
        names = []
        for item in self.config['streams']:
            names.append(item)
    
        status = []
        urls = []
        for name in names:
            try:
                print(self.config['streams'][name])
                st = not self.config['streams'][name]['disabled']
            except:
                st = True
            ur = self.config['streams'][name]['urls'][0]['url']
            status.append(st)
            urls.append(ur)

        print(status)
        for i in range(0,len(names)):
            Streams.objects.update_or_create(
                name = names[i],
                defaults={
                    'sourse' : urls[i],
                    'fluss_server' : Servers.objects.get(fluss_url="http://a1.minitv.club:8080"),
                    'data_create' : datetime.now(),
                    'status' : status[i],
                }
            )
