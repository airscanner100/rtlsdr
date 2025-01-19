from pylab import *
from rtlsdr import *
from sys import platform

import os
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime

# Initialize the sdr object
sdr = RtlSdr()

# Set a flag for Data Collection Mode (1) or Test Mode (0)
data_flag = 1

# Set a Plot Flag
plot_flag = 1

# Set a flag to subtract off baseline trace
sub_flag = 1

# Initiate Variables
num_samples = 8 * 256 * 1024  # Number of samples to collect  4*256*1024
gps = "27VP+QQ"               # GPS location in Google Maps Plus Code
incline_ew = 90               # Angle of inclination of dish from earth horizon ref east = 0, west = 180
incline_ns = 135              # Angle of inclination of dish from earth horizon ref north = 0, south = 180
psd_nfft = 8192 * 2           # Length of PSD vectors (freq and magnitude)  8192 * 2

# Set Variables for Data Collection (1) or Test Mode (0)
if data_flag == 1:   
    num_group_loop = 300	    # Set Number of Loops  100
    num_loops = 125             # Set Number of Loops  125 for 24 hrs
    pause_group_time = 0.01  	# Pause Time (sec)     1
    pause_loop_time = 300	    # Pause Time (sec)     300
    low_limit = -0.2			# Low limit for plot   0.10 (v4)
    x_low = 1419
    x_high = 1422
elif data_flag == 0:
    num_group_loop = 30  		# Set Number of Loops (30)
    num_loops = 3		        # Set Number of Loops
    pause_group_time = 0.01	    # Pause Time (sec)
    pause_loop_time = 5		    # Pause Time (sec)
    
# Configure Device
sdr.sample_rate = 2.4e6         # 2.4e6 
sdr.center_freq = 1420.4e6
sdr.gain = 'auto' # 'auto' 

print("SDR Gain = " + str(sdr.gain))

# Prepare a Time Date String for Directory
now = datetime.now()
date_time_dir = now.strftime("%Y%m%d__%H%M")
        
# Determine the OS
if platform == "linux" or platform == "linux2":
    # linux
    print("OS is Linux ...")
    file_path_dir = "/home/airscanner100/Documents/github/results/" + date_time_dir + "/"
elif platform == "darwin":
    # OS X
    print("OS is Mac ...")
    file_path_dir = "/home/airscanner100/Documents/github/results" + date_time_dir + "/"
elif platform == "win32":
    # Windows
    print("OS is Windows ...")
    file_path_dir = "C:\\Scan_Files\\results\\" + date_time_dir + "\\"

# Create the Main Directory if Necessary
if not os.path.exists(file_path_dir):
    os.mkdir(file_path_dir)

# Create a Subdirectory for the data
file_path_dir_dat = file_path_dir + "dat/"
if not os.path.exists(file_path_dir_dat):
    os.mkdir(file_path_dir_dat)

# Create a Subdirectory for the Unsubtracted Figures
file_path_dir_raw = file_path_dir + "raw/"
if not os.path.exists(file_path_dir_raw):
    os.mkdir(file_path_dir_raw)
    
# Create a Subdirectory for the Subtracted Figures
file_path_dir_sub = file_path_dir + "sub/"
if not os.path.exists(file_path_dir_sub):
    os.mkdir(file_path_dir_sub)    
    
# Print the Start Time
print("Start Time : ", time.ctime())

# Collect Data
for i in range(num_loops):

    # Initiate Variables
    count = 1    # Counter

    # String Iteration
    loop = str(i+1).rjust(3, '0')

    # Initialize Arrays for Averaging
    psd_array = np.zeros(psd_nfft)
    freq_array = np.zeros(psd_nfft)
    psd_array_avg_sub = np.zeros(psd_nfft)
    psd_array_avg = np.zeros(psd_nfft)

    for j in range(num_group_loop):
      
        # Update the time stamp
        now = datetime.now()
        date_time_cur = now.strftime("%Y%m%d__%H%M%S")

        # Collect Data
        samples = sdr.read_samples(num_samples)

        # Close Plot for PSD
        plt.close()
    
        # Generate the PSD of the Data Collected
        psd_samp, freq_samp = plt.psd(samples, NFFT=psd_nfft, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)
        
	    # Add to the loop PSD array
        psd_array = psd_array + psd_samp
        freq_array = freq_array + freq_samp
        
		# Calculate the average of the averaged PSD Array
        psd_samp_mean = np.average(psd_samp)
   
        # Print Status
        print(date_time_cur + " Group " + str(i+1) + "/" + str(num_loops) + 
            ", File " + str(j+1) + "/" + str(num_group_loop) + 
            ", PSDAvg=" + f"{psd_samp_mean:.2e}" +
            ", SDRGain=" + str(sdr.gain))
               
        # Close Plot for PSD
        plt.close()
       
        # Update Counter
        count = count + 1

        # Pause
        time.sleep(pause_group_time)

    # Print Update
    print("Collected Loop " + str(i+1) + " of " + str(num_loops))

    # Prepare a Time Date String for Filename
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time_now = now.strftime("%H:%M:%S")
    date_time = now.strftime("%Y%m%d__%H%M%S__")
    date_time_short = now.strftime("%Y%m%d__%H%M")

    # String Iteration
    group_loop = str(j+1).rjust(3, '0')

    # Create Complete Filenames
    file_path_dat = file_path_dir_dat + loop + "__avg_dat__" + date_time + gps + "_" + f"{incline_ns:03d}" + "_" + f"{incline_ew:03d}"
    file_path_raw = file_path_dir_raw + loop + "__avg_raw__" + date_time + gps + "_" + f"{incline_ns:03d}" + "_" + f"{incline_ew:03d}"
    file_path_sub = file_path_dir_sub + loop + "__avg_sub__" + date_time + gps + "_" + f"{incline_ns:03d}" + "_" + f"{incline_ew:03d}"
    
    # Generate an Average PSD
    print('Generating an Averaged Signal Result')
    psd_array_avg = psd_array / (count - 1)
    freq_array_avg = freq_array / (count - 1)

    # Calculate the average of the averaged PSD Array (single value)
    psd_array_avg_mean = np.average(psd_array_avg)

    # Add to the baseline PSD array
    if i+1 == 1 and sub_flag == 1:
	    print("Count = " + str(count-1) + " Collected Reference Sample")
	    psd_samp_base = psd_array_avg
	    
    # Save the File
    print("Saving Data to " + file_path_dir_dat)
    np.save(file_path_dat, [psd_array_avg,freq_array_avg],psd_array_avg_mean)

    # Close any Plots that Might be Open
    plt.close()

    # Plot Data
    if plot_flag == 1:

        # Turn on Interactive
        plt.ion()

        # Plot the PSD of the Averaged Data
        plt.figure(1)
        plt.plot(freq_array_avg, psd_array_avg)
        plt.xlabel('Frequency (MHz)')
        plt.ylabel('Samp Relative power (dB)')
        plt.title(str(date_time_short) + "," + str(count-1) + 
            " Trcs, Batch " + str(i+1) + ", AVg=" + 
            f"{psd_array_avg_mean:.2e}" + ", SDRGain=" + str(sdr.gain))
        if data_flag == 1:
            plt.ylim(low_limit,None)
            plt.xlim(x_low, x_high)
            
        # Save the Plot
        print("Saving Raw Figure to " + file_path_dir_raw)
        plt.savefig(file_path_raw)

        # Show the Plot
        plt.show()    
        
        # Pause
        time.sleep(1)
        
        # Close the Average Plot
        plt.close()

		# Plot the PSD of the Averaged Data with the Baseline Subtracted
        if sub_flag == 1:
            psd_array_avg_sub = psd_array_avg - psd_samp_base
	        
	        # Plot a figure subtracted off the baseline signal        
            plt.figure(2)
            plt.plot(freq_array_avg, psd_array_avg_sub)
            plt.xlabel('Frequency (MHz)')
            plt.ylabel('Samp Relative power (dB)')
            plt.title(str(date_time_short) + "," + str(count-1) + 
                " Trcs, Batch " + str(i+1) + ", AVg=" + 
                f"{psd_array_avg_mean:.2e}" + ", SDRGain=" + str(sdr.gain))
            if data_flag == 1:
                plt.ylim(low_limit,None)
                plt.xlim(x_low, x_high)
        
        # Save the Plot
        print("Saving Subtracted Figure to " + file_path_dir_sub)
        plt.savefig(file_path_sub)

        # Show the Plot
        plt.show()              
            
        # Pause
        time.sleep(1)
        
        # Close the Average Plot
        plt.close()            

    print('------------------------------------')
             
    # Pause Before the Next Loop
    time.sleep(pause_loop_time)

    # Close the File
    del file_path_dat
    del file_path_raw
    del file_path_sub
    
    # Close the Plot
    plt.close()

# Close the SDR
sdr.close()

# Close all Plots
plt.close()

# End Program
# Print the End Time
print("End Time : ", time.ctime())
print('End Program')
