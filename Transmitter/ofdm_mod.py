import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from scipy.fft import ifft,fft

def ofdm_modulation_data(Tx_data,ResourceGrid):
    guard_carriers = ResourceGrid._guard_carriers
    pilot_symbol = ResourceGrid._pilot_symbol
    pilot_interval = ResourceGrid._pilot_interval
    OFDM_symbols = len(Tx_data)//ResourceGrid._data_carriers
    split_data = np.reshape(Tx_data,(OFDM_symbols,len(Tx_data)//OFDM_symbols))

    OFDM_stream = []
    for i,data in enumerate(split_data):
        pilot_data= np.insert(data,range(pilot_interval,len(data)+1,pilot_interval),pilot_symbol)
        insert_cp = np.hstack([pilot_data[0:guard_carriers],pilot_data,pilot_data[:guard_carriers]])
        OFDM_stream.append(np.fft.ifft(insert_cp,ResourceGrid._fft_size))
    return np.array(OFDM_stream).astype(complex)


def transmitter_information(user_tx_data,ResourceGrid):
    user_data = []
    for _,data in enumerate(user_tx_data):
        user_data.append(ofdm_modulation_data(data,ResourceGrid))
    return user_data

def OFDM_Modulation(ResourceGrid,input):
    batch_size,num_tx,num_tx_antennas,data = input.shape
    final_frame = []
    data_tx = []
    for i in range(0,batch_size):
        for j in range(0,num_tx):
            data_tx.append(transmitter_information((input.numpy())[i,j],ResourceGrid))
        final_frame.append(data_tx)
        data_tx = []
    
    final_frame = tf.convert_to_tensor(final_frame)
    final_frame = tf.cast(final_frame,dtype=tf.complex64)
    # plt.figure()
    # plt.subplot(2,1,1)
    # plt.plot(np.abs(final_frame.numpy().reshape(-1)))
    # plt.subplot(2,1,2)
    # plt.plot(ResourceGrid._allSubCarrierFrequencies,10*np.log10(np.abs(np.fft.fft(final_frame.numpy().reshape(-1)))))
    # plt.show()
    return final_frame