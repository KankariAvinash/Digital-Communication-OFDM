import matplotlib.pyplot as plt
import numpy as np
import math

from Transmitter.qam_4_modulation import qam_4_modulation
from Transmitter.qam_16_modulation import qam_16_modulation
from Transmitter.qam_64_modulation import qam_64_modulation

def binarytogray(n):
    gray_code = np.zeros(len(n))
    for i in range(0,len(n)):
        if i==0:
            gray_code[i] = n[i]
        else:
            gray_code[i] = n[i] ^ n[i-1]
    return gray_code.astype(int)

def map2symbols(c, constellation_order, switch_graph):
    gray_code = binarytogray(c)
    gray_code = np.array(gray_code)
    
    if constellation_order == 2:
        print("****************4 QAM Modulation*****************")
        modulatedSignal = qam_4_modulation(gray_code,switch_graph)
        return modulatedSignal
    elif constellation_order == 4:
        print("****************16 QAM Modulation*****************")
        modulatedSignal= qam_16_modulation(gray_code,switch_graph)
        return modulatedSignal
    elif constellation_order == 6:
        print("****************64 QAM Modulation*****************")
        modulatedSignal= qam_64_modulation(gray_code,switch_graph)
        return modulatedSignal
    else:
        raise Exception('Please enter correct constellation order')