/**
 * \file
 *         A very simple Contiki application showing how Contiki programs look
 * \author
 *         mds
 */

#include "contiki.h"
#include <stdio.h> /* For printf() */
#include <stdbool.h>
#include "dev/serial-line.h"
#include "dev/cc26xx-uart.h"
#include <string.h>
#include "board-peripherals.h"
#include "ti-lib.h"
#include "rf-core/rf-ble.h"
/*---------------------------------------------------------------------------*/
//PROCESS(prac1, "prac1");
PROCESS(acc_process, "accelerometer process");
AUTOSTART_PROCESSES(&acc_process);
/*---------------------------------------------------------------------------*/

//Global Vars


PROCESS_THREAD(acc_process, ev, data){


	PROCESS_BEGIN();
	mpu_9250_sensor.configure(SENSORS_ACTIVE, MPU_9250_SENSOR_TYPE_ALL);
	printf("turning mpu sensor on\n\r");

	while(1){

		int gx_value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_X);
		int gy_value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Y);
		int gz_value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_GYRO_Z);
		int ax_value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_X);
		int ay_value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Y);
		int az_value = mpu_9250_sensor.value(MPU_9250_SENSOR_TYPE_ACC_Z);
		
		printf("ax%day%daz%dgx%dgy%dgz%d\n",ax_value, ay_value, az_value, gx_value, gy_value, gz_value);
		
		clock_wait(CLOCK_SECOND/3);	
	}
	PROCESS_END();
}





/*---------------------------------------------------------------------------*/
