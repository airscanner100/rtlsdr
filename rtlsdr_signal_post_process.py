from pylab import *
import os
import matplotlib.pyplot as plt
import numpy as np

# Set a Plot Flag
plot_sample_flag = 1
plot_avg_flag = 1

# Get the background file to read
data_path_dir = "/home/airscanner100/Data/2023_0000_0000"
bkgnd_path_dir = "/home/airscanner100/Data/2023_1221_BKGRND"
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

# Initialize arrays for averaging
psd_array = np.array(zeros(psd_nfft))
freq_array = np.array(zeros(psd_nfft))

# Set up a path and filename for the average background
plot_out_avg = os.path.join(bkgnd_path_dir, "avgbkrgnd__" + str(direction) + "__" + str(incline) + '.png')
save_out_avg = os.path.join(bkgnd_path_dir, "avgbkrgnd__" + str(direction) + "__" + str(incline))

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

        # Add to the PSD array
        psd_array = psd_array + psd_samp
        freq_array = freq_array + freq_samp

        # Update counter
        count = count + 1

        # Close the File
        del file_in

        # Clear the data
        del data_in

    else:
        continue

# Generate an average PSD
psd_array_avg = psd_array / (count - 1)
freq_array_avg = freq_array / (count - 1)

# Save averaged data to file
np.savez(save_out_avg, psd_array_avg_vector=psd_array_avg, freq_array_avg_vector=freq_array_avg)

# Plot the average of the background data
if plot_avg_flag == 1:

    # Turn on Interactive
    plt.ion()

    # Generate a figure and plot the data
    plt.figure()
    plt.plot(freq_array_avg, psd_array_avg)
    xlabel('Frequency (MHz)')
    ylabel('Sample Relative Power')
    plt.title("AvgBkGrnd__" + str(direction) + "__" + str(incline))

    # Save the figure
    plt.savefig(plot_out_avg)

    # Show the average plot
    plt.show()

    # Close the average plot
    plt.close()

# End Program 
print('End Program')
