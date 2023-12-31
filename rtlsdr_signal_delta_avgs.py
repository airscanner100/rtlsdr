from pylab import *
import os
import matplotlib.pyplot as plt
import numpy as np

# Set a Plot Flag
plot_sample_flag = 1
plot_delta_flag = 1

# Get the background file to read
data_path_dir = "/home/airscanner100/Data/2023_0000_0000"
#bkgnd_path_dir = "/home/airscanner100/Data/2023_1229_2034/background"
# file_path_dir = "/home/airscanner100/Data/2023_1220_2317"
# file_path_dir = "/home/airscanner100/Data/2023_1221_1017"

# Initiate Variables
count = 1               # Counter
sample_rate = 2.4e6     # Samples per second of data collected
center_freq = 1420.4e6  # Center frequency for PSD
direction = 270         # Compass direction 0=North, 90=East, 180=South, 270=West
incline = 45            # Angle of inclination of dish from earth horizon
psd_nfft = 2048         # Length of PSD vectors (freq and magnitude)

# Generate the filename for the averaged background data
load_bkgrnd_avg = os.path.join(data_path_dir, "avgbkrgnd__psd__" + str(direction) + "__" + str(incline) + '.npz')

# Generate the filename for the averaged sample data
load_sample_avg = os.path.join(data_path_dir, "signal_1700__psd__" + str(direction) + "__" + str(incline) + '.npz')

# Load averaged background data
avg_bkgrnd_in = np.load(load_bkgrnd_avg)
psd_array_bkgrnd_avg = avg_bkgrnd_in['psd_array_avg_vector']
freq_array_bkgrnd_avg = avg_bkgrnd_in['freq_array_avg_vector']

# Load averaged sample data
avg_sample_in = np.load(load_sample_avg)
psd_array_sample_avg = avg_sample_in['psd_array_avg_vector']
freq_array_sample_avg = avg_sample_in['freq_array_avg_vector']

# Generate file name for saving plots
plot_out = os.path.join(data_path_dir, "delta__" + str(direction) + "__" + str(incline) + '.png')

# Plot the PSD of the captured file
if plot_sample_flag == 1:

    # Turn on Interactive
    plt.ion()

    # Generate a figure and plot the data
    plt.figure()
    plt.plot(freq_array_sample_avg, psd_array_sample_avg - psd_array_bkgrnd_avg)
    xlabel('Frequency (MHz)')
    ylabel('Sample Relative Power (Corrected)')
    plt.title("delta__" + str(direction) + "__" + str(incline))

    # Save the figure
    plt.savefig(plot_out)

    # Show the delta plot
    plt.show()

    # Pause
    pause(4)

    # Close the figure
    plt.close()

# Clear the data
del avg_bkgrnd_in
del avg_sample_in

# End Program 
print('End Program')
