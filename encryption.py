from Crypto.Cipher import AES
import base64

def encrypt_message(message, key):

    cipher = AES.new(
        key,
        AES.MODE_EAX
    )

    ciphertext, tag = cipher.encrypt_and_digest(
        message.encode()
    )

    encrypted_data = (
        cipher.nonce +
        tag +
        ciphertext
    )

    return base64.b64encode(
        encrypted_data
    ).decode()


def decrypt_message(ciphertext, key):

    data = base64.b64decode(ciphertext)

    nonce = data[:16]

    tag = data[16:32]

    ciphertext = data[32:]

    cipher = AES.new(
        key,
        AES.MODE_EAX,
        nonce=nonce
    )

    message = cipher.decrypt_and_verify(
        ciphertext,
        tag
    )

    return message.decode()