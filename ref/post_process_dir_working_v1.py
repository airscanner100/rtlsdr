import os
import matplotlib.pyplot as plt
import numpy as np
import time
from sys import platform
from datetime import datetime

# Set a flag
plot_flag = 1

# Set parameter
low_limit = -0.10

# Print the Start Time
print("Str Time : ", time.ctime())

# Load the .npy file
[psd_array_avg,freq_array_avg] = np.load('C:\\Temp\\20241211__1813\\001__avg__20241211__181904__270_090.npy')

psd_array_avg_mean = np.average(psd_array_avg)
print(psd_array_avg_mean)

# Plot Data
if plot_flag == 1:

    # Turn on Interactive
    #plt.ion()

    # Plot the PSD of the Averaged Data
    #plt.figure(1)
    plt.plot(freq_array_avg,psd_array_avg)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Samp Relative power (dB)')
    plt.title(" Data  Avg_PSD=" + f"{psd_array_avg_mean:0.3f}")
    plt.ylim(low_limit, 3 * -low_limit)

    # Show the Plot
    plt.show()
        
    time.sleep(5)

    # Close the Average Plot
    plt.close()


# End Program
# Print the End Time
print("End Time : ", time.ctime())
print('End Program')
