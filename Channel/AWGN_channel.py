import numpy as np
  
def AWGN_simulate_channel(tx, snr_db):
    # snr = 10 ** (snr_db / 10.0)
    # signal_power = np.sum(np.abs(tx) ** 2) / len(tx)
    # noise_power = signal_power / snr
    # noise = np.sqrt(noise_power/2)*(np.random.randn(len(tx)) + 1j*(np.random.randn(len(tx))))
    
    SNR_Lin = np.power(10,snr_db/10)
    signal_power = np.sum(np.abs(tx) ** 2) / len(tx)
    noise_power = signal_power/SNR_Lin
    #noise = np.random.normal(0, np.sqrt(noise_power / 2), size=len(tx))

    noise = np.random.normal(0, np.sqrt(SNR_Lin / 2), size=len(tx))
    y_volts = tx  + noise
    
    return np.array(y_volts,dtype=complex)