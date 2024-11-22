from pylab import *
import os
import matplotlib.pyplot as plt
import numpy as np

# Set a Plot Flag
plot_sample_flag = 1
plot_delta_flag = 1

# Get the background file to read
data_path_dir = "/home/airscanner100/Data/2023_0000_0000"
bkgnd_path_dir = "/home/airscanner100/Data/2023_1229_2034/background"
# file_path_dir = "/home/airscanner100/Data/2023_1220_2317"
# file_path_dir = "/home/airscanner100/Data/2023_1221_1017"

# Process only data files ending in .npy
ext = '.npy'

# Initiate Variables
count = 1               # Counter
sample_rate = 2.4e6     # Samples per second of data collected
center_freq = 1420.4e6  # Center frequency for PSD
direction = 270         # Compass direction 0=North, 90=East, 180=South, 270=West
incline = 45            # Angle of inclination of dish from earth horizon
psd_nfft = 2048         # Length of PSD vectors (freq and magnitude)

# Generate the filename for the averaged background data
load_out_avg = os.path.join(bkgnd_path_dir, "avgbkrgnd__psd__" + str(direction) + "__" + str(incline) + '.npz')

# Load averaged data
avg_in = np.load(load_out_avg)
print(avg_in.files)
psd_array_avg = avg_in['psd_array_avg_vector']
freq_array_avg = avg_in['freq_array_avg_vector']

# Process Data in a Directory
for file_name in os.listdir(data_path_dir):
    if file_name.endswith(ext):

        # Generate a full file and path name
        file_in = os.path.join(data_path_dir, file_name)

        # Extract file name prefix and suffix
        split_tup = os.path.splitext(file_name)

        # Extract the file name and extension for saving plots
        file_name_prefix = split_tup[0]
        file_name_ext = split_tup[1]
        plot_out = \
            os.path.join(data_path_dir, file_name_prefix) + "__" + str(direction) + "__" + str(incline) + '.png'

        # Print Status
        print('Processing File #' + str(count).rjust(3, '0') + ":  " + file_in)

        # Read the file
        data_in = np.load(file_in)

        # Calculate the PSD of the data collected (Generates a Plot)
        psd_samp, freq_samp = \
            psd(data_in, NFFT=psd_nfft, Fs=sample_rate / 1e6, Fc=center_freq / 1e6, return_line=None)

        # Close the figure
        plt.close()

        # Plot the PSD of the captured file
        if plot_sample_flag == 1:

            # Turn on Interactive
            plt.ion()

            # Generate a figure and plot the data
            plt.figure()
            plt.plot(freq_samp, psd_samp)
            xlabel('Frequency (MHz)')
            ylabel('Sample Relative Power')
            plt.title(file_name_prefix + "__" + str(direction) + "__" + str(incline))

            # Save the figure
            plt.savefig(plot_out)

            # Show the plot
            plt.show()

            # Pause
            pause(2)

            # Close the figure
            plt.close()

            # Plot the data with background removed
            # Set up a path and filename for the calibrated plot
            plot_out_delta = os.path.join(data_path_dir, file_name_prefix +
                                          str(direction) + "__" + str(incline) + '__delta' + '.png')

            # Turn on Interactive
            plt.ion()

            # Generate a figure and plot the data
            plt.figure()
            plt.plot(freq_samp, psd_samp - psd_array_avg)
            xlabel('Frequency (MHz)')
            ylabel('Sample Relative Power (Background Subtracted)')
            plt.title(file_name_prefix + "__delta__" + str(direction) + "__" + str(incline))

            # Save the figure
            plt.savefig(plot_out_delta)

            # Show the delta plot
            plt.show()

            # Pause
            pause(2)

            # Close the figure
            plt.close()

        # Update counter
        count = count + 1

        # Close the File
        del file_in

        # Clear the data
        del data_in

    else:
        continue

# End Program 
print('End Program')
