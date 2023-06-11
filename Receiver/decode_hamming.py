## Here we are using 7,4 hamming code.
##Gaussian Normal Form: 
## Here we are using systematic code word = [u p] = [U0 U1 U2 U3 P0 P1 P2]
#### Length of information bits(k) = 4
#### Length of code bits(n) = 7
#### number of parity bits are 3 which are P0,P1,P2
##Steps to Proceed:
#### 1 : Generator matrix G = [I 4x4| P 4x3]
####   : Parity check matrix H = [-(Transpose of p) 4x3 | I 3x3]
#### 2 : syndrome => matrix multiplication of information word with Parity check matrix
#### 3 : if syndrome matrix is all zeros then information received as no errors
#### 4 : if not correction(FEC) should be done

## Error correction method
# Coset leaders represented by 7 vectors with hamming distance = 1
## 001 ->  0 0 0 0 0 0 1
## 010 ->  0 0 0 0 0 1 0
## 011 ->  1 0 0 0 0 0 0
## 100 ->  0 0 0 0 1 0 0
## 101 ->  0 1 0 0 0 0 0
## 110 ->  0 0 1 0 0 0 0
## 111 ->  0 0 0 1 0 0 0

## After error correction . Calculating received signal
### [[0,0,0,0,0,0,0],[0,1,0,0,0,0,0],[0,0,0,1,0,0,0],[0,1,0,0,0,0,1]] * codeword => received signal
import numpy as np
import matplotlib.pyplot as plt

def ErrorCorrection(syndrome_matrix):
    if(syndrome_matrix[2]==0 and syndrome_matrix[1]==0 and syndrome_matrix[0]==1):
        correction = [0,0,0,0,0,0,1]
    elif(syndrome_matrix[2]==0 and syndrome_matrix[1]==1 and syndrome_matrix[0]==0):
        correction = [0,0,0,0,0,1,0]
    elif(syndrome_matrix[2]==0 and syndrome_matrix[1]==1 and syndrome_matrix[0]==1):
        correction = [1,0,0,0,0,0,0]
    elif(syndrome_matrix[2]==1 and syndrome_matrix[1]==0 and syndrome_matrix[0]==0):
        correction = [0,0,0,0,1,0,0]
    elif(syndrome_matrix[2]==1 and syndrome_matrix[1]==0 and syndrome_matrix[0]==1):
        correction = [0,1,0,0,0,0,0]
    elif(syndrome_matrix[2]==1 and syndrome_matrix[1]==1 and syndrome_matrix[0]==0):
        correction = [0,0,1,0,0,0,0]
    elif(syndrome_matrix[2]==1 and syndrome_matrix[1]==1 and syndrome_matrix[0]==1):
        correction = [0,0,0,1,0,0,0]
    return np.array(correction,dtype=int)
    
def decode_hamming(c_hat, parity_check_matrix, n_zero_padded_bits,switch_off_cc, switch_graph):
    if switch_off_cc:
        # return the same information bits
        print("======= Channel Coding OFF ==========")
        source_decoder = c_hat[:len(c_hat) - n_zero_padded_bits]
        source_decoder = np.array(source_decoder,dtype=int)

        if switch_graph:
            plt.figure()
            plt.plot(source_decoder)
            plt.xlabel("bits")
            plt.title('First Received frame')
            plt.show()
        return source_decoder
    else:
        print("======= Channel Coding ON ==========")
        source_decoder = c_hat[:len(c_hat) - n_zero_padded_bits]
        source_decoder = np.array(source_decoder,dtype=int)

        
        #initialization of variables
        len_information = (len(source_decoder))
        c_hat_mat = np.reshape(source_decoder,(len_information//7,7))
        syndrome_matrix = ((np.matmul(c_hat_mat,np.transpose(parity_check_matrix)).astype(int))%2)
        syndrome = np.squeeze(syndrome_matrix).reshape(-1)
        
        parity_matrix = [[0,0,0,0,1,1,0],[0,0,0,0,0,0,1],[0,0,0,0,1,0,1],[0,0,0,0,1,1,1]]

        if(np.all(syndrome==0)):
            print('=== No Error: Received signal has no errors ===')
            final_message_nocorrection = (np.matmul(parity_matrix,np.transpose(c_hat_mat)).astype(int))%2
            final_message =  np.squeeze(final_message_nocorrection).reshape(-1)
        else:
            for i in range(0,len(syndrome_matrix)):
                if(~np.all(syndrome_matrix[i]==0)):
                    #error correction is need
                    order = ErrorCorrection(syndrome_matrix[i])
                    c_hat_mat[i] = (c_hat_mat[i] - order)%2
                else:
                    c_hat_mat[i] = c_hat_mat[i]
            print('=== After Correcting Errors ===')
            final_message_afterCorrection = ((np.matmul(parity_matrix,np.transpose(c_hat_mat)).astype(int))%2)
            final_message = np.squeeze(final_message_afterCorrection).reshape(-1)
        if(switch_graph):
            plt.figure()
            plt.subplot(2,1,1)
            plt.stem(c_hat)
            plt.title('Code word')
            plt.subplot(2,1,2)
            plt.stem(final_message)
            plt.title('Decoded Information word')
            plt.show()
            
        return np.array(final_message)
       
