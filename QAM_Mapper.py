import numpy as np

class QAM_Mapper:
    def generate_qam(num_bits_per_symbol):
        # Calculate number of bits per symbol
        num_bits = num_bits_per_symbol
        mod_order = np.power(2,num_bits)
        # Generate all possible combinations of bits
        all_bits = np.array(list(np.binary_repr(i, width=num_bits) for i in range(mod_order)))
        
        # Map bits to QAM symbols
        qam_values = []
        for i in range(mod_order):
            real = int(all_bits[i][:num_bits//2], 2)
            imag = int(all_bits[i][num_bits//2:], 2)
            qam_values.append((2 * real - (num_bits - 1)) + 1j * (2 * imag - (num_bits - 1)))
            
        normalised = np.sqrt(np.mean(np.square(np.abs(qam_values))))
        qam_bits = [[int(bit) for bit in bits_str] for bits_str in all_bits]
        qam_values = qam_values/normalised
        return qam_bits,qam_values
         