#!/usr/bin/env python3

# This file is part of the Python aiocoap library project.
#
# Copyright (c) 2012-2014 Maciej Wasilak <http://sixpinetrees.blogspot.com/>,
#               2013-2014 Christian Amsüss <c.amsuess@energyharvesting.at>
#
# aiocoap is free software, this file is published under the MIT license as
# described in the accompanying LICENSE file.

import logging
import asyncio
import time
import sys
import numpy as np
from aiocoap import *

logging.basicConfig(level=logging.INFO)

res = []
@asyncio.coroutine
def main():
    x=1
    reading_interval = 1 #The time interval between each GET request in second
    reading_num = 11 #How many RSSI samples you try to get? 

    while x<reading_num:
        protocol = yield from Context.create_client_context()

        request = Message(code=GET)
        #Configure the IP address of the CoAP server here
        #Also, you may need to change the URL depending on the implementation of your CoAP server
        request.set_request_uri('coap://[aaaa::212:4b00:1204:dd72]:5683/test/hello')

        try:
            response = yield from protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            #print('Result: %s\n%r'%(response.code, response.payload))
            #Get the RSSI value from the payload
            print(response.payload.decode('utf-8'))
            res.append(float(response.payload.decode('ascii')[0:3]))
        x=x+1
        #put into sleep
        time.sleep(reading_interval)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
    print(res)
    # Ax = b solve for x
    b = np.array(res)
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    A = np.vstack([x, np.ones(len(x))]).T
    a, c = np.linalg.lstsq(A, b, rcond=1.e-10)[0]
    print(a, c)
    
    
