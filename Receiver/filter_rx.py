import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filter_rx(s_tilde, downsampling_factor, switch_graph, switch_off):
    if switch_off:
        print("************* Receiver Filter OFF **************")
        o_psd = np.abs(np.fft.fft(s_tilde[0]))**2
        original_freq = np.fft.fftfreq(len(s_tilde[0]))
        if switch_graph:
            plt.figure()
            plt.plot(original_freq,o_psd)
            plt.xlabel('Frequency')
            plt.ylabel('Power Spectral Density (dB)')
            plt.title("Power Spectrum")
            plt.show()
        return np.array(s_tilde,dtype=complex)
    else:
        downsampled_data = []
        print("************* Receiver Filter ON **************")
        for i,data in enumerate(s_tilde):
            # Apply the matched lowpass filter to the received signal
            cutoff_frequency = 1.0 / downsampling_factor
            filter_order = 100  # Choose an appropriate filter order
            filter_coeffs = signal.firwin(filter_order, cutoff_frequency)
            # Apply the filter to the received signal
            filtered_signal = signal.lfilter(filter_coeffs, 1.0, data)
            # Downsample the filtered signal
            downsampled_signal = filtered_signal[::downsampling_factor]
            downsampled_data.append(downsampled_signal)

        if switch_graph:
            o_psd = np.abs(np.fft.fft(s_tilde[0]))**2
            original_freq = np.fft.fftfreq(len(s_tilde[0]))

            downsampled_psd = np.abs(np.fft.fft(downsampled_data[0]))**2
            downsampled_freq = np.fft.fftfreq(len(downsampled_data[0]))

            plt.figure()
            plt.plot(original_freq,10*np.log10(o_psd),label='Received Signal')
            plt.plot(downsampled_freq,10*np.log10(downsampled_psd),label='Downsampled Received Signal')
            plt.xlabel('Frequency')
            plt.ylabel('Power Spectral Density (dB)')
            plt.title("Power Spectrum")
            plt.legend()
            plt.show()
        return np.array(downsampled_data,dtype=complex)



