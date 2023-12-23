from pylab import *
from rtlsdr import *


import matplotlib.pyplot as plt
import numpy as np
import time
from datetime import datetime

sdr = RtlSdr()

# Set Number of Loops
num_loops = 5

# Set a Plot Flag
plot_flag = 1

# Pause Time (sec)
pause_time = 60

# Configure Device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
sdr.gain = 'auto'

# Prepare a Filename
file_prefix = 'data_'
file_path_dir = "C:\\Scan_Files\\data\\"

# Collect Data
for i in range(num_loops):

   # Prepare a Time Date String for Filename
   now = datetime.now()
   year = now.strftime("%Y")
   month = now.strftime("%m")
   day = now.strftime("%d")
   time_now = now.strftime("%H:%M:%S")
   date_time = now.strftime("%Y%m%d__%H%M%S__")
   print("date_time_string = ",date_time)	

   # Print Status
   print(i)

   # String iteration
   #loop = str(i)
   loop = str(i).rjust(3, '0')

   # Create a complete filename
   file_path = file_path_dir + file_prefix + date_time + loop
   
   # Collect Data
   samples = sdr.read_samples(4*256*1024)
   
   # Save the File
   np.save(file_path, samples)

   # Close the File
   del file_path

   # Plot Data
   if plot_flag == 1:
       # Plot the PSD of the captured file
       plt.figure(1)
       psd_samp, freq_samp = psd(samples, NFFT=2048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
       xlabel('Frequency (MHz)')
       ylabel('Samp Relative power (dB)')

   # Pause Before the Next Loop
   time.sleep(pause_time)

# Close the SDR
sdr.close()

# End Program 
print('End Program')
