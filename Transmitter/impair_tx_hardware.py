import matplotlib.pyplot as plt
import numpy as np

def impair_tx_hardware(s, clipping_threshold, switch_graph):
    clipped_signal = []
    for i,data in enumerate(s):
        clipped_signal.append(np.clip(data,a_min=-clipping_threshold,a_max= clipping_threshold))
    clipped_signal = np.array(clipped_signal,dtype=complex)
    if switch_graph:
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(np.abs(s[0]))
        plt.title("Filtered signal")
        plt.xlabel("Time(ms)")
        plt.ylabel("Amplitude(V)")
        plt.grid(True)
        plt.subplot(2,1,2)
        plt.plot(np.abs(clipped_signal[0]))
        plt.title("clipped signal")
        plt.xlabel("Time(ms)")
        plt.ylabel("Amplitude(V)")
        plt.grid(True)
        plt.show()
        
    return clipped_signal