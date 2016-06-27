from flask import Flask, request
from xkcd_colors import xkcd_names_to_hex
import socket

PORT = 8000
IP_ADDRESS = '192.168.1.100'
START_CODE = 'PLAY_SHOW'
END_CODE = '\n'

app = Flask(__name__)
# For debugging:
# app.config['PROPAGATE_EXCEPTIONS'] = True

# Include "no-cache" header in all POST responses
@public.after_request
def add_no_cache(response):
    if request.method == 'POST':
        response.cache_control.no_cache = True
return response

@app.route('/sms', methods=['POST'])
def parse_sms():
    message = request.form['Body']
    print("Received text message: " + str(message))
    color = xkcd_names_to_hex[str(message.lower())]
    cmd = START_CODE + color + END_CODE
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(cmd.encode(), (IP_ADDRESS, PORT))
    print('Sent over UDP: {0}'.format(cmd))
    return ('<?xml version="1.0" encoding="UTF-8" ?><Response></Response>')
