
import numpy as np
import matplotlib.pyplot as plt

def impair_rx_hardware(y, rxthresh, switch_graph):
    #signal clipping depending on threshold
    clipped_signal = []
    for i,data in enumerate(y):
        clipped_signal.append(np.clip(data,a_min=-rxthresh,a_max=rxthresh))
    clipped_signal = np.array(clipped_signal,dtype=complex)
    
    if(switch_graph):
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(np.abs(y[0]))
        plt.title("Received Non-Filtered signal")
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