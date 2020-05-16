import base64


def token_encode(username, password):
    message = '{}:{}'.format(username, password)

    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return base64_message


def token_decode_username(token):
    base64_bytes = token.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    username = message.split(':')[0]
    return username
