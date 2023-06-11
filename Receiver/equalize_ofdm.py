
import matplotlib.pyplot as plt
import numpy as np
def channel_estimation(data,hest):
    return np.array(data/hest)

def normalized_lms(data,pilot_symbols):
    N = len(data)

    d = np.zeros(N,dtype=complex)
    for i in range(1,N):
        if i%4==0:
            d[i] = pilot_symbols
    d = np.array(d)

    mu = 0.99
    lambda_nlms = 1
    M = 10

    s_hat_nlms = np.zeros(N,dtype=complex)
    error_nlms = np.transpose(np.zeros(N,dtype=complex))
    e_nlms = np.zeros(M,dtype=complex)
    x_nlms = np.zeros(M,dtype=complex) #regressor vector (column)

    for i in range(1,N):
        x_nlms = np.concatenate(([data[i]], x_nlms[:M-1]))
        s_hat_nlms[i] = np.dot(e_nlms, x_nlms)
        error_nlms[i] = d[i] - s_hat_nlms[i]
        e_nlms = e_nlms + (mu * x_nlms * np.conj(error_nlms[i])) / (np.linalg.norm(x_nlms) ** 2 + lambda_nlms)

    return np.array(s_hat_nlms)

def recursive_lms(data):
    lambda_rls = 4
    M = 50
    N = len(data)

    d = np.max(np.abs(data))*(np.array(np.ones(len(data))+1j*np.ones(len(data)),dtype=complex))

    # Equalizer initialization
    e_rls = np.zeros(M,dtype=complex)
    x_rls = np.zeros(M,dtype=complex)
    error_rls = np.zeros(N,dtype=complex)
    s_hat = np.zeros(N,dtype=complex)

    P = np.eye(M)
    lambda_inv = 1 / lambda_rls
    Rxx_inv = np.eye(M)

    # Adaptive Equalization
    for i in range(0,N):
        x_rls = np.concatenate(([data[i]], x_rls[:-1]))
        kFac = lambda_inv * Rxx_inv @ x_rls.conj() / (1 + lambda_inv * x_rls.conj().T @ Rxx_inv @ x_rls)
        Rxx_inv = lambda_inv * Rxx_inv - lambda_inv * np.outer(kFac, x_rls.conj()) @ Rxx_inv
        s_hat[i] = x_rls.conj().T @ e_rls
        error_rls[i] = s_hat[i] - d[i]
        # update filter coefficients
        e_rls = e_rls - kFac * error_rls[i]
    
    return np.array(s_hat)

def equalize_ofdm(D_tilde, pilot_symbols, switch_graph):
    #*****************RLMS******************
    print("*********** R-LMS Adaptive Filter ************")
    rlms_estimated_signal = recursive_lms(D_tilde)
    rlms_estimated_signal = np.array(rlms_estimated_signal,dtype=complex)

    #*****************RLMS end******************
    if switch_graph:
        plt.figure()
        plt.plot(np.abs(D_tilde),label="rx signal")
        plt.plot(np.abs(rlms_estimated_signal),label="eq signal")
        plt.legend()
        plt.show()

    return np.array(rlms_estimated_signal)

