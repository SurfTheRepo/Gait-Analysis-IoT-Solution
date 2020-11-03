#!/usr/bin/env python3

import logging
import socket
import asyncio
import time
import json
import sys
import numpy as np
import requests
from aiocoap import *

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server_address = ('18.190.138.228', 80)
#sock.connect(server_address)
#print('connecting to {} port {}'.format(*server_address))
logging.basicConfig(level=logging.INFO)

res = []
@asyncio.coroutine
def main():
    x=1
    protocol = yield from Context.create_client_context()

    request = Message(code=GET)
    request.set_request_uri('coap://[aaaa::212:4b00:1204:dd72]:5683/sensor/gyro/x')
    request.opt.observe = 0
    #Configure the IP address of the CoAP server here
    #Also, you may need to change the URL depending on the implementation of your CoAP server
    

    try:
        #response = yield from pcrotocol.request(request).response
        protocol_request = protocol.request(request)
        protocol_request.observation.register_callback(observation_callback)
        response = yield from protocol_request.response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
      print("Sending all")
        #sock.sendall(response.payload)
      myobj = {"data": response.payload.decode('utf-8')}
      header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
      x = requests.post(url='http://18.190.138.228', data=json.dumps(myobj), headers=header)
      print(x.status_code, x.encoding, x.reason)
      #finally:
        #sock.close()
      #print("Request ok: %r" % response.payload)

def observation_callback(response):
  print("Callback: %r" % response.payload)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
