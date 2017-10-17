#coding:utf-8
import tensorflow as tf
import src.mnist.mnist_inference as inference
import src.mnist.mnist_train as train
import cv2
import numpy as np

EVAL_INTERVAL_SECS = 10

def evaluate():

    im = cv2.imread('../../resources/temp/timg5.jpg', cv2.IMREAD_GRAYSCALE).astype(np.float32)
    im = cv2.resize(im, (28, 28))
    img_gray = (im - (255 / 2.0)) / 255
    x_img = np.reshape(img_gray, [-1, 784])
    analysis = inference.inference(x_img, None)

    variable_averages = tf.train.ExponentialMovingAverage(train.MOVING_AVERAGE_DECAY)
    variable_to_restore = variable_averages.variables_to_restore()
    saver = tf.train.Saver(variable_to_restore)

    with tf.Session() as sess:
        ckpt = tf.train.get_checkpoint_state(train.MODEL_SAVE_PATH)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            result = sess.run(analysis)
            print("Number in image:", np.argmax(result))
        else:
            print("No checkpoint file found!")


def main(argv=None):
    evaluate()

if __name__ == "__main__":
    main()
