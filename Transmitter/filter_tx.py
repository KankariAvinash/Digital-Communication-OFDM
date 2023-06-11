import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def filter_tx(z, oversampling_factor, switch_graph, switch_off):
    if switch_off:
        print("************* Transmitter Filter OFF **************")
        o_psd = np.abs(np.fft.fft(z[0]))**2
        original_freq = np.fft.fftfreq(len(z[0]))
        if switch_graph:
            plt.figure()
            plt.plot(original_freq,10 * np.log10(o_psd+ 1e-10) )
            plt.xlabel('Frequency')
            plt.ylabel('Power Spectral Density (dB)')
            plt.title("Power Spectrum")
            plt.show()
        return np.array(z,dtype=complex)
    else:
        print("************* Transmitter Filter ON **************")
        filtered_signal = []
        # Filter specifications
        for i,data in enumerate(z):
            cutoff_frequency = 1.0 / oversampling_factor
            # Design the low-pass filter
            filter_order = 100  # Choose an appropriate filter order
            filter_coeffs = signal.firwin(filter_order, cutoff_frequency)

            # Upsample the OFDM sequence
            #upsampled_sequence = np.repeat(data, oversampling_factor)
            #filtered_sequence = signal.lfilter(filter_coeffs, 1.0, upsampled_sequence)
        
            # Apply the filter to the OFDM sequence
            filtered_sequence = signal.lfilter(filter_coeffs, 1.0, data)
            filtered_signal.append(filtered_sequence)
             
        if switch_graph:
            # Calculate the power spectral density (PSD) of the original and filtered sequences
            o_psd = np.abs(np.fft.fft(z[0]))**2
            fil_psd = np.abs(np.fft.fft(filtered_signal[0]))**2

            original_freq = np.fft.fftfreq(len(z[0]))
            filtered_freq = np.fft.fftfreq(len(filtered_signal[0]))

            plt.plot(original_freq, 10 * np.log10(o_psd + 1e-10)  , label='Original')
            plt.plot(filtered_freq, 10 * np.log10(fil_psd), label='Filtered')
            plt.xlabel('Frequency')
            plt.ylabel('Power Spectral Density (dB)')
            plt.title("Power Spectrum")
            plt.legend()
            plt.show()

        return np.array(filtered_signal,dtype=complex)
