import tensorflow as tf

class MovingAverage:

    '''
    滑动平均模型
        衰减率：控制模型更新的速度
    '''

    def __init__(self):
        #定义一个变量用于计算滑动平均，这个变量初始值为0。
        #所有需要计算滑动平均的变量必须是实数型
        self.v1 = tf.Variable(0, dtype=tf.float32)
        #模拟神经网络中迭代的轮数，可以用于动态控制衰减率
        self.step = tf.Variable(0, trainable=False)
        #定义滑动平均的类，初始化时给定衰减率和控制衰减率的变量step
        self.ema = tf.train.ExponentialMovingAverage(0.99, self.step)
        #定义一个更新滑动平均的操作，这里要给定一个列表，每次执行这个操作时
        #这个列表中的变量都会被更新
        self.maintain_averages_op = self.ema.apply([self.v1])

    def  run(self):
        with tf.Session() as sess:
            #初始化所有变量
            init_op = tf.initialize_all_variables()
            sess.run(init_op)

            #通过emaaverage(v1)获取滑动平均之后变量的取值。在初始化之后变量v1的值和v1的滑动平均都为0
            print(sess.run([self.v1, self.ema.average(self.v1)]))

            #更新变量v1的值到5
            sess.run(tf.assign(self.v1, 5))
            #更新v1的滑动平均值，衰减率为min{0.99，（1+step）/（10+step)=0.1} = 0.1
            #所以v1的滑动平均会被更新为0.1*0+0.9*5 = 4.5
            sess.run(self.maintain_averages_op)
            print(sess.run([self.v1, self.ema.average(self.v1)]))

            #更新step到10000
            sess.run(tf.assign(self.step, 10000))
            # 更新变量v1的值到10
            sess.run(tf.assign(self.v1, 10))
            # 更新v1的滑动平均值，衰减率为min{0.99，（1+step）/（10+step)=0.999} = 0.99
            # 所以v1的滑动平均会被更新为0.99*4.5+0.01*10 = 4.555
            sess.run(self.maintain_averages_op)
            print(sess.run([self.v1, self.ema.average(self.v1)]))

            #再次更新滑动平均值，得到的新滑动平均值为：0.99*4.555+0.01*10 = 4.60945
            sess.run(self.maintain_averages_op)
            print(sess.run([self.v1, self.ema.average(self.v1)]))

mov = MovingAverage()
mov.run()
