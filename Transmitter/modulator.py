import numpy as np
import tensorflow as tf
def modulation(gray_code,num_bits_per_symbol,qam_bits,qam_values):   
    qam_signal = qam_bits
    qam_values = qam_values.astype(complex)
    
    num_tx_ant,information = gray_code.shape
    gray_code = np.array(gray_code).reshape(-1)
    binary_code = np.reshape(gray_code,(len(gray_code)//num_bits_per_symbol,num_bits_per_symbol)).astype(int)
    
    mapping = []
    for _,data in enumerate(binary_code):
        for i,data_point in enumerate(qam_signal):
            if(np.all(data == data_point)):
                mapping.append(qam_values[i])
    mapping = np.array(mapping).astype(complex)
    mapping = np.reshape(mapping,(num_tx_ant,len(mapping)//num_tx_ant))
    return mapping

def qam_modulation(binary_source,num_bits_per_symbol,qam_bits,qam_values):
    batch_size,num_tx,num_tx_antennas,information = binary_source.shape 
    data_tx = []
    data_total_batch = []
    for i in range(0,batch_size):
        for j in range(0,num_tx):
            data_tx.append(modulation((binary_source.numpy())[i,j],num_bits_per_symbol,qam_bits,qam_values))
        data_total_batch.append(data_tx)
        data_tx = []
    data_total_batch = tf.convert_to_tensor(np.array(data_total_batch).astype(complex))
    data_total_batch = tf.cast(data_total_batch,dtype=tf.complex64)
    return data_total_batch
    
