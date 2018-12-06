# -*- coding:utf-8 -*-
import cv2


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
    return select(rects), img


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
    rs_rects.append(rects[-1])
    return rs_rects


def split(path):
    rects, img = analyse(path)
    h, w = img.shape
    idx = 0
    for rect in rects:
        tmp_img = img[0:h, rect[0]:rect[0] + rect[2]]
        cv2.imwrite('./tmp/rs/{}.png'.format(idx), tmp_img)
        idx += 1


