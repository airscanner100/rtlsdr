from pylab import *

import os
import matplotlib.pyplot as plt
import numpy as np

# Set a Plot Flag
plot_flag = 1

# Get the background file to read
file_path_dir = "/home/airscanner100/Data/2023_0000_0000"
# file_path_dir = "/home/airscanner100/Data/2023_1221_BKGRND"
# file_path_dir = "/home/airscanner100/Data/2023_1220_2317"
# file_path_dir = "/home/airscanner100/Data/2023_1221_1017"

# Process only data files ending in .npy
ext = '.npy'

# Initiate Variables (Eventually pull this from a config file)
count = 1
count_files = 1
sample_rate = 2.4e6
center_freq = 1420.4e6
direction = 270
incline = 45

# Count the Number of Files in the Directory for Array Initialization
for file_name in os.listdir(file_path_dir):
    if file_name.endswith(ext):
        count_files = count_files + 1
    else:
        continue

data_array = np.zeros((count_files,1))

# Process Data in a Directory
for file_name in os.listdir(file_path_dir):
    if file_name.endswith(ext):

        # Generate a full file and path name
        file_in = os.path.join(file_path_dir, file_name)

        # Extract file name prefix and suffix
        split_tup = os.path.splitext(file_name)
        print(split_tup)

        # Extract the file name and extension for saving plots
        file_name_prefix = split_tup[0]
        file_name_ext = split_tup[1]
        plot_out = os.path.join(file_path_dir, file_name_prefix) + "__" + str(direction) + "__" + str(incline) + '.png'
        plot_out_avg = "avgbkrgnd__" + str(direction) + "__" + str(incline) + '.png'

        # Print Status
        print('Processing File #' + str(count).rjust(3, '0') + ":  " + file_in)

        # Read the file
        data_in = np.load(file_in)

        # Create a Data Array
        data_array[count-1] = data_in

        # Plot the PSD of the captured file
        if plot_flag == 1:
            # Turn on Interactive
            plt.ion()

            # Generate a figure and plot the data
            plt.figure()
            psd(data_in, NFFT=2048, Fs=sample_rate / 1e6, Fc=center_freq / 1e6)
            xlabel('Frequency (MHz)')
            ylabel('Sample Relative Power (dB)')
            plt.title(file_name_prefix + "__" + str(direction) + "__" + str(incline))

            # Save the figure
            plt.savefig(plot_out)

            # Show the plot
            plt.show()

            # Pause
            pause(4)

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

# Average column values
data_avg = np.average(data_array, axis=0)

# Plot the average of the background data
if plot_flag == 1:
    # Turn on Interactive
    plt.ion()

    # Generate a figure and plot the data
    plt.figure()
    psd(data_avg, NFFT=2048, Fs=sample_rate / 1e6, Fc=center_freq / 1e6)
    xlabel('Frequency (MHz)')
    ylabel('Sample Relative Power (dB)')
    plt.title("AvgBkgrnd__" + str(direction) + "__" + str(incline))

    # Save the figure
    plt.savefig(plot_out_avg)

    # Show the plot
    plt.show()

# End Program 
print('End Program')
