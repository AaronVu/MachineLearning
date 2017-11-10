#coding:utf-8
import os

import numpy as np
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

import deeplearning.mnist.mnist_inference_cnn as infrence

BATCH_SIZE = 100
LEARNING_RATE_BASE = 0.8
LEARNING_RATE_DECAY = 0.99
REGULARAZTION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99

MODEL_SAVE_PATH = "../../resources/"
MODEL_NAME = "model.ckpt"

def train(mnist):
    #定义输入输出
    x = tf.placeholder(tf.float32, [BATCH_SIZE, infrence.IMAGE_SIZE, infrence.IMAGE_SIZE,infrence.NUM_CHANNELS], name="x-input")

    y_ = tf.placeholder(tf.float32, [None, infrence.OUTPUT_NODE], name="y-input")

    # 定义正则化损失
    regularizer = tf.contrib.layers.l2_regularizer(REGULARAZTION_RATE)
    y = infrence.inference(x, True, regularizer)
    #指定滑动平均类，并在所以神经网络参数的变量上使用平滑平均（除global_step）
    global_step = tf.Variable(0, trainable=False)
    variable_averages = tf.train.ExponentialMovingAverage(MOVING_AVERAGE_DECAY, global_step)
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    #定义交叉熵损失
    cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=y, labels=tf.argmax(y_, 1))
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    #总损失 = 正则化损失 + 交叉熵损失
    loss = cross_entropy_mean + tf.add_n(tf.get_collection("losses"))
    #设定指数衰减的学习率
    learning_rate = tf.train.exponential_decay(LEARNING_RATE_BASE, global_step, mnist.train.num_examples/BATCH_SIZE, LEARNING_RATE_DECAY)
    #优化损失函数
    train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
    #通过反向传播来更新神经网络中的参数和滑动平均值
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name="train")
    #初始化持久化类
    saver = tf.train.Saver()
    #开始训练过程
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        for i in range(TRAINING_STEPS):
            xs, ys = mnist.train.next_batch(BATCH_SIZE)
            reshaped_xs = np.reshape(xs, (BATCH_SIZE, infrence.IMAGE_SIZE,infrence.IMAGE_SIZE,infrence.NUM_CHANNELS))
            _, loss_value, step = sess.run([train_op, loss, global_step], feed_dict={x:reshaped_xs, y_:ys})
            if i % 1000 == 0:
                print("After %d training step(s), loss on training batch is %g"%(step, loss_value))
                if i /1000 == 29:
                    saver.save(sess, os.path.join(MODEL_SAVE_PATH, MODEL_NAME), global_step=global_step)

def main(argv=None):
    mnist = input_data.read_data_sets("../../resources", one_hot=True)
    train(mnist)

if __name__ == "__main__":
    tf.app.run()


