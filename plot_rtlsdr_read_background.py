from pylab import *
from rtlsdr import *
import matplotlib.pyplot as plt

sdr = RtlSdr()

# Configure Device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
#sdr.center_freq = 94.9e6
sdr.gain = 10
samples = sdr.read_samples(4*256*1024)

# Get the background file to read
file_path = "/home/airscanner101/Data/background_4x256x1024.npy"

# Read the background file
samples_background = np.load(file_path)

# Close the File
del file_path

# Close the SDR
sdr.close()

# Plot the PSD of the captured file
plt.figure(1)
psd_samp, freq_samp = psd(samples, NFFT=2048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Samp Relative power (dB)')


# Plot the PSD of the background file
plt.figure(2)
psd_back, freq_back = psd(samples_background, NFFT=2048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Bkgrnd Relative power (dB)')

# Subtract of the background signal
psd_delta = psd_samp - psd_back

# Plot the PSD of the sample - background
plt.figure(3)
plot(psd_delta)
xlabel('Frequency (MHz)')
ylabel('Samp-Bkgrnd Relative power (dB)')
plt.show()


