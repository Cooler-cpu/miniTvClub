import requests
import json
from datetime import datetime

from fluss_servers.models import Servers
from stream.models import Stream


def get_config():
  url = f"{server_url}/flussonic/api/read_config"
  response = requests.get(url, headers = headers)
  answer = response.json()
  return answer


def create_records():
  names = []
  for item in config['streams']:
    names.append(item)
  
  status = []
  urls = []
  for name in names:
    try:
      st = not config['streams'][name]['disabled']
    except:
      st = False
    ur = config['streams'][name]['urls'][0]['url']
    status.append(st)
    urls.append(ur)

  for i in range(0,len(names)):
    Stream.update_or_create(
      name = names[i],
      sourse = urls[i],
      fluss_server = Server.objects.get(fluss_url="http://a1.minitv.club:8080"),
      data_create = datetime.now(),
      status = status[i],
      identifier={'name', names[i]}
    )


if __name__ == '__main__':
  headers = {'Content-type': 'application/json',
        'Authorization': 'Basic dGVzdDp0ZXN0MTIz', 
        'Accept': 'text/plain',
        'Content-Encoding': 'utf-8'
        }
  server_url="http://a1.minitv.club:8080"
  config = get_config()
  create_records()