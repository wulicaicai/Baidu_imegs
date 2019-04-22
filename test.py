import requests, json

l = dict()
l['url'] = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1555584822690&di=c91c1cbc0fb70b6939f859cda7dc945a&imgtype=0&src=http%3A%2F%2F0.image.al.okbuycdn.com%2Forg%2Fstatic%2F9fbd19e6db3f89ce4a4e05129254d69a.jpg'

k = json.dumps(l)
print(k)

x = requests.post(url='http://127.0.0.1:8000/register', data=k)
x = json.loads(x.text)
print(x)
