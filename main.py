import json

import requests

url_ya = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
with open('env.txt', 'r') as f:
    token = f.readline().strip()
headers_ya = {'Authorization': f'OAuth {token}'}

image_label = input('Введите надпись для картинки:')
url_cats = f'https://cataas.com/cat/says/{image_label}'
params = {"json": "true"}
response = requests.get(url_cats,
                        params=params,
                        )
url = response.json()['url']
resp = requests.get(url, stream=True, allow_redirects=True)
file_size = resp.headers['Content-Length']

with open(f'images/{image_label}.jpg', 'wb') as f:
    f.write(resp.content)

params_ya = {'path':f'AIEPYAPI-158/{image_label}.jpg'}
r = requests.get(url_ya,
                 params=params_ya,
                 headers=headers_ya)
upload_url = r.json()['href']
with open(f'images/{image_label}.jpg', 'rb') as f:
    requests.put(upload_url, data=f)

with open('size.json', encoding='utf-8') as f:
    json_data = json.load(f)
json_data[f'{image_label}'] = f'{file_size}'
with open('size.json', 'w') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)


