import os
import rsa
import base64
from Crypto.Cipher import AES

unpad = lambda s : s[:-ord(s[len(s)-1:])]

def decrypt(enc_key, crypto, signature):
    '''
    Decryption
    '''
    with open('recv_private_key.pem') as privatefile:
        keydata = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')
    aes_key = rsa.decrypt(enc_key, privkey)
    aes_decode = base64.b64decode(crypto)
    iv = aes_decode[:16]
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decoded = unpad(cipher.decrypt(aes_decode[16:]))
    print decoded
    with open('sender_pubkey.pem') as publicfile:
        pkeydata = publicfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(pkeydata)
    try:
        if rsa.verify(decoded, signature, pubkey):
            print 'Sender Authenticated'
    except Exception:
        print 'Sender is not Authenticated'

if __name__ == "__main__":

    file = open('message.txt', 'r')
    file2 = open('signature.txt','r')
    file3 = open('key.txt','r')
    crypto = file.read()
    aes_key = file3.read()
    signature = file2.read()
    file.close()
    file2.close()
    file3.close()
    decrypt(aes_key,crypto,signature)    
