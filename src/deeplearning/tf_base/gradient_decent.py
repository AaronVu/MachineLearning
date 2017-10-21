import tensorflow as tf

class GradientDecent:

    '''
    神经网络优化算法：
        反向传播算法
        梯度下降
    '''

    def learningRate(self):
        global_step = tf.Variable(0)
        #通过exponential_decay函数生成学习率
        learning_rate = tf.train.exponential_decay(0.1, global_step, 100, 0.96, staircase=True)

        #使用指数衰减的学习率。在minimize函数中传入global_step将自动更新
        #global_step参数，从而使得学习率也得到相应更新
        learning_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(None, global_step=global_step)


    def get_weight(self, shape, lambd):
        '''
        解决过拟合问题：
            当一个模型过为复杂之后，他可以很好的记忆每一个训练数据中随机噪音的部分，
            而忘记去学习训练数据中通用的趋势。
        获取一层神经网络边上的权重，并将这个权重的L2正则化损失加入名称为losses的集合中
        :param shape:
        :return:
        '''
        #生成一个变量
        var = tf.Variable(tf.random_normal(shape), dtype=tf.float32)
        #add_to_collection函数将这个新生成变量的L2正则化损失项加入集合
        #这个函数的第一个参数losses是集合的名字，第二个参数是要加入这个集合的内容。
        tf.add_to_collection('losses', tf.contrib.layers.l2_regularizer(lambd)(var))
        return var

    def regLoss(self):
        '''
        5层神经网络带L2正则化的损失函数
        :return:
        '''
        x = tf.placeholder(tf.float32, shape=(None, 2))
        y_ = tf.placeholder(tf.float32, shape=(None, 1))
        batch_size = 8
        #定义每一层网络中节点的个数
        layer_dimension = [2, 10, 10, 10, 1]
        #神经网络的层数
        n_layers = len(layer_dimension)

        #这个变量维护前向传播是最深层的节点，开始的时候就是输入层
        cur_layer = x
        in_dimension = layer_dimension[0]

        #生成5层全链接的神经网络结构
        for i in range(1, n_layers):
            out_dimension = layer_dimension[i]
            #生成当前层中权重的变量
            weight = self.get_weight([in_dimension,out_dimension], 0.001)
            bias = tf.Variable(tf.constant(0.1, shape=[out_dimension]))

            #使用ReLU激活函数
            cur_layer = tf.nn.relu(tf.matmul(cur_layer, weight)+bias)
            #进入下一层之前将下一层的节点个数更新为当前层节点个数
            in_dimension = layer_dimension[i]
        #定义损失函数
        mse_loss = tf.reduce_mean(tf.square(y_ - cur_layer))

        #将均方误差损失函数加入损失集合
        tf.add_to_collection("losses", mse_loss)
        #get_collection返回一个列表，这个列表是所有这个集合中的元素，
        #这些元素就是损失函数的不同部分，将它们加起来就可以得到最终的损失函数
        loss = tf.add_n(tf.get_collection("losses"))
        print(loss)

gra = GradientDecent()

gra.regLoss()