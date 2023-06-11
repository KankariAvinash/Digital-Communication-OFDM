# calculated error bits = Transmitted bits - expected received bits
# BER = no of error / total number of bits
import numpy as np

def analyze_errors(b, b_hat):
    detected_errors = b ^ b_hat
    count = np.count_nonzero(detected_errors)
    BER = count/(len(b))
    return BER
    