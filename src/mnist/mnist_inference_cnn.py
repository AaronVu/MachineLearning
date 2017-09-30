#-*- coding: utf-8 -*-
import tensorflow as tf

INPUT_NODE = 784
OUTPUT_NODE = 10

IMAGE_SIZE = 28
NUM_CHANNELS = 1
NUM_LABELS = 10

#第一层卷积层的尺寸和深度
CONV1_DEEP = 32
CONV1_SIZE = 5

#第二层
CONV2_DEEP = 64
CONV2_SIZE = 5

#全链接曾的结点个数
FC_SIZE = 512

def inference(input_tensor, train, regularizer):
    '''
    定义卷积神经网络的前向传播过程，
    :param input_tensor:
    :param train: 区分训练过程和测试过程
    :param regularizer:
    '''
    #声明第一层变量及实现前向传播过程
    with tf.variable_scope('layer1-conv1'):
        conv1_weights = tf.get_variable("weight", [CONV1_SIZE, CONV1_SIZE, NUM_CHANNELS,CONV1_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv1_biases = tf.get_variable("bias", [CONV1_DEEP],initializer=tf.constant_initializer(0.0))
        #边长1、深度32、步长1的过滤器，全0填充，输出为 28 x 28 x 32
        conv1 = tf.nn.conv2d(input_tensor, conv1_weights, strides=[1,1,1,1],padding='SAME')
        relu1 = tf.nn.relu(tf.nn.bias_add(conv1, conv1_biases))

    #第二层池化层的前向传播过程（最大化）
    with tf.name_scope("layer2-pool1"):
        #边长2、步长2，输出为 14 x 14 x 32
        pool1 = tf.nn.max_pool(relu1, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

    #第三层卷积层
    with tf.name_scope("layer3-conv2"):
        conv2_weights = tf.get_variable('weight', [CONV2_SIZE, CONV2_SIZE, CONV1_DEEP, CONV2_DEEP],
                                        initializer=tf.truncated_normal_initializer(stddev=0.1))
        conv2_biases = tf.get_variable('bias', [CONV2_DEEP], initializer=tf.constant_initializer(0.0))
        #边长5、深度64、步长1、全0填充的过滤器 输出为14 x 14 x 64
        conv2 = tf.nn.conv2d(pool1, conv2_weights, strides=[1,1,1,1],padding='SAME')
        relu2 = tf.nn.relu(tf.nn.bias_add(conv2, conv2_biases))

    #第四层池化层
    with tf.name_scope("layer4-pool2"):
        #输出为7 x 7 x 64
        pool2 = tf.nn.max_pool(relu2, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')

    #将第四池化层转的输出为第五层全连接层的输入格式
    #第五层全连接层的输入格式为向量，将7 x 7 x 64的矩阵拉直成一个向量,pool_shape[0]代表一个batch中的数据的个数
    pool_shape = pool2.get_shape().as_list()
    nodes = pool_shape[1]*pool_shape[2]*pool_shape[3]
    #转为向量
    reshaped = tf.reshape(pool2, [pool_shape[0], nodes])

    #第五层全连接层前向传播过程
    with tf.variable_scope('layer5-fc1'):
        fc1_weights = tf.get_variable("weight", [nodes, FC_SIZE],initializer=tf.truncated_normal_initializer(stddev=0.1))
        #只有全连接层的权重需要加入正则化
        if regularizer:
            tf.add_to_collection("losses", regularizer(fc1_weights))
        fc1_biases = tf.get_variable("bias", [FC_SIZE], initializer=tf.constant_initializer(0.1))
        fc1 = tf.nn.relu(tf.matmul(reshaped, fc1_weights)+fc1_biases)
        if train:
            #进一步提升模型可靠性并防止过拟合（该方法只在训练时使用）
            fc1 = tf.nn.dropout(fc1, 0.5)

    #第六层全连接
    with tf.variable_scope("layer6-fc2"):
        fc2_weights = tf.get_variable("weight", [FC_SIZE, NUM_LABELS],
                                      initializer=tf.truncated_normal_initializer(stddev=0.1))
        if regularizer:
            tf.add_to_collection("losses", regularizer(fc2_weights))
        fc2_biases = tf.get_variable("bias", [NUM_LABELS],initializer=tf.constant_initializer(0.1))
        logit = tf.matmul(fc1, fc2_weights)+fc2_biases

    return logit






