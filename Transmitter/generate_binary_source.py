import numpy as np
import tensorflow as tf
#Transmitter
#Generate Frames
def generate_frame(batch_size,num_tx,num_tx_antennas,information_size):
    frame = []
    bits = []
    for i in range(0,batch_size):
        for j in range(0,num_tx):
            bits.append(np.random.randint(low=0,high=2,size = information_size))
        frame.append(bits)
        bits = []
    frame = tf.convert_to_tensor(frame)
    frame = tf.expand_dims(frame, axis = 2)
    binary_frame = tf.tile(frame,[1,1,num_tx_antennas,1])
    return binary_frame
   
    