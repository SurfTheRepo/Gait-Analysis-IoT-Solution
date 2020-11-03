# Gait-Analysis-IoT-Solution

## How to Use coAP server 

There are two parts to the sensor reading solution.

1. The Python Script called Observe.py which is located in the aiocoap-master folder
- This script performs a GET request to the coap Server. It grabs and sends the data to Michaels AWS site.
- Currently it is Configured for my (Stephen) sensor Tag

2. The coAP Server.
- The Server is found in er-server-example.c. The Resource is in Resources/toggle.c

HOW TO:

RUN the coAP server with the RPL border router.

Then run Python Script like so: python3 Observe.py

Wolla! Data is sent to the server at 50 Hertz, About 3 Seconds
