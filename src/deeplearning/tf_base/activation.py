import tensorflow as tf
from numpy.random import RandomState

class Activation:
    '''
        非线性激活函数(提供网络的非线性建模能力)和偏置项
        定义变量的更新
        tf.VARIABLES ——> tf.GLOBAL_VARIABLES
        tf.all_variables ——> tf.global_variables
        tf.initialize_all_variables ——> tf.global_variables_initializer
        tf.initialize_local_variables ——> tf.local_variables_initializer
        tf.initialize_variables ——> tf.variables_initializer
        函数的更新
        tf.audio_summary ——> tf.summary.audio
        tf.contrib.deprecated.histogram_summary ——>tf.summary.histogram
        tf.contrib.deprecated.scalar_summary ——>tf.summary.scalar
        tf.histogram_summary ——> tf.summary.histogram
        tf.image_summary ——>tf.summary.image
        tf.merge_all_summaries ——> tf.summary.merge_all
        tf.merge_summary ——> tf.summary.merge
        tf.scalar_summary ——> tf.summary.scalar
        tf.train.SummaryWriter ——> tf.summary.FileWriter
        数值计算函数的更新
        tf.sub ——> tf.subtract
        tf.mul ——> tf.multiply
        tf.div ——> tf.divide
        tf.mod ——> tf.truncatemod
        tf.inv ——> tf.reciprocal
        tf.list_diff ——> tf.setdiff1d
        tf.listdiff ——> tf.setdiff1d
        tf.neg ——> tf.negative
        tf.select ——> tf.where
    '''

    def test_1(self):
        '''
        常用损失函数：
            1、交叉熵
            2、均方误差
        自定义损失函数：
            loss = tf.reduce_sum(tf.where(tf.greater(v1,v2), v1, v2))
        :return:
        '''
        v1 = tf.constant([1.0, 2.0, 3.0, 4.0])
        v2 = tf.constant([4.0, 3.0, 2.0, 1.0])

        sess = tf.InteractiveSession()
        print(tf.greater(v1, v2).eval())

        print(tf.where(tf.greater(v1,v2), v1, v2).eval())
        sess.close()

    def test_2(self):
        v = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        #将一个张量中的数值限制在指定范围之内
        tf.clip_by_value(v, 2.5, 4.5)
        tf.log(v)
        #定义损失函数：loss = tf.reduce_mean(指定损失函数)
        tf.square()
        print(tf.log(v))

    def lossFunc(self):
        batch_size = 8
        #两个输入节点
        x = tf.placeholder(tf.float32, shape=(None, 2), name="x-input")
        #回归问题一般只有一个输出节点
        y_ = tf.placeholder(tf.float32, shape=(None, 1), name="y-input")

        #定义一个单层的神经网络前向传播的过程，这里就是简单加权和
        w1 = tf.Variable(tf.random_normal([2, 1], stddev=1,seed=1))
        y = tf.matmul(x, w1)

        #定义预测多了和少了的成本
        loss_less = 10
        loss_more = 1
        loss = tf.reduce_sum(tf.where(tf.greater(y, y_), (y-y_)*loss_more, (y_-y)*loss_less))

        train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

        #通过随机数生成一个模拟数据集
        rdm = RandomState(1)
        dataset_size = 128
        X = rdm.rand(dataset_size, 2)
        #设置回归的正确值为两个输入的和加上一个随机量。之所以要加上一个随机量是为了加入
        #不可预测的噪音，否则不同损失函数的意义就不大了，因为不同损失函数去会在能完全预测正确的时候最低
        #一般来说噪音为一个均值为0的小量，所以这里的噪音设置为-0.05~0.05的随机数
        Y = [[x1 + x2 +rdm.rand()/10.0-0.05] for (x1,x2) in X]

        #训练神经网络
        with tf.Session() as sess:
            init_op = tf.initialize_all_variables()
            sess.run(init_op)
            STEPS = 5000
            for i in range(STEPS):
                start = (i*batch_size)%dataset_size
                end = min(start+batch_size, dataset_size)
                sess.run(train_step, feed_dict={x:X[start:end], y_:Y[start:end]})
                print(sess.run(w1))


act = Activation()
act.lossFunc()