import json

import requests
import rsa
import binascii

header = {
    'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6InRlc3QwMSIsImV4cCI6MTYyNjIzMzIyOCwiZW1haWwiOiIifQ.zpXFDD0o-Oz3Tz9F2TddfuksLXhm0ENAZ49aFhg42uw'
}
url1 = 'http://127.0.0.1:8005/info/dkinfo/'
response = requests.get(url=url1, headers=header)
datadict = json.loads(response.text)
print(datadict)

data2 = (datadict['data'])
print("获取加密后的原数据："+data2)
# 取出私钥
with open('dataprivate.pem', 'r') as file_pri:
    f_pri = file_pri.read()
prikey = rsa.PrivateKey.load_pkcs1(f_pri)
ret = binascii.unhexlify(data2)
length = len(ret)
val_list = []
for i in range(0, length, 128):
    tpl = ret[i:i + 128]
    val = rsa.decrypt(tpl, prikey)
    val_list.append(val)

ret = b''.join(val_list)
data2 = bytes.decode(ret)
print(data2)
