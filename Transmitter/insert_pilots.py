import numpy as np
def insert_pilots(d, fft_size, N_blocks, pilot_symbols):
    pilot_interval = len(d)//N_blocks
    
    pilot_carriers= np.insert(d,range(pilot_interval,len(d)+1,pilot_interval),pilot_symbols)
    pilot_carriers = np.array(pilot_carriers,dtype=complex)
    pilot_carriers_arrays = np.reshape(pilot_carriers,(len(pilot_carriers)//N_blocks,N_blocks))
    
    return np.array(pilot_carriers_arrays,dtype=complex)