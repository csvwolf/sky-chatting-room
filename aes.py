# encoding:utf-8
from Crypto.Cipher import AES
from Crypto import Random

"""
加密模块
"""

def getPassword():
    return '1111111111111111'

def encrypt(data, password):
    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    iv = Random.new().read(bs)
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data = cipher.encrypt(pad(data))
    data = iv + data
    return data

def decrypt(data, password):
    bs = AES.block_size
    if len(data) <= bs:
        return data
    unpad = lambda s : s[0:-ord(s[-1])]
    iv = data[:bs]
    cipher = AES.new(password, AES.MODE_CBC, iv)
    data  = unpad(cipher.decrypt(data[bs:]))
    return data

if __name__ == '__main__':
    data = 'hello world'
    password = '1111111111111111' #16,24,32位长的密码
    encrypt_data = encrypt(data, password)
    print 'encrypt_data:', encrypt_data

    decrypt_data = decrypt(encrypt_data, password)
    print 'decrypt_data:', decrypt_data