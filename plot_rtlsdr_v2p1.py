from pylab import *
from rtlsdr import *
import matplotlib.pyplot as plt


sdr = RtlSdr()

# Configure Device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
sdr.gain = 10
samples = sdr.read_samples(256*1024)

# Save Samples To File
file_path = "/home/airscanner101/Data/background_256x1024.bin"

# Open the file in binary read mode 
with open(file_path, 'rb') as file: 
    # Read the contents of the file 
    samples_background = file.read() 

# Close the File
file.close()

# Close the SDR
sdr.close()

# Plot the PSD of the captured file
#plt.figure(1)
#plt.psd(samples, NFFT=2048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
#xlabel('Frequency (MHz)')
#ylabel('Samp Relative power (dB)')
#plt.show()

# Plot the PSD of the background file
plt.figure(2)
plt.psd(samples_background, NFFT=2048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Bkgrnd Relative power (dB)')
plt.show()