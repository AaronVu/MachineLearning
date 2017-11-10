from tensorflow.examples.tutorials.mnist import input_data

class DownloadMNIST:

    def load(self):
        '''
        #载入MNIST数据集
        :return:
        '''
        self.mnist = input_data.read_data_sets("../../resources", one_hot=True)
        '''
        print("Training data size:",self.mnist.train.num_examples)
        print("Validating data size:", self.mnist.validation.num_examples)
        print("Testing data size:", self.mnist.test.num_examples)
        print("Example training data:", self.mnist.train.images[0])
        print("Example training data label:", self.mnist.train.labels[0])
        '''

    def test(self):
        self.load()
        batch_size = 100
        xs, ys = self.mnist.train.next_batch(batch_size)
        print("X shape:", xs.shape)
        print("Y shape:", ys.shape)

'''
dow = DownloadMNIST()
dow.test()
'''
