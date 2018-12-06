# -*- coding:utf-8 -*-
"""
@File      : gen_img.py
@Software  : OCR
@Time      : 2018/3/30 12:22
@Author    : yubb
"""
import os
from PIL import Image, ImageFont, ImageDraw
from tools.common import list_files

'''
Unicode范围:
    汉字: 0x4E00 - 0x9FA5
    数字：0x30 - 0x39 
    小写字母：0x61 - 0x7a
    大写字母：0x41 - 0x5a
'''

RANGE_LIST = [(0x4e00, 0x9FA6), (0x30, 0x3a), (0x61, 0x7b), (0x41, 0x5b)]
CH_SIZE = 20902
MODE = 'RGB'
IMG_SIZE = (35, 35)
COLOR = (255, 255, 255)
FONT_SIZE = 28
DIR_NAME = 'text_data'


def create_img(txt, name=None, font='simsun.ttc', dest='.'):
    img = Image.new(MODE, IMG_SIZE, COLOR)
    draw = ImageDraw.Draw(img)
    cur_font_size = FONT_SIZE
    if name in '12':
        cur_font_size = 27
    font = ImageFont.truetype(os.path.join("fonts", font), cur_font_size)
    draw.text((2, 2), txt, font=font, fill="#000000")
    img.save("{}/{}.png".format(dest, name))


def gen_ch_txt(dest='.'):
    print('Start to generating pictures...')
    dest = os.path.join(dest, DIR_NAME)
    if not os.path.exists(dest):
        os.makedirs(dest)
    files = list_files(dest)
    if len(files) < 20000:
        for (begin, end) in RANGE_LIST:
            for idx in range(begin, end):
                ch_txt = '\\u{0:04x}'.format(idx).encode('utf8').decode('unicode_escape')
                if ch_txt in 'abcdefghijklmnopqrstuvwxyz':
                    dt = os.path.join(dest, ch_txt + str(0))
                elif ch_txt in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    dt = os.path.join(dest, ch_txt + str(1))
                else:
                    dt = os.path.join(dest, ch_txt)
                if not os.path.exists(dt):
                    os.makedirs(dt)
                create_img(ch_txt, name='0', dest=dt)
                create_img(ch_txt, name='1', font='msyh.ttc', dest=dt)
                create_img(ch_txt, name='2', font='msyhl.ttc', dest=dt)
        files = list_files(dest)
    print('Number of pictures:',
          len(files),
          '\nPosition of image:',
          dest,
          '\nFinished!')


def show_img(txt, dest='../../resources/train_data'):
    dest = os.path.join(dest, DIR_NAME, txt + '.png')
    img = Image.open(dest)
    img.show()


# gen_ch_txt()
# print('\\u{0:04x}'.format(0x30).encode('utf8').decode('unicode_escape'))
