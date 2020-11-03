/*
 * Copyright (c) 2013, Institute for Pervasive Computing, ETH Zurich
 * All rights reserved.
 *
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
 */

/**
 * \file
 *      Example resource
 * \author
 *      Matthias Kovatsch <kovatsch@inf.ethz.ch>
 */

#include "contiki.h"


#include <string.h>
#include "contiki.h"
#include "rest-engine.h"
#include "dev/leds.h"
#include "board-peripherals.h"
#include <limits.h>

#define CHUNKS_TOTAL    4200
#define MAX_AGE      60
static void res_get_handler_x(void *request, void *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset);

static struct ctimer timer_ctimer;		//Callback Timer
static int counter_ctimer;
 // hold timer vals
static int n;

static int indexVal = 0;
static int sendval[900];
static int interval_counter = 0;
static int count = 0;

 // hold timer vals
/*
 * Use local resource state that is accessed by res_get_handler() and altered by res_periodic_handler() or PUT or POST.
 */
static int32_t event_counter = 0;
static void res_periodic_handler(void);
PERIODIC_RESOURCE(res_mpu_x,
         "title=\"Gyro-x\";rt=\"Gyro\";obs",
         res_get_handler_x,
         NULL,
         NULL,
         NULL,
         CLOCK_SECOND / 50,
         res_periodic_handler);

// GYRO Sensors
/*---------------------------------------------------------------------------*/

static void
res_get_handler_x(void *request, void *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset)
{	
	
	int gyroX = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_X);
	int gyroY = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Y);
	int gyroZ = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Z);
	int accX = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_X);
	int accY = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Y);
	int accZ = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Z);

  char *str;
	unsigned int accept = -1;
  REST.get_header_accept(request, &accept);

	REST.set_header_content_type(response, REST.type.TEXT_PLAIN);
	REST.set_header_max_age(response, MAX_AGE);
	// Chunks
	int32_t strpos = 0;
	
	//ctimer_set(&timer_ctimer, CLOCK_SECOND / 50, updateTime, NULL);
  /* Check the offset for boundaries of the resource data. */
  if(*offset >= CHUNKS_TOTAL) {
    REST.set_response_status(response, REST.status.BAD_OPTION);
    /* A block error message should not exceed the minimum block size (16). */

    const char *error_msg = "BlockOutOfScope";
    REST.set_response_payload(response, error_msg, strlen(error_msg));
    return;
  }

  /* Generate data until reaching CHUNKS_TOTAL. */
	// Fill the Buffer at a rate of 50 Hertz
  while(strpos < preferred_size) {
		strpos += snprintf((char *)buffer + strpos, preferred_size - strpos + 1,  "ax%day%daz%dgx%dgy%dgz%d", gyroX, gyroY, gyroZ, accX, accY, accZ);
  }

  /* snprintf() does not adjust return value if truncated by size. */
  if(strpos > preferred_size) {
    strpos = preferred_size;
    /* Truncate if above CHUNKS_TOTAL bytes. */
  }
  if(*offset + (int32_t)strpos > CHUNKS_TOTAL) {
    strpos = CHUNKS_TOTAL - *offset;
  }
  REST.set_response_payload(response, buffer, strpos);

  /* IMPORTANT for chunk-wise resources: Signal chunk awareness to REST engine. */
  *offset += strpos;

  /* Signal end of resource representation. */
  if(*offset >= CHUNKS_TOTAL) {
    *offset = -1;
  }
}
static void
res_periodic_handler()
{	
		/*int gyroX = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_X);
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
		printf("interval_Count: %d, ax%day%daz%dgx%dgy%dgz%d\n\r", interval_counter, sendval[indexVal], sendval[indexVal+1], sendval[indexVal+2], sendval[indexVal+3], sendval[indexVal+4], sendval[indexVal+5]);*/
  ++interval_counter;
		
 // if(interval_counter == 150) {
    /* Notify the registered observers which will trigger the res_get_handler to create the response. */
    REST.notify_subscribers(&res_mpu_x);
	//	interval_countr = 0;
//  }
} 
  /* The REST.subscription_handler() will be called for observable resources by the REST framework. */
