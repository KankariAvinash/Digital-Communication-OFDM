import numpy as np
import matplotlib.pyplot as plt

def qam_4_modulation(gray_code,switch_graph):
    bits = [
      [0,0],
      [0,1],
      [1,0],
      [1,1]]
    bit_values = [
      -1-1j,
      -1+1j,
      +1-1j,
      +1+1j
    ]
    #mapping bits with 4 QAM Amplitude Values
  
    re_format_signal = np.reshape(gray_code,(len(gray_code)//2,2))
    re_format_signal = np.array(re_format_signal)

    mapping = []
    for i in range(len(re_format_signal)):
      for k in range(len(bits)):
        if (np.all(np.equal(re_format_signal[i],bits[k]))):
          mapping.append(bit_values[k])
    mapping = np.array(mapping,complex)
    encoded = np.ravel(mapping)
    
    normalized_signal = np.array(np.divide(encoded,np.max(np.abs(encoded))),dtype=complex)


    if switch_graph:
      plt.figure()
      plt.scatter(np.real(bit_values),np.imag(bit_values),color="blue")
      plt.axhline(0, color='red')
      plt.axvline(0, color='blue')
      for i, txt in enumerate(bits):
        plt.annotate(txt,(np.real(bit_values[i]),np.imag(bit_values[i])))
      plt.title('4-QAM Constellation Diagram')
      plt.xlabel('Quadrature Part')
      plt.ylabel('In-Phase Part')
      plt.grid(True)
      plt.figure()

      plt.subplot(2,1,1)
      plt.plot(np.abs(normalized_signal))
      plt.title('Sample waveform')
      plt.xlabel('time')
      plt.ylabel('Amplitude')
      plt.grid(True)
      plt.subplot(2,1,2)
      freq = np.fft.fftfreq(len(normalized_signal))
      plt.plot(freq,10*np.log10((np.abs(np.fft.fft(normalized_signal))**2)))
      plt.title('Normalized Power of each frame')
      plt.xlabel('freq')
      plt.ylabel('power in db')
      plt.grid(True)
      plt.show()
    
    return normalized_signal
