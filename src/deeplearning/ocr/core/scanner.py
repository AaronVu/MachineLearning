# -*- coding:utf-8 -*-
"""
@File      : scanner.py
@Software  : OCR
@Time      : 2018/4/15 18:11
@Author    : yubb
"""
import cv2
import numpy as np


class Scanner:

    """
    Vertical edge:     Horizontal edge:
        [[-1, 0, 1],      [[1, 1, 1],
        [-1, 0, 1],       [0, 0, 0],
        [-1, 0, 1]]       [-1, -1, -1]]
    """

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.cur_h, self.cur_w = 0, 0
        self.ver_edge = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        self.hor_edge = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

    def split_image(self, path):
        img_matrix = self.prepare(path)
        self.scanning(img_matrix)

    def scanning(self, img_matrix):
        print(self.width, img_matrix)

    def prepare(self, path):
        """
        preprocessor:
            1、Binaryzation
            2、Remove blank edges
        :param path: path of image
        :return: numpy.array
        """
        img = cv2.imread(path, 0)
        ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        self.cur_h, self.cur_w = img.shape
        return img


def split_hor_edge():
    img1 = cv2.imread('./exam.png', 0)
    ret, img = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)
    # ver_edge = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    hor_edge = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    height, width = img.shape
    x_axis, y_axis, x_span, y_span, num = 0, 0, 3, 3, 0
    h_rs, h_row_rs = None, None
    for h_idx in range(height - 2):
        for w_idx in range(width - 2):
            tmp_arr = img[h_idx:h_idx + y_span, w_idx:w_idx + x_span]
            # v_tmp = np.sum(ver_edge * tmp_arr)
            h_tmp = np.sum(hor_edge * tmp_arr)
            if h_row_rs is None:
                h_row_rs = h_tmp
            else:
                h_row_rs = np.hstack((h_row_rs, h_tmp))
        if h_rs is None:
            h_rs = h_row_rs
        else:
            h_rs = np.vstack((h_rs, h_row_rs))
        h_row_rs = None
    h, w = h_rs.shape
    cur_is_having, pre_is_having, pre_idx = False, False, 0
    for h_ in range(h):
        line = h_rs[h_, :]
        cur_is_having = len(np.where(line != 0)[0]) > 0
        if cur_is_having:
            if not pre_is_having:
                pre_idx = h_
        else:
            if pre_is_having:
                cv2.imwrite('./tmp/{}.png'.format(h_), img1[pre_idx:h_, :])
                pre_idx = h_
        pre_is_having = cur_is_having
    # cv2.imwrite('./tmp/h.png', h_rs)
    # cv2.imwrite('./tmp/v.png', v_rs)
    # cv2.imwrite('./tmp/all.png', h_rs * v_rs)
    return h_rs


def max_distance(cols):
    max_d = 0
    pre_max = 0
    for idx in range(len(cols)):
        if idx + 1 < len(cols):
            if cols[idx + 1] - cols[idx] == 1:
                max_d += 1
            else:
                pre_max = max_d if max_d > pre_max else pre_max
                max_d = 0
    return pre_max


def split_vor_edge(path='./tmp/112.png'):
    img1 = cv2.imread(path, 0)
    ret, img = cv2.threshold(img1, 125, 255, cv2.THRESH_BINARY)
    cv2.imwrite('./tmp/rs/bin.png', img)
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

    cv2.imwrite('./tmp/rs/v.png', v_rs)
    h, w = v_rs.shape
    cur_is_having, pre_is_having, begin = False, False, 0

    # col_map = np.ones(w) * 255
    map = None
    for idx in range(w):
        col = img[:, idx]
        arr = np.where(col == 0)[0]
        col = col.reshape(len(col), 1)
        if len(arr):
            col[arr[0]:] = 0
        if map is None:
            map = col
        else:
            map = np.hstack((map, col))
    cv2.imwrite('./tmp/rs/map.png', map)
    # for x in cols:
    #     col_map[x] = 0
    # cv2.imwrite('./tmp/rs/map.png', col_map.reshape(1, w))
    # print(col_map)

    for w_ in range(w):
        cur_is_having = len(np.where(v_rs[:, w_] != 0)[0]) > 0

        # 字符开始
        if cur_is_having and not pre_is_having:
            if w_ - begin >= 20:
                begin = w_

        # 字符结束
        if pre_is_having and not cur_is_having:
            if w_ - begin >= 17:
                cv2.imwrite('./tmp/rs/{}.png'.format(w_), img1[:, begin:w_])
        pre_is_having = cur_is_having


np.set_printoptions(threshold=np.nan)
split_hor_edge()
# split_vor_edge()