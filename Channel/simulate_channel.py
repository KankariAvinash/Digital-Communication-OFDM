from Channel.AWGN_channel import AWGN_simulate_channel
from Channel.FSBF_channel import FSBF_simulate_channel
import numpy as np

def simulate_channel(x, snr_db, channel_type,oversampling_factor):
    if channel_type:
        print("****************FSBF simulated Channel ******************************")
        signal = []
        for i,data in enumerate(x):
            signal.append(FSBF_simulate_channel(data, snr_db,oversampling_factor))
    else:
        print("****************AWGN simulated Channel******************************")
        signal = []
        for i,data in enumerate(x):
            signal.append(AWGN_simulate_channel(data, snr_db))
    return np.array(signal,dtype=complex)