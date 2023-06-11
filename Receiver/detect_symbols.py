import numpy as np
from Receiver.qam_4_demodulation import qam_4_demodulation
from Receiver.qam_16_demodulation import qam_16_demodulation
from Receiver.qam_64_demodulation import qam_64_demodulation

def graytobinary(n):  # Conversion of gray code to binary code
    binary_code = np.zeros(len(n))
    #binary_code = n[0]
    for i in range(1, len(n)):
        if n[i] == 0:
            binary_code[i] += binary_code[i-1]
        else:
            binary_code[i] += 1 - binary_code[i-1]
    return binary_code.astype(int)

def detect_symbols(d_bar, constellation_order, switch_graph):
    if constellation_order == 2:
        print("****************4 QAM Demodulation*****************")
        modulatedSignal = qam_4_demodulation(d_bar,switch_graph)
        gray2bin = graytobinary(modulatedSignal)
        return np.array(gray2bin,dtype=int)
    
    elif constellation_order == 4:
        print("****************16 QAM Demodulation*****************")
        modulatedSignal= qam_16_demodulation(d_bar,switch_graph)
        gray2bin = graytobinary(modulatedSignal)
        return gray2bin
    
    elif constellation_order == 6:
        print("****************64 QAM Demodulation*****************")
        modulatedSignal= qam_64_demodulation(d_bar,switch_graph)
        gray2bin = graytobinary(modulatedSignal)
        return np.array(gray2bin,dtype=int)
    
    else:
        raise Exception('Please enter correct constellation order')