import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def qam_64_demodulation(gray_code,switch_graph):
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
  
  distances = np.abs(np.expand_dims(gray_code, axis=1) - np.divide(bit_values,np.max(np.abs(bit_values))))
  demodulated_indices = np.argmin(distances, axis=1)
  demodulated_indices = np.array(demodulated_indices)
  
  

  demodulated_values = []
  for i in range(len(demodulated_indices)):
    index = demodulated_indices[i]
    demodulated_values.append(bits[index])
  demodulated_values = np.array(np.squeeze(demodulated_values).reshape(-1),dtype=int)
  
  

  if switch_graph:
    plt.figure()
    plt.scatter(np.real(bit_values),np.imag(bit_values),color="blue")
    plt.scatter(np.real(gray_code),np.imag(gray_code),color="red")
    plt.axhline(0, color='red')
    plt.axvline(0, color='blue')
    for i, txt in enumerate(bits):
      plt.annotate(txt,(np.real(bit_values[i]),np.imag(bit_values[i])))
    plt.title('64-QAM Constellation Diagram')
    plt.xlabel('Quadrature Part')
    plt.ylabel('In-Phase Part')
    plt.grid(True)
    plt.show()
  return demodulated_values
    