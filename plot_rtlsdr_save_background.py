from pylab import *
from rtlsdr import *

sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.4e6
sdr.center_freq = 1420.4e6
#sdr.center_freq = 94.9e6
sdr.gain = 10
samples_background = sdr.read_samples(4*256*1024)

# Save Samples To File
file_path = "/home/airscanner101/Data/background_4x256x1024"
np.save(file_path, samples_background)


# Close the file
del file_path

# Close the SDR
sdr.close()

# use matplotlib to estimate and plot the PSD
psd(samples_background, NFFT=2048, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
xlabel('Frequency (MHz)')
ylabel('Relative power (dB)')

show()

