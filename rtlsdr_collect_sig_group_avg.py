from pylab import *
from rtlsdr import *
from sys import platform

import os
import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime

sdr = RtlSdr()

# Initiate Variables
num_samples = 8 * 256 * 1024  # Number of samples to collect  1024
direction = 270               # Compass direction 0=North, 90=East, 180=South, 270=West
incline = 45                  # Angle of inclination of dish from earth horizon
psd_nfft = 4096               # Length of PSD vectors (freq and magnitude)  2048

# Set Number of Loops
num_group_loop = 100 #100
num_loops = 100 #90

# Pause Time (sec)
pause_group_time = 1 #1
pause_loop_time = 60 #600

# Set a Plot Flag
plot_flag = 1

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
    file_path_dir = "/home/airscanner101/Data/" + date_time_dir + "/"
elif platform == "darwin":
    # OS X
    print("OS is Mac ...")
    file_path_dir = "/home/airscanner101/Data/" + date_time_dir + "/"
elif platform == "win32":
    # Windows
    print("OS is Windows ...")
    file_path_dir = "C:\\Scan_Files\\data\\" + date_time_dir + "\\"

# Create directory if necessary
if not os.path.exists(file_path_dir):
    os.mkdir(file_path_dir)

# Collect Data
for i in range(num_loops):

    # Initiate Variables
    count = 1    # Counter

    # String iteration
    loop = str(i).rjust(3, '0')

    # Initialize arrays for averaging
    psd_array = np.array(zeros(psd_nfft))
    freq_array = np.array(zeros(psd_nfft))

    for j in range(num_group_loop):
      
        # Print Status
        print("Collected Group File " + str(j+1) + " of " + str(num_group_loop))

        # Collect Data
        samples = sdr.read_samples(num_samples)

        # Close plot for PSD
        plt.close()
    
        # Generate the PSD of the data collected
        psd_samp, freq_samp = psd(samples, NFFT=psd_nfft, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)

        # Close plot for PSD
        plt.close()

	# Add to the PSD array
        psd_array = psd_array + psd_samp
        freq_array = freq_array + freq_samp
        
        # Update counter
        count = count + 1

        # Pause
        pause(pause_group_time)

    # Print update
    print("Collected Loop " + str(i+1) + " of " + str(num_loops))

    # Prepare a Time Date String for Filename
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    time_now = now.strftime("%H:%M:%S")
    date_time = now.strftime("%Y%m%d__%H%M%S__")

    # String iteration
    group_loop = str(j+1).rjust(3, '0')

    # Create a complete filename
    file_path = file_path_dir + loop + "__avg__" + date_time + str(direction) + "_" + str(incline)

    # Generate an average PSD
    print('Generating an Averaged Signal Result')
    print('------------------------------------')
    psd_array_avg = psd_array / (count - 1)
    freq_array_avg = freq_array / (count - 1)

    # Save the File
    np.save(file_path, [psd_array_avg,freq_array_avg])

    # Close any plots that might be open
    plt.close()

    # Plot Data
    if plot_flag == 1:

        # Turn on interactive
        plt.ion()

        # Plot the PSD of the averaged data
        plt.figure(1)
        plt.plot(freq_array_avg, psd_array_avg)
        xlabel('Frequency (MHz)')
        ylabel('Samp Relative power (dB)')
        plt.title(str(date_time) + "  Uncr Avg PSD " + str(count-1) + " Traces: Loop " + str(i+1))

        # Save the plot
        plt.savefig(file_path)

        # Show the plot
        plt.show()

        # Pause
        pause(1)
        
        # Close the average plot
        plt.close()
            
    # Pause Before the Next Loop
    pause(pause_loop_time)

    # Close the File
    del file_path
    
    # Close the plot
    plt.close()

# Close the SDR
sdr.close()

# Close all plots
plt.close()

# End Program
print('End Program')
