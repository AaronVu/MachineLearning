# -*- coding:utf-8 -*-
"""
@File      : test.py
@Software  : DeepOCR
@Time      : 2018/4/20 8:05
@Author    : yubb
"""
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.patches as mpatches


def analysed(path):
    img = cv2.imread(path)
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)
    _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(img, contours, -1, (0, 0, 255))
    rects = []
    for contour in contours:
        x1, y1, w1, h1 = cv2.boundingRect(contour)
        rects.append((x1, y1, w1, h1))
    rects.sort()
    return rects, img


def find(x_arr, h_max):
    rs = []
    cur = None
    for idx in range(len(x_arr)):
        begin = x_arr[idx]
        vir_end = begin + h_max
        for i in range(len(x_arr)):
            if i == len(x_arr) - 1:
                break
            if x_arr[i] < vir_end < x_arr[i + 1]:
                end = (x_arr[i] + x_arr[i + 1]) // 2
                if cur and begin < cur:
                    break
                if x_arr[i + 1] - x_arr[i] < h_max:
                    rs.append((begin, end))
                cur = end
                break
    rs.append((x_arr[-1], x_arr[-1] + h_max))
    return rs


def show(img, rs, height):
    fig, axes = plt.subplots(1, len(rs), figsize=(height, height))
    idx = 0
    for ax in axes.ravel():
        ax.imshow(img[0:height, rs[idx][0]:rs[idx][1]])
        idx += 1
    fig.tight_layout()
    plt.show()


def show_rects(rects):
    idx = 0
    fig, axis = plt.subplots()
    boxes = []
    for rect in rects:
        if idx > 0:
            box = mpatches.Rectangle(rect[0:2], rect[2], rect[3], ec='none')
            boxes.append(box)
        idx += 1
    pc = PatchCollection(boxes, facecolor='r', alpha=0.3, edgecolor='None')
    axis.add_collection(pc)
    axis.errorbar([x[0] for x in rects], [x[1] for x in rects], fmt='None', ecolor='b')
    plt.tight_layout()
    plt.show()


def what_rests(rects):
    for rect in rects:
        print(rect)


def split_vor(img):
    cv2.imshow('f', img)
    cv2.waitKey(0)
    ver_edge = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    height, width = img.shape
    x_axis, y_axis, x_span, y_span, num = 0, 0, 3, 3, 0
    v_rs, v_row_rs = None, None
    for h_idx in range(height - 2):
        for w_idx in range(width - 2):
            tmp_arr = img[h_idx:h_idx + y_span, w_idx:w_idx + x_span]
            v_tmp = np.sum(ver_edge * tmp_arr)
            if v_row_rs is None:
                v_row_rs = v_tmp
            else:
                v_row_rs = np.hstack((v_row_rs, v_tmp))
        if v_rs is None:
            v_rs = v_row_rs
        else:
            v_rs = np.vstack((v_rs, v_row_rs))
        v_row_rs = None
    print(v_rs[4])
    cv2.imshow('f', v_rs)
    cv2.waitKey(0)
    return v_rs


def analyse(path):
    img = cv2.imread(path, 0)
    ret, thresh = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY)
    imgray = cv2.GaussianBlur(thresh, (3, 3), 0)
    imgray = cv2.Canny(imgray, 50, 150)
    _, contours, hierarchy = cv2.findContours(imgray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    rects = []
    for contour in contours:
        x1, y1, w1, h1 = cv2.boundingRect(contour)
        rects.append([x1, y1, w1, h1])
    rects.sort()
    return rects


def select(rects):
    rs_rects = []
    begin = rects[0]
    for idx in range(1, len(rects)):
        cur = rects[idx]
        if begin[0] + begin[2] <= cur[0]:
            begin[1] = 0
            begin[3] = 21
            rs_rects.append(begin)
            begin = cur
        else:
            dis = cur[0] + cur[2] - begin[0] - begin[2]
            if dis > 0:
                begin[2] += dis
            if cur[3] > begin[3]:
                begin[3] = cur[3]
            if cur[1] < begin[1]:
                begin[1] = cur[1]
    return rs_rects


def main():
    rects = select(analyse('./tmp/504.png'))
    img = cv2.imread('./tmp/504.png')
    h, w, _ = img.shape
    idx = 0
    for rect in rects:
        tmp_img = img[0:h, rect[0]:rect[0] + rect[2]]
        cv2.imwrite('./tmp/rs/{}.png'.format(idx), tmp_img)
        idx += 1
        # t_im = np.copy(img)
        # cv2.rectangle(t_im, tuple(rect[0:2]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 0, 255), 1)
        # cv2.imshow('Image', t_im)
        # cv2.waitKey(0)

"""
if __name__ == '__main__':
    arr1 = np.array([5, 7])
    arr2 = np.array([[0, 1],
                     [1, 2],
                     [1, 2]])

    n = np.array([arr1 for i in range(arr2.shape[0])])
    n[1, :] = [3, 1]
    print(n)
    # dist = np.sqrt(np.sum(np.square(np.subtract(arr1, arr2)), axis=1))
    # print(np.where(dist == np.min(dist))[0])

"""
