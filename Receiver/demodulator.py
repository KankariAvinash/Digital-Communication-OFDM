import numpy as np
import tensorflow as tf
def demodulation(modulation,qam_bits,qam_values):
    qam_signal = qam_bits
    qam_values = qam_values
    
    num_rx_ant,information = modulation.shape 
    modulation = np.array(modulation).reshape(-1)
    #demapping
    #distances = np.abs(np.expand_dims(modulation, axis=1) - np.divide(qam_values,np.max(np.abs(qam_values))))
    distances = np.abs(np.expand_dims(modulation, axis=1) - qam_values)
    demodulated_indices = np.argmin(distances, axis=1)
    demodulated_indices = np.array(demodulated_indices)
  
    demodulated_values = []
    for i in range(len(demodulated_indices)):
        index = demodulated_indices[i]
        demodulated_values.append(qam_signal[index])
    demodulated_values = np.array(np.squeeze(demodulated_values).reshape(-1),dtype=int)
    demodulated_values = np.reshape(demodulated_values,(num_rx_ant,len(demodulated_values)//num_rx_ant))
    return demodulated_values

def qam_demodulation(binary_source,qam_bits,qam_values):
    batch_size,num_rx,num_rx_antennas,information = binary_source.shape 
    data_rx = []
    data_total_batch = []
    for i in range(0,batch_size):
        for j in range(0,num_rx):
            data_rx.append(demodulation((binary_source.numpy())[i,j],qam_bits,qam_values))
        data_total_batch.append(data_rx)
        data_rx = []
    data_total_batch = tf.convert_to_tensor(np.array(data_total_batch).astype(int))
    return data_total_batch