import json

import requests
import rsa
import binascii

url = 'http://127.0.0.1:8005/gettoken/'

#取出公钥
with open('public.pem', 'rb') as file_pub:
     f_pub = file_pub.read()
     pubkey = rsa.PublicKey.load_pkcs1(f_pub)

#  用户名
username = rsa.encrypt('test01'.encode('utf8'), pubkey)#使用公钥去加密字符串
# 16进制转ASCII码
username = binascii.hexlify(username)
# bytes转str
username = bytes.decode(username)

#  密码
password = rsa.encrypt('JSKJ9595'.encode('utf8'), pubkey)#使用公钥去加密字符串
# 16进制转ASCII码
password = binascii.hexlify(password)
# bytes转str
password = bytes.decode(password)
data = {
    'username': username,
    'password': password
}

response = requests.post(url=url, data=data)
datadict = json.loads(response.text)
print(datadict)