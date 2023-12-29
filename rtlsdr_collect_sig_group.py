from pylab import *
from rtlsdr import *

import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime

sdr = RtlSdr()

# Configure NFFT
nfft_len = 2048

# Set Number of Loops
num_group_loop = 5
num_loops = 5

# Set a Plot Flag
plot_flag = 1

# Pause Time (sec)
pause_group_time = 1
pause_loop_time = 60

# Configure Device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
sdr.gain = 'auto'

# Prepare a Filename
file_prefix = 'data_'
file_path_dir = "C:\\Scan_Files\\data\\"

# Collect Data
for i in range(num_loops):

    for j in range(num_group_loop):

        # Prepare a Time Date String for Filename
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time_now = now.strftime("%H:%M:%S")
        date_time = now.strftime("%Y%m%d__%H%M%S__")

        # String iteration
        # loop = str(i)
        loop = str(i).rjust(3, '0')

        # Create a complete filename
        file_path = file_path_dir + file_prefix + date_time + loop

        # Print Status
        print("Collected " + loop + " of " + str(num_loops) + " " + file_path)

        # Collect Data
        samples = sdr.read_samples(4 * 256 * 1024)

        # Save the File
        np.save(file_path, samples)

        # Close the File
        del file_path

        # Generate the PSD of the data collected
        psd_samp, freq_samp = psd(samples, NFFT=nfft_len, Fs=sdr.sample_rate / 1e6, Fc=sdr.center_freq / 1e6)

        plt.close()

        # Plot Data
        if plot_flag == 1:
            # Plot the PSD of the captured file
            plt.figure(1)
            plt.plot(freq_samp, psd_samp)
            xlabel('Frequency (MHz)')
            ylabel('Samp Relative power (dB)')

            # Show the plot
            plt.show()

        pause(pause_loop_time)

# Pause Before the Next Loop
time.sleep(pause_group_time)

# Close the SDR
sdr.close()

# End Program
print('End Program')
