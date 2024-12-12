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
data_flag = 0

# Set a Plot Flag
plot_flag = 1


# Initiate Variables
num_samples = 8 * 256 * 1024  # Number of samples to collect  8*256*1024
direction = 270               # Compass direction 0=North, 90=East, 180=South, 270=West
incline = 90                  # Angle of inclination of dish from earth horizon
psd_nfft = 4096               # Length of PSD vectors (freq and magnitude)  4096


# Set Variables for Data Collection (1) or Test Mode (0)
if data_flag == 1:   
    num_group_loop = 100	# Set Number of Loops
    num_loops = 200		# Set Number of Loops
    pause_group_time = 1 	# Pause Time (sec)
    pause_loop_time = 90	# Pause Time (sec)
elif data_flag == 0
    num_group_loop = 3		# Set Number of Loops
    num_loops = 3		# Set Number of Loops
    pause_group_time = 1	# Pause Time (sec)
    pause_loop_time = 3		# Pause Time (sec)


# Configure Device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
sdr.gain = 'auto'

# Prepare a Time Date String for Directory
now = datetime.now()
date_time_dir = now.strftime("%Y%m%d__%H%M")
        
# Determine the OS
if platform == "linux" or platform == "linux2":
    # linux
    print("OS is Linux ...")
    file_path_dir = "/home/airscanner100/Data/" + date_time_dir + "/"
elif platform == "darwin":
    # OS X
    print("OS is Mac ...")
    file_path_dir = "/home/airscanner100/Data/" + date_time_dir + "/"
elif platform == "win32":
    # Windows
    print("OS is Windows ...")
    file_path_dir = "C:\\Scan_Files\\data\\" + date_time_dir + "\\"

# Create Directory if Necessary
if not os.path.exists(file_path_dir):
    os.mkdir(file_path_dir)

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

    for j in range(num_group_loop):
      
        # Print Status
        print(date_time_dir + " Group " + str(i+1) + "/" + str(num_loops) + 
            ", File " + str(j+1) + "/" + str(num_group_loop))

        # Collect Data
        samples = sdr.read_samples(num_samples)

        # Close Plot for PSD
        plt.close()
    
        # Generate the PSD of the Data Collected
        psd_samp, freq_samp = plt.psd(samples, NFFT=psd_nfft, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)

        # Close Plot for PSD
        plt.close()

	    # Add to the PSD array
        psd_array = psd_array + psd_samp
        freq_array = freq_array + freq_samp
        
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

    # String Iteration
    group_loop = str(j+1).rjust(3, '0')

    # Create a Complete Filename
    file_path = file_path_dir + loop + "__avg__" + date_time + f"{direction:03d}" + "_" + f"{incline:03d}"

    # Generate an Average PSD
    print('Generating an Averaged Signal Result')
    print('------------------------------------')
    psd_array_avg = psd_array / (count - 1)
    freq_array_avg = freq_array / (count - 1)

    # Save the File
    np.save(file_path, [psd_array_avg,freq_array_avg])

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
        plt.title(str(date_time) + "  Uncr Avg PSD " + str(count-1) + " Traces: Loop " + str(i+1))

        # Save the Plot
        plt.savefig(file_path)

        # Show the Plot
        plt.show()

        # Pause
        time.sleep(4)
        
        # Close the Average Plot
        plt.close()
            
    # Pause Before the Next Loop
    time.sleep(pause_loop_time)

    # Close the File
    del file_path
    
    # Close the Plot
    plt.close()

# Close the SDR
sdr.close()

# Close all Plots
plt.close()

# Upload the Results




# End Program
# Print the End Time
print("End Time : ", time.ctime())
print('End Program')
