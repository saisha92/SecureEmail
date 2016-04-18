import os
import rsa
import smtplib
import base64
from Crypto.Cipher import AES
from Crypto import Random
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.application import MIMEApplication
import datetime

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
fromaddr = "fromaddr"
toaddr = "toaddr"
msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Secure Email"

MSG = ('RSA is an algorithm used by modern computers to encrypt and decrypt messages.'
       ' It is an asymmetric cryptographic algorithm. Asymmetric means that there are '
       'two different keys. This is also called public key cryptography, because one of '
       'them can be given to everyone. The other key must be kept private')

def send_email():
    body = 'The email contains 3 attachments, one is the encrypted message,the other is the signature and the 3rd is the key to decrypt the message'
    encrypt()
    part = MIMEApplication(open("personal.txt", "rb").read(), 'txt', name='message.txt')
    part2 = MIMEApplication(open("sign.txt", "rb").read(), 'txt', name='signature.txt')
    part3 = MIMEApplication(open("aes_key.txt", "rb").read(), 'txt', name='key.txt')
    part.add_header('Content-Disposition', 'attachment', filename="message.txt")
    part2.add_header('Content-Disposition', 'attachment', filename="signature.txt")
    part3.add_header('Content-Disposition', 'attachment', filename="key.txt")
    msg.attach(part)
    msg.attach(part2)
    msg.attach(part3)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(fromaddr, "password")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def get_keys():
    '''
    Get the receivers public key and the senders private key
    '''
    with open('recv_pubkey.pem') as publicfile:
        pkeydata = publicfile.read()
    recv_pubkey = rsa.PublicKey.load_pkcs1(pkeydata)
    with open('sender_private_key.pem') as privatefile:
        keydata = privatefile.read()
    senderprivkey = rsa.PrivateKey.load_pkcs1(keydata, 'PEM')
    return (recv_pubkey, senderprivkey)

def encrypt():
    '''
    Encryption
    '''
    date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    message = date
    message = message + "\n" +MSG
    raw = pad(message)
    recv_pubkey, senderprivkey = get_keys()
    aes_key = Random.new().read(AES.block_size)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    encoded = base64.b64encode(iv + cipher.encrypt(raw))
    crypto = rsa.encrypt(aes_key, recv_pubkey)
    fo = open("personal.txt", "w")
    fo.write(encoded)
    fo.close()
    signature = rsa.sign(message, senderprivkey, 'SHA-256')
    fsign = open("sign.txt", "w")
    fsign.write(signature)
    key = open("aes_key.txt", "w")
    key.write(crypto)
    fsign.close()
    key.close()

if __name__ == "__main__":
    send_email()
