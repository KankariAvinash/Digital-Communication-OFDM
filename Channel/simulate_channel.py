import numpy as np
import tensorflow as tf
def AWGN_channel(tx_data,no):
    y_volts = []
    for _,data in enumerate(tx_data):
        signal_power = np.mean(np.square(np.abs(data)))
        SNR_Lin = np.power(10,no/10)
        noise_power = signal_power/SNR_Lin
        noise = np.random.normal(0, np.sqrt(noise_power / 2), size=len(data)) + 1j*np.random.normal(0, np.sqrt(noise_power / 2), size=len(data))
        y_volts.append(data + noise)
    return np.array(y_volts).astype(complex)


def receiver_information(user_tx_data,no):
    user_data = []
    num_tx_antennas,ofdm_symbols,data = user_tx_data.shape
    for i in range(0,num_tx_antennas):
        user_data.append(AWGN_channel(user_tx_data[i],no))
    return user_data


def awgn_channel(input,no):
    batch_size,num_tx,num_tx_antennas,ofdm_symbols,data = input.shape
    final_frame = []
    data_frame = []
    for i in range(0,batch_size):
        for j in range(0,num_tx):
            data_frame.append(receiver_information((input.numpy())[i,j],no))
        final_frame.append(data_frame)
        data_frame =[]

    final_frame = tf.convert_to_tensor(final_frame)
    return final_frame