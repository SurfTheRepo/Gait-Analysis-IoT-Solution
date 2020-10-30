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

#if PLATFORM_HAS_LEDS

#include <string.h>
#include "contiki.h"
#include "rest-engine.h"
#include "dev/leds.h"
#include "board-peripherals.h"
#include <limits.h>

#define CHUNKS_TOTAL    5000
#define MAX_AGE      60
static void res_get_handler_x(void *request, void *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset);

static struct ctimer timer_ctimer;		//Callback Timer
static int counter_ctimer;
 // hold timer vals
static int n;

static int indexVal = 0;
static int sendval[800];
static struct ctimer timer_ctimer;		//Callback Timer
static int counter_ctimer;
 // hold timer vals
/*
 * Use local resource state that is accessed by res_get_handler() and altered by res_periodic_handler() or PUT or POST.
 */
static int32_t event_counter = 0;

PARENT_RESOURCE(res_mpu_x,
                "title=\"Gyro-x\"",
                res_get_handler_x,
                NULL,
                NULL,
                NULL);
static void res_get_handlerTwo(void *request, void *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset);
static void res_periodic_handler(void);

static void updateTime() {
	if (!(counter_ctimer >= 120)) {
  ctimer_reset(&timer_ctimer);
	counter_ctimer = 0;
	}	
		int senseX = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_X);
		int senseY = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Y);
		int senseZ = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Z);
		sendval[indexVal] = senseX;
		sendval[indexVal+1] = senseY;
    sendval[indexVal+2] = senseZ;
		indexVal++;
  counter_ctimer++;
}

// GYRO Sensors
/*---------------------------------------------------------------------------*/

static void
res_get_handler_x(void *request, void *response, uint8_t *buffer, uint16_t preferred_size, int32_t *offset)
{	
	
  char *str;
	REST.set_header_content_type(response, REST.type.TEXT_PLAIN);
	REST.set_header_max_age(response, MAX_AGE);
	// Chunks
	int32_t strpos = 0;

  const char *uri_path = NULL;
  int len = REST.get_url(request, &uri_path);
  int base_len = strlen(res_mpu_x.url);

  if(len == base_len) {
    snprintf((char *)buffer, REST_MAX_CHUNK_SIZE, "Request any sub-resource of /%s", res_mpu_x.url);
  } else {
    snprintf((char *)buffer, REST_MAX_CHUNK_SIZE, "%.*s", len - base_len, (uri_path) + base_len);
	str = strtok (buffer, "/");
	n = atoi(str);
	
	ctimer_set(&timer_ctimer, CLOCK_SECOND / 50, updateTime, NULL);
  /* Check the offset for boundaries of the resource data. */
  if(*offset >= CHUNKS_TOTAL) {
    REST.set_response_status(response, REST.status.BAD_OPTION);
    /* A block error message should not exceed the minimum block size (16). */

    const char *error_msg = "BlockOutOfScope";
    REST.set_response_payload(response, error_msg, strlen(error_msg));
    return;
  }

  /* Generate data until reaching CHUNKS_TOTAL. */
	int count = 0;
	// Fill the Buffer at a rate of 50 Hertz
  while(strpos < preferred_size) {
		strpos += snprintf((char *)buffer + strpos, preferred_size - strpos + 1, "|%d|", sendval[count]);
		
	count++;
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
 // Chunks
  }
	
 // snprintf((char *)buffer, REST_MAX_CHUNK_SIZE, "Gyro-X: %d", value);
  //REST.set_response_payload(response, buffer, strlen((char *)buffer));
  /* The REST.subscription_handler() will be called for observable resources by the REST framework. */
}

  /* The REST.subscription_handler() will be called for observable resources by the REST framework. */

#endif /* PLATFORM_HAS_LEDS */
