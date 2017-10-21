# coding:utf-8
import tensorflow as tf


class Forward:

    def one(self):
        #保存和更新神经网络中的参数
        w1= tf.Variable(tf.random_normal([2,3], stddev=2))
        w2 = tf.Variable(w1.initialized_value()* 2.0)

    def two(self):
        '''
        每一个变量在使用之前，该变量的初始化过程须被明确调用
        [2,3]代表 产生一个2*3矩阵
        stddev 标准差
        seed随机种子——》保证每次运行得到的结果是一样的
        :return:
        '''
        w1 = tf.Variable(tf.random_normal([2,3], stddev=1,seed=1))
        w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))
        #输入值 定义为一个常量 1*2矩阵
        x = tf.constant([[0.7, 0.9]])
        #前向传播
        a = tf.matmul(x, w1)
        y = tf.matmul(a, w2)
        sess = tf.Session()
        #初始化变量
        #sess.run(w1.initializer)
        #sess.run(w2.initializer)
        init_var = tf.initialize_all_variables()
        sess.run(init_var)
        #输出结果
        print(sess.run(y))
        sess.close()

    def three(self):
        '''
        避免生成大量常量来提供输入数据：placeholder
        :return:
        '''
        w1 = tf.Variable(tf.random_normal([2, 3], stddev=1, seed=1))
        w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))
        #定义placeholder作为存放输入数据的地方，这里维度也不一定要定义
        #但如果维度是确定的，那么给出维度可以降低出错的概率
        x = tf.placeholder(tf.float32, shape=(3,2), name="input") #在run时传入输入数据
        a = tf.matmul(x, w1)
        y = tf.matmul(a, w2)
        sess = tf.Session()
        init_var = tf.initialize_all_variables()
        sess.run(init_var)
        print(sess.run(y, feed_dict={x: [[0.7,0.9],[0.1,0.4],[0.5,0.8]]})) #feed_dict输入数据
       


fm = Forward()
fm.three()