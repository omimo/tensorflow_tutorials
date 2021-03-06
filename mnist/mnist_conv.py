# Created on Tue Sep 20 18:50:00 2016
# @author: Omid Alemi

import tensorflow as tf

# Define utility functions for initializing the variables
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

# Define utility functions for our convolution and pooling operations
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 1, 1, 1], strides=[1, 2, 2, 1], padding='SAME')

# Download/load the MNIST data
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# Defining the symbolic variables

# use tf.placeholder for input
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])

# Define the 1st layer
W_conv1 = weight_variable([5, 5, 1, 32]) #5x5 patches, 1 input channel, 32 output channels
b_conv1 = bias_variable([32])

# Apply the 1st layer
## reshape the input x to a 4d tensor
x_image = tf.reshape(x, [-1, 28, 28, 1]) # HxW = 28x28, one output color channel
## convolve x_image with the weight tensor, apply ReLU, and max pool
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


# Define the 2nd layer
W_conv2 = weight_variable([5, 5, 32, 64]) #5x5 patches, 32 input, 64 output features
b_conv2 =  bias_variable([64])

# Apply the 2nd layer
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


# Define the dense layer
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)


# Define the dropout layer
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


# Define the readout layer
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# Define the trainer
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# Initialize the tf variables
init = tf.initialize_all_variables()

# Lunch the session
sess = tf.Session()
sess.run(init)

# Do the train
for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i%100 == 0:
        correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        train_accuracy = sess.run(accuracy,feed_dict={
            x:batch[0], y_:batch[1], keep_prob: 1.0
        })
        print("step %d, train_accuracy = %g" % (i, train_accuracy))
    sess.run(train_step,feed_dict={x:batch[0], y_:batch[1], keep_prob:0.5})

test_accuracy = sess.run(accuracy,feed_dict={
            x:mnist.test.images, y_:mnist.test.labels, keep_prob: 1.0
        })

print "test accuracy = %g" % (test_accuracy)