# -*- coding:utf-8 -*-
"""
@File      : dataset.py
@Software  : OCR
@Time      : 2018/3/31 20:34
@Author    : yubb
"""
import os
import cv2
import numpy as np
from PIL import Image
import operator
from functools import reduce
from itertools import combinations
from tools.common import list_files


SAMPLE_SIZE = 3


def encode_img(path, tmp='./tmp'):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(path + " is None!")
        exit(0)
    img.astype(np.float32)
    img = cv2.resize(img, (35, 35))
    ret, thresh = cv2.threshold(img, 155, 255, cv2.THRESH_BINARY)
    return thresh
    # local = path.split('\\')[-1]
    # local = os.path.join(tmp, local)
    # if not os.path.exists(tmp):
    #     os.makedirs(tmp)
    # if cv2.imwrite(local, img):
    #     return local


class TextDataSet:

    def __init__(self, path):
        dirs, files = list_files(path)
        self.dirs = dirs[1:]
        self.dataset_size = len(self.dirs)
        self.current_index = 0

    def _next_batch(self, batch_size):
        if batch_size > self.dataset_size:
            raise Exception("Bad batch_size!")
        pre_idx = self.current_index
        end_idx = self.current_index + batch_size
        if end_idx > self.dataset_size:
            self.current_index = self.dataset_size
            return self.dirs[pre_idx:]
        self.current_index = self.current_index + batch_size
        return self.dirs[pre_idx:end_idx]

    def next_batch(self, batch_size):
        dirs = self._next_batch(batch_size)
        imgs, paths, labels = [], [], []
        for d in dirs:
            label = d.split('\\')[-1]
            _, ims = list_files(d)
            if len(label) > 1:
                label = label[0:1]
            labels.extend(label * len(ims))
            paths.extend(ims)
            imgs.append(ims)
        # datas = []
        # for d in range(len(imgs)):
        #     tmp_dirs = imgs[0:]
        #     tmp_dirs.remove(imgs[d])
        #     dt = transform(imgs[d], tmp_dirs)
        #     datas.append(dt)
        # return dirs, reduce(operator.add, datas), labels
        return imgs, paths, labels


def load_data(paths):
    dts = []
    if isinstance(paths, list):
        for path in paths:
            im = encode_img(path)
            dts.append(im)
    else:
        return encode_img(paths)
    return dts


def transform(dirs, tmp_dirs):
    combs = list(combinations(dirs, 2))
    tmp_dirs = reduce(operator.add, tmp_dirs)
    rs = []
    for tmp_dir in tmp_dirs:
        for comb in combs:
            tmp = list(comb)
            tmp.append(tmp_dir)
            rs.append(tmp)
    return rs


def load_embs_data(path):
    dirs, files = list_files(path)
    return [x for x in files if '0' in x], [x[-1] for x in dirs[1:]]


def test():
    dataset = TextDataSet('./data')
    paths, labels, _ = dataset.next_batch(3)
    print(paths, labels)



def main():
    files, labels = load_embs_data('../core/data')
    print(files, labels)


