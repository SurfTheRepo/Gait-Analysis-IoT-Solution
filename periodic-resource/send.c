/*
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the Institute nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE INSTITUTE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE INSTITUTE OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 *
 * This file is part of the Contiki operating system.
 *
 */

#include "contiki.h"
#include "contiki-lib.h"
#include "contiki-net.h"
#include "sys/timer.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#define DEBUG DEBUG_PRINT
#include "net/ip/uip-debug.h"
#include "dev/leds.h"
#include "board-peripherals.h"

#define MAX_PAYLOAD_LEN 250
#define UDP_HDR ((struct uip_udpip_hdr *) &uip_buf[UIP_LLH_LEN])

static struct uip_conn *server_conn;

static struct tcp_socket socket;

#define INPUTBUFSIZE 400
static uint8_t inputbuf[INPUTBUFSIZE];

#define OUTPUTBUFSIZE 1200
static int indexVal = 0;
static int sendval[950];

static uint8_t outputbuf[OUTPUTBUFSIZE];
PROCESS(tcp_process, "TCP server process");
AUTOSTART_PROCESSES(&resolv_process,&tcp_process);
/*---------------------------------------------------------------------------*/
static struct ctimer timer_ctimer;		//Callback Timer
static int counter_ctimer;
static void
takeReadings() {
	if (!(counter_ctimer >= 75)) {
  ctimer_reset(&timer_ctimer);
	}	
		int gyroX = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_X);
		int gyroY = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Y);
		int gyroZ = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Z);
		int accX = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_X);
		int accY = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Y);
		int accZ = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Z);
		
		sendval[indexVal] = gyroX;
		sendval[indexVal+1] = gyroY;
    sendval[indexVal+2] = gyroZ;
		sendval[indexVal+3] = accX;
		sendval[indexVal+4] = accY;
    sendval[indexVal+5] = accZ;
		indexVal += 6;
  counter_ctimer++;
}
static void
tcpip_handler(process_event_t ev, process_data_t data)
{
	 char *str;
  	char buf[MAX_PAYLOAD_LEN];
}
static void
event (struct tcp_socket *s, void *ptr, tcp_socket_event_t ev)
{
	printf("event %d\n", ev);
}
/*---------------------------------------------------------------------------*/
static void
print_local_addresses(void)
{
  int i;
  uint8_t state;

  PRINTF("Server IPv6 addresses: ");
  for(i = 0; i < UIP_DS6_ADDR_NB; i++) {
    state = uip_ds6_if.addr_list[i].state;
    if(uip_ds6_if.addr_list[i].isused &&
       (state == ADDR_TENTATIVE || state == ADDR_PREFERRED)) {
      PRINT6ADDR(&uip_ds6_if.addr_list[i].ipaddr);
      PRINTF("\n\r");
    }
  }
}
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(tcp_process, ev, data)
{
 uip_ipaddr_t ipaddr;
	uint16_t port = 5555;

  PROCESS_BEGIN();
	mpu_9250_sensor.configure(SENSORS_ACTIVE, MPU_9250_SENSOR_TYPE_ALL);
  PRINTF("TCP starting\n\r");


  print_local_addresses();
  //Create a tcp socket and connect to remote host
	uip_ipaddr_t addr;
	uip_ip6addr(&addr, 0xaaaa, 0, 0, 0, 0, 0, 0, 1);
	int reg = tcp_socket_register(&socket, NULL, inputbuf, sizeof(inputbuf), outputbuf, sizeof(outputbuf), NULL, event);
	int connection = tcp_connect(&addr,  UIP_HTONS(port), NULL);
	
	printf("Connecting...\n");
	PROCESS_WAIT_EVENT_UNTIL(ev == tcpip_event);
	ctimer_set(&timer_ctimer, CLOCK_SECOND / 50, takeReadings, NULL);
	
	if (uip_aborted() || uip_timedout() || uip_closed()) {
		printf("could not establish connection\n");
	} else if (uip_connected()) {
		printf("Connected\n");
	}
	printf("register: %d, Connect: %d\n",reg, connection);
	
	
  	while(1) {
		
		 PROCESS_YIELD();
		//Wait for tcipip event to occur
		// Start sending
		printf("IndexVal: %d\n\r", indexVal);
		if (indexVal >= 450) {
			printf("IndexVal: %d\n\r", indexVal);
			int count = 0;
			if (count <= 450) {
				printf("count: %d\n\r",count);
				while(count <= 200) {	
						char buf[30];	
						sprintf(buf, "ax%day%daz%dgz%dgy%dgz%d", sendval[count], sendval[count+1], sendval[count+2], sendval[count+3], sendval[count+4], sendval[count+5]);
					strcat((char*)outputbuf, buf);
					printf("count: %d\n\r",count);
					printf("BUF: %s\n\r", (char*)outputbuf);
					count += 6;
				}
				uip_send(outputbuf, 1200);
				}
				count = 0;
				break;
			}
		

	}

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/
