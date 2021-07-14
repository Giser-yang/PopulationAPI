import binascii
import datetime
import json
import time as time1

import pymssql
import rsa
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from django.db import models

# 超级用户 test01 JSKJ9595
# Create your views here.
# 取出数据加密公钥
from DKPop import models

with open('datapublic.pem', 'rb') as file_pub:
    f_pub = file_pub.read()
    datapubkey = rsa.PublicKey.load_pkcs1(f_pub)

# 取出用户信息解密私钥
with open('private.pem', 'r') as file_pri:
    f_pri = file_pri.read()
    prikey = rsa.PrivateKey.load_pkcs1(f_pri)


# 用户名密码长度不超过117字符，所以直接进行RSA加密解密，无需分段
def user_login(request):
    if request.method == 'POST':
        username = bytes(request.POST['username'], encoding='utf8')
        username = binascii.unhexlify(username)
        password = bytes(request.POST['password'], encoding='utf8')
        password = binascii.unhexlify(password)
        username = rsa.decrypt(username, prikey).decode()  # 用私钥去解密
        password = rsa.decrypt(password, prikey).decode()  # 用私钥去解密
        if username is None or password is None:
            return JsonResponse({'code': 500, 'message': '请求参数错误'})
        is_login = authenticate(request, username=username, password=password)
        if is_login is None:
            return JsonResponse({'code': 500, 'message': '账号或密码错误'})
        login(request, is_login)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(is_login)
        token = jwt_encode_handler(payload)
        return JsonResponse(
            {
                'code': 200,
                'message': 'Login successful',
                'data': {'token': token}
            }
        )
    else:
        return JsonResponse(
            {
                'code': 400,
                'message': 'Login failed',
                'data': 'Error request method!'
            }
        )


# 下面的3个装饰器全部来自from引用，相当与给接口增加了用户权限校验和token校验
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def get_info(request):
    data = 'some info'
    # 数据加密
    data = rsa.encrypt(data.encode('utf8'), datapubkey)  # 使用公钥去加密字符串
    # 16进制转ASCII码
    data = binascii.hexlify(data)
    # bytes转str
    data = bytes.decode(data)
    return JsonResponse(
        {
            'code': 200,
            'message': '请求成功',
            'data': data
        }
    )


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def dkdata(request):
    conn = pymssql.connect(host='localhost', user='sa', password='JSKJ9595', database='APIData', port=1433)
    cursor = conn.cursor()
    sql = 'SELECT Id,Time,Code,Name  FROM [DKPopulation] where Id<=100'
    cursor.execute(sql)
    data = dictfetchall(cursor)
    conn.commit()
    cursor.close()
    conn.close()
    datastr = Dataencry(data)
    return JsonResponse(
        {
            'code': 200,
            'message': '请求成功',
            'data': datastr
        }
    )


# 将返回结果转换成字典
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# 将字典列表转换成字符串进行分段加密并返回加密后的字符串
def Dataencry(dictlist):
    data = str(dictlist)
    data1 = data.encode('utf8')
    length = len(data1)
    val_list = []
    for i in range(0, length, 117):
        tpl = data1[i:i + 117]
        val = rsa.encrypt(tpl, datapubkey)
        val_list.append(val)
    ret = b''.join(val_list)
    asc1 = binascii.hexlify(ret)
    # bytes转str
    datastr = bytes.decode(asc1)
    return datastr


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JSONWebTokenAuthentication,))
def query_cqrk(request):
    timeStamp = int(request.POST['timestamp'])
    code = request.POST['code']
    timeArray = time1.localtime(timeStamp)
    Time = time1.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    data = {}
    rk = models.Cqdkpopulation.objects.filter(time=Time, code=code).values()
    # data['result'] = json.loads(serializers.serialize("json", rk))
    data = list(rk)
    data = Dataencry(data)
    # print(data)
    return JsonResponse(
        {
            'code': 200,
            'message': '请求成功',
            'data': data
        }
    )
