import tensorflow as tf
def compute_BER(b,b_hat):
    b = tf.cast(b,dtype=tf.int32)
    b_hat = tf.cast(b_hat,dtype=tf.int32)
    ber = tf.not_equal(b, b_hat)
    ber = tf.cast(ber, tf.float64) # tf.float64 to suport large batch-sizes
    return tf.reduce_mean(ber)

    
    
