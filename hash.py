import json
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

random_gen = Random.new().read
print(random_gen)
rsa = RSA.generate(2048, random_gen)  # 获取秘钥对
private_pem = rsa.exportKey()  # 获取私钥
with open("private.pem", "wb") as f:
    f.write(private_pem)
public_pem = rsa.publickey().exportKey()  # 获取公钥
with open("public.pem", "wb") as f:
    f.write(public_pem)
# 加密
message = {"orderId": 9252678862671456643, "money": 50, "type": 2, "style": 241, 'userName': "241_liu924Wxy2"}
message = json.dumps(message)
rsaKey = RSA.importKey(open("public.pem").read())
cipher = Cipher_pkcs1_v1_5.new(rsaKey)  # 创建用于执行pkcs1_v1_5加密或解密的密码
cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))  # 加密的密文
print(cipher_text.decode('utf-8'))

# 解密
encrypt_text = cipher_text.decode('utf-8')
rsakey = RSA.importKey(open("private.pem").read())
cipher = Cipher_pkcs1_v1_5.new(rsakey)      # 创建用于执行pkcs1_v1_5加密或解密的密码
text = cipher.decrypt(base64.b64decode(encrypt_text), "解密失败")
print(text.decode('utf-8'))

# private_pem = rsa.exportKey() with open('private.pem', 'wb') as f: f.write(private_pem)
# public_pem = rsa.publickey().exportKey()with open('public.pem', 'wb') as f: f.write(public_pem)
