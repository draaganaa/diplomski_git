import smbus                    #import SMBus module of I2C
from time import sleep          #import time module
import csv			#import csv module for saving data
from datetime import datetime
import serial			
from time import sleep
import sys
from gps_class import GPSVis
import numpy as np 
import matplotlib.pyplot as plt


#configuratio for GPS module

ser=serial.Serial("/dev/ttyAMA0")
gpgga_info = "$GPGGA,"  
GPGGA_buffer = 0
NMEA_buff = 0



#some MPU6050 Registers and their Address

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


# function for initialization of accelerometer

def MPU_Init():
        #write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)

        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)


#function for reading raw data from accelerometer


def read_raw_data(addr):
        #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

#function for processing data grom GPS module

def convert_to_degrees(raw_value):
        decimal_value = raw_value/100.00
        degrees = int(decimal_value)
        mm_mmmm  = (decimal_value - int(decimal_value))/0.6
        position = degrees + mm_mmmm
        position = "%.4f" %(position)
        return position





bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")
file_1 =open( "accel_data.csv","w")
file_2 = open("gps_data.csv", "w")
writer_1=csv.writer(file_1)
writer_2=csv.writer(file_2)
writer_1.writerow(["Time","Xout","Yout","Zout"])
#writer_2.writerow(["Latitude", "Longitude"])

try:
	while True:
		received_data = (str)(ser.readline())   #read NMEA string receivde
		GPGGA_data_available = received_data.find(gpgga_info)   #check for NMEA GPGGAstring
		if (GPGGA_data_available > 0):
			GPGGA_buffer = received_data.split("$GPGGA,",1)[1]      #store data coming after ">
			NMEA_buff = (GPGGA_buffer.split(','))
			nmea_time = []
			nmea_latitude = []
			nmea_longitude =[]
			nmea_time = NMEA_buff[0]
			nmea_latitude = NMEA_buff[1]
			nmea_longitude = NMEA_buff[3]

			print("NMEA Time:", nmea_time, '\n')
			lat = (float) (nmea_latitude)
			lat = convert_to_degrees(lat)
			longi = (float)(nmea_longitude)
			longi = convert_to_degrees(longi)

			writer_2.writerow([lat,longi])

			print("NMEA Latitude:", lat, "NMEA Longitude", longi, '\n')

        #Read Accelerometer raw value
		acc_x = read_raw_data(ACCEL_XOUT_H)
		acc_y = read_raw_data(ACCEL_YOUT_H)
		acc_z = read_raw_data(ACCEL_ZOUT_H)

        #Read Gyroscope raw value
	#gyro_x = read_raw_data(GYRO_XOUT_H)
	#gyro_y = read_raw_data(GYRO_YOUT_H)
	#gyro_z = read_raw_data(GYRO_ZOUT_H)

        #Full scale range +/- 250 degree/C as per sensitivity scale factor
		Ax = acc_x/2048.0
		Ay = acc_y/2048.0
		Az = acc_z/2048.0

	#Gx = gyro_x/32.8
	#Gy = gyro_y/32.8
	#Gz = gyro_z/32.8

		time_=  datetime.now()
		curr_time = time_.strftime("%H:%M:%S")

		writer_1.writerow([curr_time,Ax, Ay, Az])

		print ("\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
		sleep(1)
except KeyboardInterrupt:
	file_1.close()
	file_2.close()

	vis = GPSVis(data_path='gps_data.csv',
             map_path='map.png',  # Path to map downloaded from the OSM.
             points=(45.8357, 15.9645, 45.6806, 16.1557)) # Two coordinates of >

	vis.create_image(color=(0, 0, 255), width=3)  # Set the color and the width of >
	vis.plot_map(output='save')

	print()


	with open("accel_data.csv", "r") as f:
        	data = list(csv.reader(f, delimiter=","))       #reading csv file
        	data1 = np.array(data[1:])      

#extracting data
        	time = data1[:,0]
        	ax = data1[:,1].astype(float)
        	ay = data1[:,2].astype(float)
        	az = data1[:,3].astype(float)


#plotting all data on same axis
        	plt.figure(figsize=(20,20))
        	plt.plot(time, ax, time, ay, time, az)
        	plt.title("Accelerometer data:", fontsize = 20)
        	plt.xlabel("Time",  fontsize = 20)
        	plt.xticks(rotation = 45, ha="right")
        	plt.ylabel("Acc . values", fontsize = 20)
        	plt.savefig("accel_data_time.jpeg")
        	plt.show()

#separate plots using subplots
        	plt.figure(figsize=(30,30))

        	plt.subplot(2,2,1)
        	plt.plot(ax, color="r")
        	plt.title("a[x]", fontsize=30)
        	plt.savefig("X_axis_time.jpeg")

        	plt.subplot(2,2,2)
        	plt.plot(ay, color="g")
        	plt.title("a[y]", fontsize=30)
        	plt.savefig("Y_axis_time.jpeg")

        	plt.subplot(2,2,3)      
        	plt.plot(az, color="b")
        	plt.title("a[z]", fontsize=30)
        	plt.savefig("Z_axis_time.jpeg")
        	#plt.show()




