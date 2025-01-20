import os
import numpy as np

def process_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            # Do something with the file
            print(f"Processing {filename}")
            # Example: Read the file
            with open(filepath, 'r') as file:
                [psd_array_avg,freq_array_avg] = np.load(filepath)
                print(psd_array_avg)
                print(freq_array_avg)
                #content = file.read()
                # Process the content as needed

if __name__ == "__main__":
    directory_to_process = "C:\\Users\\airscanner100\\Downloads\\20250116__2014\\data\\"
    process_files(directory_to_process)