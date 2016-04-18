# SecureEmail

This is a simple project which allows users to send secure email through an email client of their choice (Gmail, Yahoo, etc).

# Idea behind the Project

The implementation is based on a hybrid cryptosystem as it combines the convenience of a public-key cryptosystem and efficiency of the symmetric key cryptosystem. The message is encrypted first using a symmetric key Algorithm (AES) and the key is encrypted using RSA and shared with the receiver.
Since the receiver needs to verify if the message has been sent by the person who he/she claims to be. This is achieved by using a RSA signature. This signature is encrypted by using SHA algorithm
To prevent Data replay attacks, we attach a timestamp along with the message. The timestamp is also encrypted along with the message.

# Running the Application

The Sender and Receiver must share the public keys before hand by some means (GPG is one way , https://www.gnupg.org/ ).
To send the email, add the message body in the encrypt_message.py and make the necessary changes
Then run `python encrypt_message.py`

To Decrypt, make sure you have the correct key names, then run `python decrypt_message.py`
