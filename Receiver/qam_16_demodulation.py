import matplotlib.pyplot as plt
import numpy as np

def qam_16_demodulation(gray_code,switch_graph):
  #constellation diagram points
  bits = [
      [0,0,0,0],
      [0,0,0,1],
      [0,0,1,0],
      [0,0,1,1],
      [0,1,0,0],
      [0,1,0,1],
      [0,1,1,0],
      [0,1,1,1],
      [1,0,0,0],
      [1,0,0,1],
      [1,0,1,0],
      [1,0,1,1],
      [1,1,0,0],
      [1,1,0,1],
      [1,1,1,0],
      [1,1,1,1]
      ]
  bit_values = [
      -3-3j,
      -1-3j,
      +3-3j,
      +1-3j,
      -3-1j,
      -1-1j,
      +3-1j,
      +1-1j,
      -3+3j,
      -1+3j,
      +3+3j,
      +1+3j,
      -3+1j,
      -1+1j,
      +3+1j,
      +1+1j,
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
    plt.title('16-QAM Constellation Diagram')
    plt.xlabel('Quadrature Part')
    plt.ylabel('In-Phase Part')
    plt.grid(True)
    plt.show()
  return demodulated_values
    