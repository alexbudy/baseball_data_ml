import tensorflow as tf
from numpy import genfromtxt
import numpy as np

# get the data into numpy arrays
train_x = genfromtxt('data_x.csv', delimiter=',', dtype='int')
train_y = genfromtxt('data_y.csv', dtype='int')
test_x = genfromtxt('test_x.csv', delimiter=',', dtype='int')
test_y = genfromtxt('test_y.csv', dtype='int')


learning_rate = 0.001
training_epochs = 40
batch_size = 100
display_step = 1

#Network Parameters
n_hidden_1 = 28
n_hidden_2 = 28
n_input = 28
n_classes = 16

# tf Graph input
x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])

# create onehot test data
test_y_onehot = np.zeros((test_y.shape[0], n_classes), dtype="int")
test_y_onehot[np.arange(test_y.shape[0]), test_y] = 1

def multilayer_perceptron(x, weights, biases):
    # hidden with RELU act
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.relu(layer_1)
    # hidden with RELU act
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    layer_2 = tf.nn.relu(layer_2)
    # output layer with lin act
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer

weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_input, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

pred = multilayer_perceptron(x, weights, biases)

# define loss and optimizer
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Init variables
init = tf.initialize_all_variables()

def getBatchedData(batchId, batchSize, data_x, data_y):
    batch_x = data_x[batchId*batchSize : batchId*batchSize + batchSize]
    batch_y = data_y[batchId*batchSize : batchId*batchSize + batchSize]
    # batch_y needs to be one-hot
    batch_y_onehot = np.zeros((batchSize, n_classes), dtype="int")
    batch_y_onehot[np.arange(batchSize), batch_y] = 1

    return batch_x, batch_y_onehot

with tf.Session() as sess:
    sess.run(init)

    # Training cycle
    for epoch in range(training_epochs):
        avg_cost = 0
        total_batch = int(train_x.shape[0]/batch_size)
        # Loop over all batches
        for i in range(total_batch):
            batch_x, batch_y = getBatchedData(i, batch_size, train_x, train_y)
            # Run optimization op (backdrop_ and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
            # Compute avg loss
            avg_cost += c / total_batch
        # display logs per epoch
        if epoch % display_step == 0:
            print "Epoch:", '%04d' % (epoch+1), "cost=", "{:.9f}".format(avg_cost)
    print("Optimization finished")
    
    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    print(pred)
    # Calculate accuracy
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print "Accuracy:", accuracy.eval({x: test_x, y: test_y_onehot})
