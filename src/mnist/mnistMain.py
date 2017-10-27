#coding:utf-8
import tensorflow as tf
import src.mnist.mnist_inference as inference
import src.mnist.mnist_train as train
import cv2
import numpy as np
from PIL import Image
from tensorflow.examples.tutorials.mnist import input_data


EVAL_INTERVAL_SECS = 10


def deal_input_img(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE).astype(np.float32)
    img = cv2.resize(img, (28, 28))
    local = path.split('/')[-1]
    if cv2.imwrite(local, img):
        return local


def evaluate(path):

    # im = cv2.imread('../../resources/test/12.png', cv2.IMREAD_GRAYSCALE).astype(np.float32)
    # im = cv2.resize(im, (28, 28))
    #
    # img_gray = (im - (255 / 2.0)) / 255
    # x_img = np.reshape(img_gray, [-1, 784])
    local = deal_input_img(path)
    if local:
        im = Image.open(local)
        im = np.array(im).astype(np.float32)
        im = (im % 255) % 2
        x_img = np.reshape(im, [1, 784])

        analysis = inference.inference(x_img, None)

        variable_averages = tf.train.ExponentialMovingAverage(train.MOVING_AVERAGE_DECAY)
        variable_to_restore = variable_averages.variables_to_restore()
        saver = tf.train.Saver(variable_to_restore)

        with tf.Session() as sess:
            ckpt = tf.train.get_checkpoint_state(train.MODEL_SAVE_PATH)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                result = sess.run(tf.argmax(analysis, 1))
                return result[0]
                #print("Number in image:", result[0])
            else:
                print("No checkpoint file found!")


def test():
    mnist = input_data.read_data_sets("../../resources",one_hot=True)
    print(mnist.validation.labels)


def train_eval(path):
    import os
    files = os.listdir(path)
    with open('label.txt') as f:
        str_label = f.read()
        labels = str_label.split(',')
    return files, labels


def main(argv=None):
    path = '../../resources/test/1.png'
    index = path.split('/')[-1].split('.')[0]
    with open('../../resources/qrc/label.txt') as f:
        str_label = f.read()
        labels = str_label.split(',')
        print(labels[int(index)])
    print(evaluate(path))
    #test()
    # files, labels = train_eval('../../resources/test')
    # for fileName in files:
    #     index = fileName.split('.')[0]
    #     num = evaluate('../../resources/test/'+fileName)
    #     if num == labels[int(index)]:
    #         print("Success")
    #     else:
    #         print('Failed')
    #     #print(fileName, labels[int(index)])

if __name__ == "__main__":
    main()
