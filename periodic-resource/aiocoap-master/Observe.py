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
    var=1
    protocol = yield from Context.create_client_context()

    while var < 5:
        print(1)
        request = Message(code=GET)
        request.set_request_uri('coap://[aaaa::212:4b00:f0e:7502]:5683/sensor/gyro/x')
        request.opt.observe = 0
    #Configure the IP address of the CoAP server here
    #Also, you may need to change the URL depending on the implementation of your CoAP server
    

        try:
            print(2)
            #response = yield from pcrotocol.request(request).response
            print("A")
            protocol_request = protocol.request(request)
            print("B")
            protocol_request.observation.register_callback(observation_callback)
            print("C")
            print(protocol_request)
            print(protocol_request.response)
            response = yield from protocol_request.response
            print("D")
        except Exception as e:
            print(3)
            print('Failed to fetch resource:')
            print(e)
        else:
          print(4)
          print("Sending all")
           #sock.sendall(response.payload)
          result = response.payload.decode('utf-8')
          print(result)
          #cut = result.split("|");
          myobj = {"ip_address": "ip_address",
               "data": result}
          #myobj = {"ip_address": cut[0],
          #     "data": cut[1]}
          header = {'Content-Type': 'application/json', 'Accept': 'application/json'}
          x = requests.post(url='http://3.129.101.239', data=json.dumps(myobj), headers=header)
          print(x.status_code, x.encoding, x.reason)
      #finally:
        #sock.close()
      #print("Request ok: %r" % response.payload)
        print(5)
        var = var + 1

def observation_callback(response):
  print("Callback: %r" % response.payload)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
