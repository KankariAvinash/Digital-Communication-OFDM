import matplotlib.pyplot as plt
import numpy as np

def qam_64_modulation(gray_code,switch_graph):
    #constellation diagram points
    bits = [
      [0,0,0,0,0,0],
      [0,0,0,0,0,1],
      [0,0,0,0,1,0],
      [0,0,0,0,1,1],
      [0,0,0,1,0,0],
      [0,0,0,1,0,1],
      [0,0,0,1,1,0],
      [0,0,0,1,1,1],
      [0,0,1,0,0,0],
      [0,0,1,0,0,1],
      [0,0,1,0,1,0],
      [0,0,1,0,1,1],
      [0,0,1,1,0,0],
      [0,0,1,1,0,1],
      [0,0,1,1,1,0],
      [0,0,1,1,1,1],
      [0,1,0,0,0,0],
      [0,1,0,0,0,1],
      [0,1,0,0,1,0],
      [0,1,0,0,1,1],
      [0,1,0,1,0,0],
      [0,1,0,1,0,1],
      [0,1,0,1,1,0],
      [0,1,0,1,1,1],
      [0,1,1,0,0,0],
      [0,1,1,0,0,1],
      [0,1,1,0,1,0],
      [0,1,1,0,1,1],
      [0,1,1,1,0,0],
      [0,1,1,1,0,1],
      [0,1,1,1,1,0],
      [0,1,1,1,1,1],
      [1,0,0,0,0,0],
      [1,0,0,0,0,1],
      [1,0,0,0,1,0],
      [1,0,0,0,1,1],
      [1,0,0,1,0,0],
      [1,0,0,1,0,1],
      [1,0,0,1,1,0],
      [1,0,0,1,1,1],
      [1,0,1,0,0,0],
      [1,0,1,0,0,1],
      [1,0,1,0,1,0],
      [1,0,1,0,1,1],
      [1,0,1,1,0,0],
      [1,0,1,1,0,1],
      [1,0,1,1,1,0],
      [1,0,1,1,1,1],
      [1,1,0,0,0,0],
      [1,1,0,0,0,1],
      [1,1,0,0,1,0],
      [1,1,0,0,1,1],
      [1,1,0,1,0,0],
      [1,1,0,1,0,1],
      [1,1,0,1,1,0],
      [1,1,0,1,1,1],
      [1,1,1,0,0,0],
      [1,1,1,0,0,1],
      [1,1,1,0,1,0],
      [1,1,1,0,1,1],
      [1,1,1,1,0,0],
      [1,1,1,1,0,1],
      [1,1,1,1,1,0],
      [1,1,1,1,1,1]
      ]
    bit_values = [
      -7+7j,
      -5+7j,
      -1+7j,
      -3+7j,
      +7+7j,
      +5+7j,
      +1+7j,
      +3+7j,
      -7+5j,
      -5+5j,
      -1+5j,
      -3+5j,
      +7+5j,
      +5+5j,
      +1+5j,
      +3+5j,
      -7+1j,
      -5+1j,
      -1+1j,
      -3+1j,
      +7+1j,
      +5+1j,
      +1+1j,
      +3+1j,
      -7+3j,
      -5+3j,
      -1+3j,
      -3+3j,
      +7+3j,
      +5+3j,
      +1+3j,
      +3+3j,
      -7-7j,
      -5-7j,
      -1-7j,
      -3-7j,
      +7-7j,
      +5-7j,
      +1-7j,
      +3-7j,
      -7-5j,
      -5-5j,
      -1-5j,
      -3-5j,
      +7-5j,
      +5-5j,
      +1-5j,
      +3-5j,
      -7-1j,
      -5-1j,
      -1-1j,
      -3-1j,
      +7-1j,
      +5-1j,
      +1-1j,
      +3-1j,
      -7-3j,
      -5-3j,
      -1-3j,
      -3-3j,
      +7-3j,
      +5-3j,
      +1-3j,
      +3-3j,
    ]

    re_format_signal = np.reshape(gray_code,(len(gray_code)//6,6))
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
      plt.title('64-QAM Constellation Diagram')
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