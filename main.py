#!/usr/bin/env python3
# -*- coding: utf-8 -*-
## This is main.m example for ICT Lab (CIT)
# 
#  In this file, all main parameters are defined and all functions are 
#  called. Please refer to this structure also given in the pdf-description
#  to write your code. However you might still modify the main loop, e.g. for 
#  coded/uncoded simulation.
#
###########################################################################
import numpy as np
import matplotlib.pyplot as plt
import math

from Transmitter.generate_frame import generate_frame
from Transmitter.encode_hamming import encode_hamming
from Transmitter.map2symbols import map2symbols
from Transmitter.insert_pilots import insert_pilots
from Transmitter.modulate_ofdm import modulate_ofdm
from Transmitter.filter_tx import filter_tx
from Transmitter.impair_tx_hardware import impair_tx_hardware

from Channel.simulate_channel import simulate_channel

from Receiver.impair_rx_hardware import impair_rx_hardware
from Receiver.filter_rx import filter_rx
from Receiver.demodulate_ofdm import demodulate_ofdm
from Receiver.equalize_ofdm import equalize_ofdm
from Receiver.detect_symbols import detect_symbols
from Receiver.decode_hamming import decode_hamming
from Receiver.digital_sink import digital_sink
# IMPORTANT: 
# Since the modules will be in the folders 'transmitter', 'receiver' and 
# 'Channel', you have add an import command here AND an import command in the
# __init__.py files in the folders! Here are some examples: 
# from transmitter.generate_bits import generate_bits
# ...
# from channel.simulate_channel import simulate_channel
# from reiceiver.filter_rx import filter_rx
# ...


## define parameters 
# set and uncomment the parameters to use

# switch_graph =                  # 1/0--> show/not show the graph

# n_bits =                        # no. of bits to transmit
# parity_check_matrix =           # code parity check matrix
# switch_mod =                    # 0 --> 16-QAM 1-->16-PSK
# usf_filter =                    # upsampling factor of tx filter

# dsf_filter =                    # downsampling factor of rx filter

# tx_power =                       # SNRs to simulate in dB


## generate frame
print("****************Generate Frames *****************")
#frame_size = int(input('Please enter frame size suitable for OFDM: '))
frame_size = 10
switch_graph = 0
b = generate_frame(frame_size, switch_graph)


## Linear block code : Hamming code(7,4) -(n,k)
## n-k = 3 bits bits
print("The total number bits generated are ",64*frame_size)
print("****************Frames Generated *****************")
parity_matrix = np.zeros((4,3))
Identiy_matrix = np.identity(4)
for i in range(len(Identiy_matrix)):
    parity_matrix[i][0] = ((Identiy_matrix[i][1] + Identiy_matrix[i][2] + Identiy_matrix[i][3])%2).astype(int)
    parity_matrix[i][1] = ((Identiy_matrix[i][0] + Identiy_matrix[i][2] + Identiy_matrix[i][3])%2).astype(int)
    parity_matrix[i][2] = ((Identiy_matrix[i][0] + Identiy_matrix[i][1] + Identiy_matrix[i][3])%2).astype(int)

## parity check matrix H = [-(Transpose of p)| I]
parity_check_matrix = (np.concatenate((-np.transpose(parity_matrix.astype(int)),np.identity(3)),1)).astype(int)

############# Number of Zeros ###############
#                    | 4 QAM  | 16 QAM | 64 QAM  |
# Channel coding On  |   0    |   0    |  20     |
# Channel coding Off |   0    |   0    |  20     |
n_zero_padded_bits = 20
switch_off_cc = 0
c = encode_hamming(b, parity_check_matrix, n_zero_padded_bits, switch_off_cc)


print("**************** MODULATION *****************")
#constellation_order = (int)(input("Please enter Modulation order as follows:\n2:4-QAM Modulation\n4:16-QAM Modulation\n6:64 QAM Modulation:\nPlease enter number here: "))
constellation_order = 6
switch_graph = 0
d = map2symbols(c, constellation_order, switch_graph)

print("**************** Insert pilot *****************")
pilot_symbols = np.divide(np.abs(1+1j),(1+1j))
# # from my knowledge for efficient ODFM modulation , The FFT size should be equal to power of Blocks.
## frame size denotes number of messages
## 64bits in each message
fft_size = 1024
N_blocks = int(np.ceil(np.log2(fft_size)))
D = insert_pilots(d, fft_size, N_blocks, pilot_symbols)

print("**************** OFDM Modulation *****************")
cp_size = 10 
switch_graph = 0
z = modulate_ofdm(D, fft_size, cp_size, switch_graph)

print("**************** filter transmitter *****************")
oversampling_factor = 20
switch_graph = 0
switch_off_tx = 0
s = filter_tx(z, oversampling_factor, switch_graph, switch_off_tx)

print("****************Impair Transmitter Hardware *****************")
clipping_threshold = 0.002
switch_graph = 0
x = impair_tx_hardware(s, clipping_threshold, switch_graph)

print("****************BaseBand Channel******************************")
print("Channel Type\n0:AWGN: Additive White Gaussian Noise,\n1:'FSBF': Frequency Selective Block Fading.")
snr_db = 20
channel_type = 0
y = simulate_channel(x, snr_db, channel_type,oversampling_factor)

print("****************Impair Receiver Hardware *****************")
clipping_threshold = 20
switch_graph = 0
s_tilde = impair_rx_hardware(y, clipping_threshold, switch_graph)

print("**************** filter Receiver *****************")
downsampling_factor = oversampling_factor
switch_off_rx = switch_off_tx
switch_graph = 0
z_tilde = filter_rx(s_tilde, downsampling_factor, switch_graph, switch_off_rx)


print("**************** OFDM Demodulation *****************")
switch_graph = 0
D_tilde = demodulate_ofdm(z_tilde, fft_size, cp_size, switch_graph)

print("Number of symbols: ",len(D_tilde))

print("**************** OFDM equalisation *****************")
switch_graph = 0
d_bar= equalize_ofdm(D_tilde, pilot_symbols,switch_graph)

print("**************** DEMODULATION *****************")
switch_graph = 0
c_hat = detect_symbols(d_bar, constellation_order, switch_graph)


print("**************** Channel Coding *****************")
switch_graph = 0
b_hat = decode_hamming(c_hat, parity_check_matrix, n_zero_padded_bits,switch_off_cc, switch_graph)

print("****************Performance *****************")
switch_graph = 1
BER = digital_sink(b, b_hat,snr_db,switch_graph)

