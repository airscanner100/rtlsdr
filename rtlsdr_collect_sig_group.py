from pylab import *
from rtlsdr import *

import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime

sdr = RtlSdr()

# Initiate Variables
direction = 270         # Compass direction 0=North, 90=East, 180=South, 270=West
incline = 45            # Angle of inclination of dish from earth horizon
psd_nfft = 2048         # Length of PSD vectors (freq and magnitude)

# Set Number of Loops
num_group_loop = 30
num_loops = 120

# Set a Plot Flag
plot_flag = 0

# Pause Time (sec)
pause_group_time = 3
pause_loop_time = 600

# Configure Device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
sdr.gain = 'auto'

# Prepare a Filename
file_prefix = 'data_'
file_path_dir = "C:\\Scan_Files\\data\\"

# Collect Data
for i in range(num_loops):

    # String iteration
    loop = str(i).rjust(3, '0')

    for j in range(num_group_loop):

        # Prepare a Time Date String for Filename
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time_now = now.strftime("%H:%M:%S")
        date_time = now.strftime("%Y%m%d__%H%M%S__")

        # String iteration
        group_loop = str(j + 1)

        # Create a complete filename
        file_path = file_path_dir + file_prefix + date_time + loop + "__" + str(direction) + "_" + str(incline)

        # Print Status
        print("Collected Group Loop " + group_loop + " of " + str(num_group_loop) + " " + file_path)

        # Collect Data
        samples = sdr.read_samples(4 * 256 * 1024)

        # Save the File
        np.save(file_path, samples)

        # Generate the PSD of the data collected
        psd_samp, freq_samp = psd(samples, NFFT=psd_nfft, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)

        plt.close()

        # Plot Data
        if plot_flag == 1:

            # Turn on interactive
            plt.ion()

            # Plot the PSD of the captured file
            plt.figure(1)
            plt.plot(freq_samp, psd_samp)
            xlabel('Frequency (MHz)')
            ylabel('Samp Relative power (dB)')

            # Show the plot
            plt.show()

            # Save the plot
            # Save command

            # Close the plot
            plt.close()

        pause(pause_group_time)

    # Print update
    print("Collected Loop " + loop + " of " + str(num_loops))

    # Pause Before the Next Loop
    pause(pause_loop_time)

    # Close the File
    del file_path

# Close the SDR
sdr.close()

# End Program
print('End Program')
