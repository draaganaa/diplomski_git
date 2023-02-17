import serial
from time import sleep
import sys
import csv

ser=serial.Serial("/dev/ttyAMA0",9600,timeout=1)
gpgga_info = "$GPGGA,"	
GPGGA_buffer = 0
NMEA_buff = 0


def convert_to_degrees(raw_value):
	decimal_value = raw_value/100.00
	degrees = int(decimal_value)
	mm_mmmm  = (decimal_value - int(decimal_value))/0.6
	position = degrees + mm_mmmm
	position = "%.4f" %(position)
	return position

file = open("gps_data.csv","w")
writer=csv.writer(file)

while True:
	received_data = (str)(ser.readline())	#read NMEA string receivde
	GPGGA_data_available = received_data.find(gpgga_info) 	#check for NMEA GPGGAstring
	
	if (GPGGA_data_available > 0):
		GPGGA_buffer = received_data.split("$GPGGA,",1)[1]	#store data coming after "$GPGGA,"
		NMEA_buff = (GPGGA_buffer.split(','))
		nmea_time = []
		nmea_latitude = []
		nmea_longitude = []
		nmea_time = NMEA_buff[0]
		nmea_latitude = NMEA_buff[1]
		nmea_longitude = NMEA_buff[3]
			
		print("NMEA Time:", nmea_time, '\n')
		lat = (float) (nmea_latitude)
		lat = convert_to_degrees(lat)
		longi = (float)(nmea_longitude)
		longi = convert_to_degrees(longi)
		writer.writerow([lat,longi])
		print("NMEA Latitude:", lat, "NMEA Longitude", longi, '\n')

file.close()

	
