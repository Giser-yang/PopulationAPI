import binascii

import rsa

# (publickey, privatekey) = rsa.newkeys(1024)  # 对数字1000加密得到公钥和私钥
# pub = publickey.save_pkcs1()  # 获取公钥
# # 将公钥保存到文件*************
# filepub = open("datapublic.pem", 'wb+')
# filepub.write(pub)
# filepub.close()
#
# pri = privatekey.save_pkcs1()  # 获取私钥
# # 将私钥保存到文件***********
# filepri = open('dataprivate.pem', 'wb+')
# filepri.write(pri)
# filepri.close()


#
# # 取出公钥
# with open('public.pem', 'rb') as file_pub:
#     f_pub = file_pub.read()
#     pubkey = rsa.PublicKey.load_pkcs1(f_pub)
#
# # 取出私钥
# with open('private.pem', 'r') as file_pri:
#     f_pri = file_pri.read()
#     prikey = rsa.PrivateKey.load_pkcs1(f_pri)
#
#
#
# string = "test01"  # 待加密的字符串
#
#
# # 加密字符串string
#
# crypt = rsa.encrypt(string.encode('utf8'), pubkey)  # 使用公钥去加密字符串
#
#
#
# # 解密
# de_crypt = rsa.decrypt(crypt, prikey).decode()  # 用私钥去解密
#
# # 解出来的de_crypt与string应该是相等的，判断一下
# print(crypt)
# print(type(crypt))
# print(de_crypt)


data = 'some info'
# 取出公钥
with open('datapublic.pem', 'rb') as file_pub:
    f_pub = file_pub.read()
    pubkey = rsa.PublicKey.load_pkcs1(f_pub)
# 数据加密
data = rsa.encrypt(data.encode('utf8'), pubkey)  # 使用公钥去加密字符串
# 16进制转ASCII码
data = binascii.hexlify(data)
# bytes转str
data = bytes.decode(data)
print(data)


# 取出私钥
with open('dataprivate.pem', 'r') as file_pri:
    f_pri = file_pri.read()
prikey = rsa.PrivateKey.load_pkcs1(f_pri)
data1 = binascii.unhexlify(data)
data1 = rsa.decrypt(data1, prikey).decode()  # 用私钥去解密
print(data1)