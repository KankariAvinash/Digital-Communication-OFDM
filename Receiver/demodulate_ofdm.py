import numpy as np
import matplotlib.pyplot as plt
def demodulate_ofdm(z_tilde, fft_size, cp_size, switch_graph):
    frame, sym = z_tilde.shape
    removeCp = []
    for i,data in enumerate(z_tilde):
        removeCp.append(data[cp_size:])
    removeCp = np.array(removeCp)

    #perform DFT
    demod = []
    for j,data in enumerate(removeCp):
        demod.append(np.fft.fft(data,int(np.log2(fft_size))))
    demod = np.array(demod,dtype=complex)
    
    #remove pilot elements
    demod = np.array(np.squeeze(demod).reshape(-1),dtype=complex)
    pilot_interval = frame
    removed_insert_pilots = [x for i, x in enumerate(demod) if i%pilot_interval !=0]
    removed_insert_pilots = np.array(removed_insert_pilots,dtype=complex)
    
    if switch_graph:
        freq = np.fft.fftfreq(len(demod))
        plt.figure()
        plt.subplot(2,1,1)
        plt.plot(freq,10*np.log10(np.abs(np.fft.fft(demod**2) + 1e-10)))
        plt.xlabel("frequency")
        plt.ylabel("Power in db")
        plt.title("Power Spectrum")
        plt.subplot(2,1,2)
        plt.plot(np.abs(demod))
        plt.xlabel("samples")
        plt.ylabel("Amplitude(V)")
        plt.title("Time Signal")
        plt.show()
    return removed_insert_pilots
    