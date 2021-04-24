import json
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, quote

addr = '서울특별시 압구정동 현대아파트'
vworld_apikey = '발급받은인증키'
url = "http://api.vworld.kr/req/address?service=address&request=getCoord&type=ROAD&refine=false&key=%s&" % (vworld_apikey) + urlencode({quote_plus('address'):addr}, encoding='UTF-8')
print(url)

request = Request(url)
response = urlopen(request)
rescode = response.getcode()
print(response)
if rescode == 200:
  response_body = response.read().decode('utf-8')
else:
  print('error code:', rescode)

jsonData = json.loads(response_body)
lat = float(jsonData['response']['result']['point']['y'])
lng = float(jsonData['response']['result']['point']['x'])
print('lat:{}, lng:{}'.format(lat, lng))