#coding:utf-8

import tensorflow as tf
from numpy.random import RandomState

class BCP:

    '''
        训练神经网络的过程：
            1、定义神经网络的结果和前向传播的输出结果
            2、定义损失函数以及选择反向传播的算法
            3、生成会话，并且在训练数据上反复运行反向传播优化算法
        注：无论神经网络的结构如何变化，这3个步骤是不变的
    '''

    def __init__(self, batch_size=8):
        # 定义训练数据batch的大小
        self.batch_size = batch_size
        #定义神经网络的参数
        self.w1 = tf.Variable(tf.random_normal([2,3], stddev=1, seed=1))
        self.w2 = tf.Variable(tf.random_normal([3, 1], stddev=1, seed=1))
        #在shape的一个维度上使用None可以方便使用不同的batch大小，在实际训练时需要把数据分成较小的batch，
        #不然将大量的数据放入一个batch可能会导致内存溢出
        self.x = tf.placeholder(tf.float32, shape=(None, 2), name='x-input')
        self.y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y-input')
        #定义前向传播的过程
        self.a = tf.matmul(self.x, self.w1)
        self.y = tf.matmul(self.a, self.w2)
        #定义损失函数和反向传播算法
        self.cross_entropy = -tf.reduce_mean(self.y_ * tf.log(tf.clip_by_value(self.y, 1e-10, 1.0)))
        self.train_step = tf.train.AdamOptimizer(0.001).minimize(self.cross_entropy)
        self.sess = tf.Session()
        # 初始化所有变量
        initVar = tf.initialize_all_variables()
        self.sess.run(initVar)

    def create_model_data(self):
        '''
        通过随机数生成一个模拟数据集
        定义规则来给出样本的标签。 x1 + x2 > 1 的样例都被认为是正样本
            0 代表负样本 1 代表正样本
        :return:
        '''
        self.rdm = RandomState(1)
        self.dataset_size= 128
        X = self.rdm.rand(self.dataset_size, 2)
        Y = [[int(x1+x2 < 1)] for (x1, x2) in X]
        return X,Y


    def run(self):
        print("训练之前结果：")
        print(self.sess.run(self.w1))
        print(self.sess.run(self.w2))

    def runTest(self, STEPS=5000):
        X,Y = self.create_model_data()
        for i in range(STEPS):
            #每次选取batch_size个样本进行训练
            start = (i * self.batch_size) % self.dataset_size
            end = min(start+self.batch_size, self.dataset_size)
            self.sess.run(self.train_step, feed_dict={self.x: X[start:end], self.y_: Y[start:end]})
            if i % 1000 == 0:
                total_cross_entropy = self.sess.run(self.cross_entropy, feed_dict={self.x: X, self.y_: Y})
                #交叉熵越小，说明预测的结果和真实的结果差距越小
                print("After %d training step(s), cross entropy on all data is %g"%(i, total_cross_entropy))
        print("训练之后结果：")
        print(self.sess.run(self.w1))
        print(self.sess.run(self.w2))

if __name__ == '__main__':
    bcp = BCP()
    bcp.run()
   #bcp.runTest()