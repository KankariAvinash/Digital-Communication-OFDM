import numpy as np

def encode_hamming(b, parity_check_matrix, n_zero_padded_bits, switch_off):
    if switch_off:
        print("======= Channel Coding OFF ==========")
        final = (np.pad(b,(0,n_zero_padded_bits)))
        return np.array(final)
    else:
        print("======= Channel Coding ON ==========")
        len_information = (len(b))//4
        codeword = []
        codeword_matrix = np.zeros((len_information,7))

        #taking parity elements from parity check matrix
        parity_matrix = []
        for i in range(0,3):          # A for loop for row entries
            a =[]
            for j in range(0,4):      # A for loop for column entries
                a = parity_check_matrix[i][j]
                parity_matrix.append(a)
        
        parity_matrix = np.transpose(-(np.reshape(parity_matrix,(3,4))))

        #forming Generator matrix using parity matrix
        generator_matrix = (np.concatenate((np.identity(4),parity_matrix),1)).astype(int)
        
        #checking the condition: matrix multiplication is Generator matrix and Parity check matrix is zero
        condition = np.matmul(generator_matrix,np.transpose(parity_check_matrix)).astype(int)
        #it is true, form codeword using information and Generator matrix
        if(np.all(condition==0)):
            b_2array = np.reshape(b,(len_information,4))
            codeword_matrix = ((np.matmul(b_2array,generator_matrix).astype(int))%2)
            condition2 = ((np.matmul(codeword_matrix,np.transpose(parity_check_matrix)).astype(int))%2)
            # checking the condition 2: if matrix multiplication is codeword and Parity check matrix is zero, then resultant code word is true
            if(np.all(condition2==0)):
                # coverting matrix to array
                codeword = np.squeeze(codeword_matrix).reshape(-1)
                codeword = np.array(codeword)
            
                return np.array(np.pad(codeword,(0,n_zero_padded_bits)))

            else:
                print('resultant Codeword matrix is false')
        else:
            print('Resultant Generator matrix is wrong')