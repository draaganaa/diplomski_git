import numpy as np
import matplotlib.pyplot as plt
import csv

with open("accel_data.csv", "r") as f:
	data = list(csv.reader(f, delimiter=","))	#reading csv file
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
	plt.show()
