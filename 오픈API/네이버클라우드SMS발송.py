import requests
import json
import time
import base64
import hmac
import hashlib

serviceId = 'SERVICE_ID'
url = 'https://sens.apigw.gov-ntruss.com/sms/v2/services/' + serviceId + '/messages'


def make_signature():
    timestamp = str(int(time.time() * 1000))

    access_key = "ACCESS_KEY"   # access key id (from portal or sub account)
    secret_key = "SECRET_KET"   # secret key (from portal or sub account)
    secret_key = bytes(secret_key, 'UTF-8')

    # 그지같은 안되는 코드 네이버 튜터리얼 누구냐
    # method = "GET"
    # uri = "/photos/puppy.jpg?query1=&query2"
    
    method = "POST"
    uri = '/sms/v2/services/' + serviceId + '/messages'

    message = method + " " + uri + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    print('signingKey: ', signingKey)
    return signingKey


timestamp = str(int(time.time() * 1000))
key = make_signature()

headers = {
    'Content-Type' : 'application/json; charset=utf-8',
    'x-ncp-apigw-timestamp' : timestamp,
    'x-ncp-iam-access-key' : 'D8095CC96E982FF7BADE',
    'x-ncp-apigw-signature-v2' : key
}

body = {
    "type":"SMS",
    "contentType":"COMM",
    "countryCode":"82",
    "from":"SENDER-NUMBER",
    "content":"내용1234",
    "messages":[
        {
            "to":"RECEIVER-NUMBER",
            # "content":"위의 content와 별도로 해당 번호로만 보내는 내용(optional)"
        }
    ]
}

res = requests.post(url,
                    headers=headers,
                    data=json.dumps(body))

print(url)
print(res.request)
print(res.status_code)
print(res.json())
