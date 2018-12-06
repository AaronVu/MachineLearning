# -*- coding:utf-8 -*-
import cv2  
import numpy as np  
from matplotlib import pyplot as plt 


def adaptive(img):
    ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    images = [img, th1, th2, th3]
    plt.figure()
    for i in range(4):
        plt.subplot(2, 2, i+1)
        plt.imshow(images[i], 'gray')
    plt.show()


def threshold(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray_img, 200, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    titles = ['Gray Image', 'BINARY', 'BINARY_OTSU']
    images = [gray_img, thresh1, thresh2]
    cv2.imwrite('./test.png', thresh2)
    for i in range(3):
        plt.subplot(3, 1, i+1)
        plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([])
        plt.yticks([])
    plt.show()


def analysed_episode(im, img, xaxis, yaxis):
    # 边缘判定
    up, down, left, right = im[0], im[9], im[:, 0], im[:, 9]
    print("Begin: ")
    up_where = np.where(up == 0)
    if len(up_where[0]):
        print("Up Had!")
    down_where = np.where(down == 0)
    if len(down_where[0]):
        print("Down Had!")
    left_where = np.where(left == 0)
    if len(left_where[0]):
        print("Left Had!")
    right_where = np.where(right == 0)
    if len(right_where[0]):
        print("Right Had!")
    print("End!")
    return None


def split_img(path):
    img = cv2.imread(path, 0)
    ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    height, width = img.shape
    print("Image Size: {}:{}".format(width, height))
    x_axis, y_axis, x_span, y_span, num = 0, 0, 10, 10, 0
    for episode in range(height - y_span):
        for idx in range(width - x_span):
            tmp_arr = img[y_axis:y_axis + y_span, x_axis:x_axis + x_span]
            x_axis += x_span
            if x_axis > width or x_axis + x_span > width:
                num += 1
                break
            im = analysed_episode(tmp_arr, img, x_axis, y_axis)
            # cv2.imwrite('./tmp/{}.png'.format(num), im)
            num += 1
            #  return
        y_axis += y_span
        x_axis = 0
        if y_axis > height or y_axis + y_span > height:
            break
    print("OK!")


def main():
    split_img('E:\\tmp\\timg.jpg')


if __name__ == '__main__':
    main()