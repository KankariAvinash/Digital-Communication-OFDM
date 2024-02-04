import numpy as np
import tensorflow as tf
from scipy.fft import fft
def ofdm_demodulation_data(Rx_data,ResourceGrid):
    guard_carriers = ResourceGrid._guard_carriers
    fft_size = ResourceGrid._fft_size 
    pilot_interval = ResourceGrid._pilot_interval + 1
    removed_insert_pilots = []

    fft_information = fft(Rx_data,fft_size)
    removed_guard_carriers = fft_information[guard_carriers:(len(fft_information)-guard_carriers)]
    
    for i in range(1,len(removed_guard_carriers)+1):
        if np.mod(i,pilot_interval)!=0:
            removed_insert_pilots.append(removed_guard_carriers[i-1])
    removed_insert_pilots = np.array(removed_insert_pilots).astype(complex)
    return removed_insert_pilots


def receiver_information(user_rx_data,ResourceGrid):
    rx_ant,ofdm_symbols,data = user_rx_data.shape
    user_data =[]
    final_data = []
    for i in range(0,rx_ant):
        for j in range(0,ofdm_symbols):
            user_data.append(ofdm_demodulation_data(user_rx_data[i,j],ResourceGrid))
        user_data = np.array(np.array(user_data).reshape(-1)).astype(complex)
        final_data.append(user_data)
        user_data = []
    final_data = np.array(final_data).astype(complex)
    return final_data


def OFDM_Demodulation(ResourceGrid,input):
    batch_size,num_rx,num_rx_antennas,num_ofdm_symbols,data = input.shape
    data_frame = []
    final_frame = []
    for i in range(0,batch_size):
        for j in range(0,num_rx):
            data_frame.append(receiver_information((input.numpy())[i,j],ResourceGrid))
        final_frame.append(data_frame)
        data_frame = []

    final_frame = tf.convert_to_tensor(final_frame)
    final_frame = tf.cast(final_frame,dtype=tf.complex64)
    return final_frame