####################################################################################################
# Code Author: Jorge Mazariegos
# Using the sample code provided at https://api.walabot.com/_sample.html
# Modified for use in course project of Umass Lowell's CS4600 class.
####################################################################################################

####################################################################################################
# Begin Imports
####################################################################################################

from __future__ import print_function#WalabotAPIworksonbothPython2an3.
import sys
from sys import platform
from os import system
from imp import load_source
from os.path import join
import datetime
import time
from time import sleep #imported so that we can stop recording after 5 minutes without user input.
import pandas as pd
import numpy as np

####################################################################################################
# End Imports
####################################################################################################

####################################################################################################
# Begin initialization of the Walabot Libraries.
####################################################################################################

if platform=='win32':
	modulePath=join('C:/','Program Files','Walabot','WalabotSDK','python','WalabotAPI.py')
elif platform.startswith('linux'):
	modulePath=join('/usr','share','walabot','python','WalabotAPI.py')
	
wlbt=load_source('WalabotAPI',modulePath)
wlbt.Init()

####################################################################################################
# End initialization of the Walabot Libraries.
####################################################################################################

####################################################################################################
# Begin Definition of SensorApp() which collects the data from the sensor and records it into lists,
# which are converted to numpy arrays before finally becoming panda dataframs to be exported to csv
# files for later use in training and testing our model for fall detection.
####################################################################################################

def SensorApp(label):
	##################################################
	# Initialize the input parameters of:
	# wlbt.SetArenaR
	# wlbt.SetArenaTheta
	# wlbt.SetArenaPhi
	##################################################

	minInCm, maxInCm, resInCm=30,200,3
	minIndegrees, maxIndegrees, resIndegrees=-15,15,5
	minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees=-60, 60, 5
	
	##################################################
	# SetMTImode, start_time and the label
	##################################################
	
	mtiMode=False
	duration = 300
	start_time = time.time()
	rasterImage = []
	targets = []
	timeStamp = []
	labels = []
	
	print_label = ""
	if label == "0":
		print_label = "Walk"
	elif label == "1":
		print_label = "Stand"
	elif label == "2":
		print_label = "Fall"
	
	##################################################
	# Initialize and establish communication with the
	# device and configure it.
	##################################################
	
	wlbt.Initialize()
	wlbt.ConnectAny()
	wlbt.SetProfile(wlbt.PROF_SENSOR)
	wlbt.SetArenaR(minInCm, maxInCm, resInCm)
	wlbt.SetArenaTheta(minIndegrees, maxIndegrees, resIndegrees)
	wlbt.SetArenaPhi(minPhiInDegrees, maxPhiInDegrees, resPhiInDegrees)
	
	##################################################
	# Create the Filenames
	##################################################
	
	raster_filename = (print_label + "_RasterImage" + ".csv")
	targets_filename = (print_label + "_Targets" + ".csv")
	
	##################################################
	# Start the device.
	##################################################
	wlbt.Start()
	
	rf = open(raster_filename, "a+")
	tf = open(targets_filename, "a+")
	
	##################################################
	# Start Collecting Data until 5 minutes have
	# passed.
	##################################################
	
	if not mtiMode:
		wlbt.StartCalibration()
		while wlbt.GetStatus()[0]==wlbt.STATUS_CALIBRATING:
			wlbt.Trigger()
			try:
				print("Collecting Data... Interrupt with Ctrl+C")
				while True:
					
					appStatus, calibrationProcess=wlbt.GetStatus()
					wlbt.Trigger()
					
					targets.append(wlbt.GetSensorTargets())
					rasterImage.append(wlbt.GetRawImageSlice()[0])
					
					time_now=pd.to_datetime(datetime.datetime.now(), format="%Y-%m-%d %H:%M")
					timeStamp.append(time_now)
					labels.append(label)
					
					if time.time() - start_time > duration:
						break

			except KeyboardInterrupt:
				print("Press Ctrl+C to terminate while statement")
				pass
				
			wlbt.Stop()
			wlbt.Disconnect()
			wlbt.Clean()

			i = 0
			while(i < len(rasterImage)): # Conveniently rasterImage, targets, timeStamp and labels are all the same length.
				rf.write(str(timeStamp[i]) + "," + str(rasterImage[i]) + "," + print_label + "\n")
				tf.write(str(timeStamp[i]) + "," + str(targets[i]) + "," + print_label + "\n")
				i += 1
				
			rf.close()
			tf.close()
			
			print('Terminated Successfully and Saved')
			
#################################################################################################################################################
# End SensorApp
#################################################################################################################################################

#################################################################################################################################################
# Begin Main
#################################################################################################################################################

if __name__=='__main__':
	##################################################
	# Prompt the user for the activity being recorded. 
	##################################################
	print("Please enter which activity is being recorded: walking(0) standing(1) fall(2)")
	while True:
		if(sys.argv[1] == '0' or sys.argv[1] == '1' or sys.argv[1] == '2'):
			label = sys.argv[1]
			SensorApp(label)
			break
		else:
			print("Please enter a number corresponding to an activity!")
			
#################################################################################################################################################
# End of main
#################################################################################################################################################	