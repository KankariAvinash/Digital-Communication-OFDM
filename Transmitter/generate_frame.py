import numpy as np
import matplotlib.pyplot as plt

def generate_shuffled_arrays(n):
    original_array = np.pad(np.ones(32), (0, 32)).astype(int)
    arrays = []
    for _ in range(n):
        shuffled_array = np.random.permutation(original_array)
        arrays.append(shuffled_array)
    return arrays

def generate_frame(frame_size, switch_graph):
    '''
        Here each frame has 64bits
        that means number of bits in total = 64*frame_size
    '''
    frame = []
    shuffled_arrays = generate_shuffled_arrays(frame_size)
    for arr in shuffled_arrays:
        frame.append(arr)
    prob = []
    for i in range(frame_size):
        prob.append(sum(frame[i])/len(frame[i]))
    if switch_graph:
        plt.figure()
        plt.stem(frame[i])
        plt.text(frame_size, 1,prob[i])
        plt.title('Sample Signal with equal probability of 1s and 0s')
        plt.xlabel('Single Frame')
        plt.show()  
    return np.array(np.ravel(frame))