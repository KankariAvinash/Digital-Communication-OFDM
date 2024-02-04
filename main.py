import numpy as np

import matplotlib.pyplot as plt

from Transmitter.generate_binary_source import generate_frame
from Transmitter.modulator import qam_modulation
from Transmitter.ofdm_mod import OFDM_Modulation

from Channel.simulate_channel import awgn_channel

from Receiver.ofdm_demod import OFDM_Demodulation
from Receiver.demodulator import qam_demodulation
from Receiver.performance import compute_BER

from QAM_Mapper import QAM_Mapper
from ResourceGrid import ResourceGrid

batch_size = 1
num_tx = 1
num_tx_antennas = 1

num_rx = 1
num_rx_antennas = 1

qam_bits = [2,4,6,8]
carrier_freq = 10e3
BER = []

NoisePower = np.arange(-60,100,20)
QAM_SNR = []
resourceGrid = ResourceGrid(guard_carriers = 10,
                            FFT_size = 128,
                            ofdm_symbols = 1,
                            pilot_symbol = 1+1j,
                            Bandwidth = 2e6)

for num_bits_per_symbol in qam_bits:
    qam_bits,qam_values = QAM_Mapper.generate_qam(num_bits_per_symbol = num_bits_per_symbol)
    information_size = resourceGrid._data_symbols * num_bits_per_symbol
    binary_source = generate_frame(batch_size,num_tx,num_tx_antennas,information_size)
    modulator = qam_modulation(binary_source,num_bits_per_symbol,qam_bits,qam_values)
    ofdm_mod = OFDM_Modulation(resourceGrid,modulator)

    for eb_no in NoisePower:
        received_signal = awgn_channel(ofdm_mod,eb_no)
        ofdm_demod = OFDM_Demodulation(resourceGrid,received_signal)
        sink = qam_demodulation(ofdm_demod,qam_bits,qam_values)
        BER.append(compute_BER(binary_source,sink))
    
    QAM_SNR.append(BER)
    BER = []

plt.figure()
for BER in QAM_SNR:
    plt.semilogy(NoisePower,BER,marker='o')
plt.title("SNR vs BER")
plt.xlabel("SNR in dB")
plt.ylabel("Eb/No")
plt.grid(True)
plt.show()