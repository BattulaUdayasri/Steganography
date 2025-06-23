from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import base64

def derive_key(password):
    return SHA256.new(password.encode()).digest()  # 32-byte key

def encrypt_message(message, password):
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

def decrypt_message(ciphertext, password):
    key = derive_key(password)
    raw = base64.b64decode(ciphertext)
    iv = raw[:16]
    ct = raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')
