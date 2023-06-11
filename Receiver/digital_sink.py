import numpy as np
import matplotlib.pyplot as plt
import math

def digital_sink(b, b_hat,snr_db,switch_graph):
    BER = np.abs(np.mean(b - b_hat))
    print('BER :',BER)
    if switch_graph:
        SNRs_db = snr_db
        SNR = np.arange(-40,30,1)
        QAM4_BER_th = []
        QAM16_BER_th = []
        QAM64_BER_th = []
    
        for i in SNR:
            i = 10**(i/10)
            QAM4_BER_th.append((1 / (2 * math.log2(4))) * math.erfc(math.sqrt(3 * math.log2(4) * (i) / (4 - 1))))  # Theoritcal 4-QAM
            QAM16_BER_th.append((1 / (2 * math.log2(16))) * math.erfc(math.sqrt(3 * math.log2(16) * (i) / (16 - 1))))  # Theoritcal 16-QAM
            QAM64_BER_th.append((1 / (2 * math.log2(64))) * math.erfc(math.sqrt(3 * math.log2(64) * (i) / (64 - 1))))  # Theoritcal 64-QAM
        QAM4_BER_th = np.array(QAM4_BER_th)
        QAM16_BER_th = np.array(QAM16_BER_th)
        QAM64_BER_th = np.array(QAM64_BER_th)
        plt.figure()
        plt.subplot(2,1,1)
        plt.stem(b)
        plt.title("Source Information")
        plt.subplot(2,1,2)
        plt.stem(b_hat)
        plt.title("Sink Received")

        plt.figure()
        plt.semilogy(SNRs_db,BER,'b*-',SNR,QAM4_BER_th,'g*-',SNR,QAM16_BER_th,'r*-',SNR,QAM64_BER_th,'k*-')  
        plt.legend(["Practical","QAM4_BER_th","QAM16_BER_th","QAM64_BER_th"],loc="lower right")
        plt.title('BER vs SNR')
        plt.xlabel('SNR(db)')
        plt.ylabel('BER')
        plt.ylim((1e-10,1))
        plt.grid(True)
        plt.show()
    return np.array(BER)