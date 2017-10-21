# -*-coding:utf-8-*-
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os


def add_layer(inputs, in_size, out_size, activation_function=None):
    '''
    add layer
    '''
    with tf.name_scope('layer'):
        with tf.name_scope('weights'):
            Weights = tf.Variable(tf.random_normal([in_size, out_size]), name='W')

        with tf.name_scope('biases'):
            biases = tf.Variable(tf.zeros([1, out_size])+.1, name='b')

        with tf.name_scope('Wx_plus_b'):
            Wx_plus_b = tf.matmul(inputs, Weights) + biases

        if activation_function:
            outputs = activation_function(Wx_plus_b)
        else:
            outputs = Wx_plus_b

        return outputs


def start():
    x_data = np.linspace(-1, 1, 300)[:, np.newaxis]
    noise = np.random.normal(0, 0.05, x_data.shape)
    y_data = np.square(x_data) - 0.5 + noise

    ax = data_vis(x_data, y_data)

    with tf.name_scope('inputs'):
        xs = tf.placeholder(tf.float32, [None, 1], name='x_input')
        ys = tf.placeholder(tf.float32, [None, 1], name='y_input')

    # hidden layer
    layer1 = add_layer(xs, 1, 10, activation_function=tf.nn.relu)
    # output layer
    predition = add_layer(layer1, 10, 1, activation_function=None)

    # loss function
    with tf.name_scope('loss'):
        loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys-predition), reduction_indices=[1]))

    # gradient descent
    with tf.name_scope('train'):
        train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)
        
    init = tf.initialize_all_variables()

    with tf.Session() as sess:
        writer = tf.train.write_graph(graph_or_graph_def=sess.graph,  name='plot', logdir='logs/')
        sess.run(init)
        for i in range(1000):
            sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
            if i % 5 == 0:
                try:
                    ax.lines.remove(lines[0])
                except Exception:
                    pass
                prediction_value = sess.run(predition, feed_dict={xs: x_data, ys: y_data})
                lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
                plt.pause(0.1)
        os.system('pause')


def data_vis(x_data, y_data):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.scatter(x_data, y_data)
    plt.ion()  # unblocked
    plt.show()
    return ax


start()



