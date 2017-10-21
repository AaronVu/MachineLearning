# -*-coding:utf-8-*-
import tensorflow as tf
import numpy as np

def example_1():
    # creat data
    x_data = np.random.rand(100).astype(np.float32)
    y_data = x_data*.1 + .3

    Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
    biases = tf.Variable(tf.zeros([1]))

    y = Weights*x_data+biases

    loss = tf.reduce_mean(tf.square(y-y_data))

    optimizer = tf.train.GradientDescentOptimizer(0.5)
    train = optimizer.minimize(loss)

    init = tf.initialize_all_variables()

    with tf.Session() as sess:
        sess.run(init)
        for step in range(201):
            sess.run(train)
            if step % 20 == 0:
                print(step, sess.run(Weights), sess.run(biases))


def example_2():
    matrix1 = tf.constant([[3, 3]])
    matrix2 = tf.constant(([[2], [2]]))
    product = tf.matmul(matrix1, matrix2)  # see np.dot(m1, m2)
    with tf.Session() as sess:
        result = sess.run(product)
        print(result)


def example_3():
    state = tf.Variable(0, name='counter')
    one = tf.constant(1)
    val = tf.add(state, one)
    update = tf.assign(state, val)
    init = tf.initialize_all_variables()
    with tf.Session() as sess:
        sess.run(init)
        for i in range(3):
            sess.run(update)
            print(sess.run(state))


def example_4():
    '''
    placehodler
    '''
    input1 = tf.placeholder(tf.float32)
    input2 = tf.placeholder(tf.float32)

    output = tf.add(input1, input2)

    with tf.Session() as sess:
        print(sess.run(output, feed_dict={input1: [7.], input2: [2.]}))




