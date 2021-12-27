import sys
import json
import traceback

from decos import log
from errors import IncorrectDataRecivedError



def get_message(client):

    from common.variables import MAX_PACAGE_LEGTH
    from common.variables import ENCODING


    encoded_response = client.recv(MAX_PACAGE_LEGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise IncorrectDataRecivedError
    raise IncorrectDataRecivedError

@log
def send_meccage(sock, message):
    if not isinstance(message,dict):
        raise TypeError
    from common.variables import ENCODING
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)

