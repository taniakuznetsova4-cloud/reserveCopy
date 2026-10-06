import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('API_Token_Ya')
url_ya = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
headers_ya = {'Authorization': f'OAuth {token}'}

image_label = input('Введите надпись для картинки:')
url_cats = f'https://cataas.com/cat/says/{image_label}'
params = {"json": "true"}
response = requests.get(url_cats,
                        params=params,
                        )
if response.status_code != 200:
    print('Сайт cataas.com не отвечает')
else:
    url = response.json()['url']
    resp = requests.get(url, stream=True, allow_redirects=True)
    file_size = resp.headers['Content-Length']
    f = resp.content
    params_ya = {'path':f'AIEPYAPI-158/{image_label}.jpg'}
    r = requests.get(url_ya,
                 params=params_ya,
                 headers=headers_ya)
    if r.status_code != 200:
        print('Сайт yandex не отвечает')
    else:
        upload_url = r.json()['href']
        requests.put(upload_url, data=f)
        if os.path.isfile("size.json"):
            with open('size.json', encoding='utf-8') as f:
                json_data = json.load(f)
        else:
            json_data = {}
        json_data[f'{image_label}'] = f'{file_size}'
        with open('size.json', 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)


