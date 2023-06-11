import numpy as np
import matplotlib.pyplot as plt

def modulate_ofdm(D, fft_size, cp_size, switch_graph):
    modulate_ofdm = []
    for i,data in enumerate(D):
        modulate_ofdm.append(np.fft.ifft(data,fft_size))
    modulate_ofdm = np.array(modulate_ofdm,dtype=complex)
    
    cyc_modulate_ofdm = []
    for i,data in enumerate(modulate_ofdm):
        cp = data[-cp_size:]
        cyc_modulate_ofdm.append(np.hstack([modulate_ofdm[i],cp]))
    cyc_modulate_ofdm = np.array(cyc_modulate_ofdm,dtype=complex)
    
    if switch_graph:
        freq = np.fft.fftfreq(len(modulate_ofdm[0]))
        plt.figure()
        plt.subplot(2,1,1)
        plt.xlabel("frequency")
        plt.ylabel("Power in db")
        plt.title("Power Spectrum")
        plt.plot(freq,10*np.log10(np.abs(np.fft.fft(modulate_ofdm[0])**2) + 1e-10))
        plt.subplot(2,1,2)
        plt.plot(np.abs(modulate_ofdm[0]))
        plt.xlabel("samples")
        plt.ylabel("Amplitude(V)")
        plt.title("Time Signal")
        plt.show()

    return cyc_modulate_ofdm 

    