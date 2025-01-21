import os
import numpy as np
import matplotlib.pyplot as plt
import time

# Set flag
plot_flag = 1

# Set parameters
low_limit = -0.10

def process_files(directory):
    for filename in os.listdir(directory):
        prefix, extension = os.path.splitext(filename)
        filepath = os.path.join(directory, filename)
        filepath_out = os.path.join(directory, prefix)
        if os.path.isfile(filepath) and filename.endswith('.npy'):
            # Do something with the file
            print(f"Processing {filename}")
            # Example: Read the file
            with open(filepath, 'r') as file:
                [psd_array_avg,freq_array_avg] = np.load(filepath)
                
                # Preview the Data
                #print(psd_array_avg)
                #print(freq_array_avg)
               
                #Process the content as needed
                psd_array_avg_mean = np.average(psd_array_avg)
                print(psd_array_avg_mean)

                # Plot Data
                if plot_flag == 1:

		    # Turn on Interactive
                    plt.ion()

    		    # Plot the PSD of the Averaged Data
                    plt.figure(1)
                    plt.plot(freq_array_avg,psd_array_avg)
                    plt.xlabel('Frequency (MHz)')
                    plt.ylabel('Samp Relative power (dB)')
                    plt.title(prefix + " Avg_PSD=" + f"{psd_array_avg_mean:0.3f}")
                    plt.ylim(low_limit - low_limit, 4 * -low_limit)

                    # Show the Plot
                    plt.show()

                    # Save the Plot 
                    plt.savefig(filepath_out)

                    # Pause
                    #time.sleep(5)

                    # Close the Average Plot
                    plt.close()


if __name__ == "__main__":
    directory_to_process = "C:\\Users\\airscanner100\\Downloads\\20250116__2014\\data\\"
    process_files(directory_to_process)
    print("Input directory: " + directory_to_process)
